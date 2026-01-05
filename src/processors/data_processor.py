"""数据处理模块"""

from typing import Optional
import pandas as pd


class DataProcessor:
    """数据处理器"""

    @staticmethod
    def clean_price_data(df: pd.DataFrame) -> pd.DataFrame:
        """清洗价格数据"""
        if df is None or df.empty:
            return df

        # 去除空值行
        df = df.dropna()

        # 去除重复行
        df = df.drop_duplicates()

        return df

    @staticmethod
    def merge_contract_data(data_list: list) -> Optional[pd.DataFrame]:
        """合并合约数据"""
        if not data_list:
            return None

        combined = pd.concat(data_list, ignore_index=True)
        return combined

    @staticmethod
    def filter_by_date(df: pd.DataFrame, start_date: str, end_date: str) -> pd.DataFrame:
        """按日期范围筛选"""
        if df is None or df.empty:
            return df

        df["日期"] = pd.to_datetime(df["日期"])
        mask = (df["日期"] >= start_date) & (df["日期"] <= end_date)
        return df[mask]

    @staticmethod
    def calculate_statistics(df: pd.DataFrame) -> dict:
        """计算统计数据"""
        if df is None or df.empty:
            return {}

        stats = {
            "总记录数": len(df),
            "平均收盘价": df["收盘"].mean() if "收盘" in df.columns else None,
            "最高收盘价": df["收盘"].max() if "收盘" in df.columns else None,
            "最低收盘价": df["收盘"].min() if "收盘" in df.columns else None,
        }

        return stats
