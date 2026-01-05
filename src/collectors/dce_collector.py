"""大连商品交易所数据采集模块"""

import time
from datetime import datetime
from typing import Optional, List, Dict, Any

import efinance as ef
import pandas as pd
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from ..config import (
    TARGET_VARIETIES,
    VALID_FUTURES_MONTHS,
    RAW_TARGET_COLUMNS,
)


class DCECollector:
    """大商所期货数据采集器"""

    def __init__(self):
        self.session = requests.Session()
        retry = Retry(total=5, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
        adapter = HTTPAdapter(max_retries=retry)
        self.session.mount('http://', adapter)
        self.session.mount('https://', adapter)

    def get_start_contract_month(self) -> Dict[str, Any]:
        """根据当前日期智能计算合约起始月份"""
        now = datetime.now()
        current_year = now.year
        current_month = now.month

        start_month = current_month
        start_year = current_year

        while start_month not in VALID_FUTURES_MONTHS:
            start_month += 1
            if start_month > 12:
                start_month = 1
                start_year += 1

        start_contract_suffix = f"{str(start_year)[-2:]}{str(start_month).zfill(2)}"

        return {
            "start_year": start_year,
            "start_month": start_month,
            "start_contract_suffix": start_contract_suffix
        }

    def get_next_valid_month(self, current_year: int, current_month: int) -> tuple:
        """获取下一个有效交易月份"""
        next_month = current_month + 1
        next_year = current_year

        if next_month > 12:
            next_month = 1
            next_year += 1

        while next_month not in VALID_FUTURES_MONTHS:
            next_month += 1
            if next_month > 12:
                next_month = 1
                next_year += 1

        return next_year, next_month

    def build_contract_list(self, valid_contracts_ahead: int = 9) -> tuple:
        """动态构建合约列表"""
        target_contracts = []
        start_info = self.get_start_contract_month()

        # 添加主连合约
        for variety in TARGET_VARIETIES:
            main_contract = {
                "期货名称": variety["主连名称"],
                "期货代码": variety["主连代码"],
                "行情ID": f"114.{variety['主连代码']}"
            }
            target_contracts.append(main_contract)

        current_contract_year = start_info["start_year"]
        current_contract_month = start_info["start_month"]

        for _ in range(valid_contracts_ahead):
            contract_month_suffix = f"{str(current_contract_year)[-2:]}{str(current_contract_month).zfill(2)}"

            for variety in TARGET_VARIETIES:
                variety_prefix = variety["品种前缀"]
                variety_name = variety["品种名称"]

                contract_code = f"{variety_prefix}{contract_month_suffix}"
                contract_name = f"{variety_name}{contract_month_suffix}"
                quote_id = f"114.{contract_code}"

                target_contracts.append({
                    "期货名称": contract_name,
                    "期货代码": contract_code,
                    "行情ID": quote_id
                })

            current_contract_year, current_contract_month = self.get_next_valid_month(
                current_contract_year, current_contract_month
            )

        target_contracts = sorted(
            list({c["行情ID"]: c for c in target_contracts}.values()),
            key=lambda x: x["期货代码"]
        )
        return target_contracts, start_info

    def get_contract_history(self, quote_id: str, contract_name: str, contract_code: str,
                             max_retries: int = 3) -> Optional[pd.DataFrame]:
        """获取单个合约历史K线数据"""
        retry_count = 0
        while retry_count < max_retries:
            try:
                df = ef.futures.get_quote_history(quote_id)
                if df.empty or not set(RAW_TARGET_COLUMNS).issubset(df.columns):
                    return None

                df = df[RAW_TARGET_COLUMNS].copy()
                df["日期"] = pd.to_datetime(df["日期"], errors='coerce')
                df = df.dropna(subset=["日期"]).sort_values(by="日期", ascending=False).reset_index(drop=True)

                if df.empty:
                    return None

                today = datetime.now().date()
                latest_data_date = df.iloc[0]["日期"].date()

                if latest_data_date < today:
                    print(f"   提示：当日（{today}）不开盘，自动提取上一开盘日（{latest_data_date}）数据")
                    df = df[df["日期"].dt.date == latest_data_date].copy()
                else:
                    print(f"   提示：当日（{today}）已开盘，保留完整历史数据（最新数据为{latest_data_date}）")

                from ..config import TARGET_COLUMNS
                df["期货名称"] = contract_name
                df["期货代码"] = contract_code
                df = df[TARGET_COLUMNS]
                df["日期"] = df["日期"].dt.strftime("%Y-%m-%d")

                return df
            except Exception as e:
                retry_count += 1
                print(f"获取{contract_name}（{contract_code}）数据失败（第{retry_count}次重试）：{str(e)}")
                if retry_count < max_retries:
                    time.sleep(2 ** retry_count)
        return None

    def get_main_contract_yearly_close(self, quote_id: str, variety_name: str,
                                        max_retries: int = 3) -> Optional[pd.DataFrame]:
        """获取主连合约近一年收盘数据"""
        retry_count = 0
        while retry_count < max_retries:
            try:
                from ..config import TODAY, ONE_YEAR_AGO

                df = ef.futures.get_quote_history(quote_id)
                if df.empty:
                    print(f"❌ {variety_name} 未获取到近一年历史数据")
                    return None

                core_df = df[["日期", "收盘"]].copy()
                core_df["日期"] = pd.to_datetime(core_df["日期"], errors='coerce').dt.date

                filter_mask = (core_df["日期"] >= ONE_YEAR_AGO) & (core_df["日期"] <= TODAY)
                filtered_df = core_df[filter_mask].dropna(subset=["日期"]).reset_index(drop=True)

                if filtered_df.empty:
                    print(f"❌ {variety_name} 近一年无有效历史数据")
                    return None

                result_df = filtered_df.rename(
                    columns={"日期": "日期", "收盘": "收盘价格"}
                ).sort_values(by="日期", ascending=True).reset_index(drop=True)

                result_df["日期"] = result_df["日期"].astype(str)

                print(f"✅ {variety_name} 近一年收盘数据爬取成功（共{len(result_df)}条记录）")
                return result_df
            except Exception as e:
                retry_count += 1
                print(f"❌ {variety_name} 近一年数据爬取失败（第{retry_count}次重试）：{str(e)}")
                if retry_count < max_retries:
                    time.sleep(2 ** retry_count)
        return None

    def collect_all(self) -> Dict[str, Any]:
        """采集所有数据"""
        # 动态构造合约列表
        print("正在根据当前日期智能构造豆粕、豆油有效合约列表...")
        target_contracts, start_info = self.build_contract_list(valid_contracts_ahead=9)

        if not target_contracts:
            print("❌ 未能构造出豆粕、豆油相关合约，程序终止")
            return {"contracts_data": [], "yearly_data": {}, "start_info": start_info}

        print(f"✅ 智能确定起始合约：{start_info['start_contract_suffix']}（{start_info['start_year']}年{start_info['start_month']}月）")
        print(f"✅ 有效交易月份：{sorted(VALID_FUTURES_MONTHS)}（已规避2、4、6月）")
        print(f"✅ 成功构造{len(target_contracts)}个豆粕、豆油合约")

        # 采集合约数据
        all_contracts_data = []
        print("\n开始批量爬取合约当日数据...")
        for contract in target_contracts:
            quote_id = contract["行情ID"]
            contract_name = contract["期货名称"]
            contract_code = contract["期货代码"]
            print(f"\n正在爬取：{contract_name}（{contract_code}）")

            contract_df = self.get_contract_history(quote_id, contract_name, contract_code)

            if contract_df is not None and not contract_df.empty:
                all_contracts_data.append(contract_df)
                print(f"✅ {contract_name} 数据爬取成功（共{len(contract_df)}条记录）")
            else:
                print(f"❌ {contract_name} 数据获取失败或无数据")

            time.sleep(1)

        # 采集主连近一年数据
        yearly_main_contract_data = {}
        print("\n" + "="*50)
        print("开始爬取主连品种近一年收盘数据...")
        print("="*50)
        for variety in TARGET_VARIETIES:
            main_name = variety["主连名称"]
            main_quote_id = f"114.{variety['主连代码']}"

            print(f"\n正在爬取：{main_name}")
            yearly_df = self.get_main_contract_yearly_close(main_quote_id, main_name)
            if yearly_df is not None and not yearly_df.empty:
                yearly_main_contract_data[main_name] = yearly_df

            time.sleep(1)

        return {
            "contracts_data": all_contracts_data,
            "yearly_data": yearly_main_contract_data,
            "start_info": start_info
        }
