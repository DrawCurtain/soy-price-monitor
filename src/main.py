#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
大豆价格监控与数据分析系统
主入口文件
"""

from collectors import DCECollector
from exporters import ExcelExporter
from config import TARGET_COLUMNS


def main():
    """主函数"""
    print("=" * 60)
    print("大豆价格监控与数据分析系统")
    print("=" * 60)

    # 采集数据
    collector = DCECollector()
    result = collector.collect_all()

    # 导出数据
    if result["contracts_data"] or result["yearly_data"]:
        exporter = ExcelExporter()
        exporter.export(
            contracts_data=result["contracts_data"],
            yearly_data=result["yearly_data"]
        )

        # 打印统计信息
        if result["contracts_data"]:
            from processors import DataProcessor
            combined = DataProcessor.merge_contract_data(result["contracts_data"])
            if combined is not None:
                print(f"\n📈 汇总数据共 {len(combined)} 条记录")
                print(f"📋 包含字段：{', '.join(TARGET_COLUMNS)}")
    else:
        print("\n❌ 未获取到任何有效数据")


if __name__ == "__main__":
    main()
