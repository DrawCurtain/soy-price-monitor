"""项目配置模块"""

import os
import sys
from pathlib import Path
from datetime import date, timedelta

# 项目根目录
def get_project_root() -> Path:
    """获取项目根目录"""
    if getattr(sys, 'frozen', False):
        return Path(sys.executable).parent
    return Path(__file__).parent.parent

# 数据输出目录
DATA_DIR = get_project_root() / "data"
DATA_DIR.mkdir(exist_ok=True)

# 目标品种配置
TARGET_VARIETIES = [
    {"品种名称": "豆粕", "品种前缀": "m", "主连代码": "mm", "主连名称": "豆粕主连"},
    {"品种名称": "豆油", "品种前缀": "y", "主连代码": "ym", "主连名称": "豆油主连"},
]

# 有效交易月份（排除2、4、6月）
VALID_FUTURES_MONTHS = [1, 3, 5, 7, 8, 9, 10, 11, 12]

# 时间配置
TODAY = date.today()
ONE_YEAR_AGO = TODAY - timedelta(days=365)

# 目标字段
RAW_TARGET_COLUMNS = ["日期", "开盘", "收盘", "最高", "最低", "成交量", "成交额", "振幅", "涨跌幅", "涨跌额"]
TARGET_COLUMNS = ["期货名称", "期货代码", "日期", "开盘", "收盘", "最高", "最低", "成交量", "成交额", "振幅", "涨跌幅", "涨跌额"]

# Excel 输出配置
EXCEL_FILENAME = "大豆价格数据汇总.xlsx"
