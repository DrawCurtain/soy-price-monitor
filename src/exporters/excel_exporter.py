"""Excel导出模块"""

import os
from typing import Optional, Dict

import pandas as pd

from ..config import get_project_root, EXCEL_FILENAME


class ExcelExporter:
    """Excel导出器"""

    def __init__(self, filename: str = None):
        self.project_root = get_project_root()
        self.filename = filename or EXCEL_FILENAME
        self.output_path = self.project_root / self.filename

    def export(self, contracts_data: list, yearly_data: Dict[str, pd.DataFrame],
               contracts_sheet_name: str = "合约汇总") -> str:
        """
        导出数据到Excel

        Args:
            contracts_data: 合约数据列表
            yearly_data: 主连年度数据字典
            contracts_sheet_name: 合约汇总sheet名称

        Returns:
            输出文件路径
        """
        # 删除已存在的旧文件
        if os.path.exists(self.output_path):
            os.remove(self.output_path)
            print(f"已删除旧文件：{self.output_path}")

        with pd.ExcelWriter(self.output_path, engine="openpyxl") as writer:
            # 写入合约汇总
            if contracts_data:
                combined_df = pd.concat(contracts_data, ignore_index=True)
                combined_df.to_excel(
                    writer,
                    sheet_name=contracts_sheet_name,
                    index=False,
                    engine="openpyxl"
                )
                print(f"\n📊 合约数据已写入sheet：{contracts_sheet_name}")

            # 写入年度数据
            for main_name, yearly_df in yearly_data.items():
                sheet_name = main_name[:31]
                yearly_df.to_excel(
                    writer,
                    sheet_name=sheet_name,
                    index=False,
                    engine="openpyxl"
                )
                print(f"📊 {main_name} 近一年数据已写入sheet：{sheet_name}")

        print(f"\n🎉 所有数据已汇总保存至：{self.output_path}")
        return str(self.output_path)

    def get_output_path(self) -> str:
        """获取输出路径"""
        return str(self.output_path)
