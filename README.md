# Soy Price Monitor

大豆价格监控与数据分析系统，支持大连商品交易所（DCE）期货数据采集与美国农业部（USDA）数据爬取。

## 功能特性

- **数据采集**: 采集豆粕、豆油等期货合约数据
- **数据处理**: 自动处理日期格式、数据清洗
- **多格式导出**: 支持 Excel 多 Sheet 导出
- **可视化支持**: 图表生成（预留）
- **实时数据**: 实时行情监控（预留）

## 项目结构

```
soy-price-monitor/
├── src/
│   ├── __init__.py
│   ├── main.py              # 主入口
│   ├── config.py            # 配置文件
│   ├── collectors/          # 数据采集模块
│   │   ├── __init__.py
│   │   └── dce_collector.py
│   ├── processors/          # 数据处理模块
│   │   ├── __init__.py
│   │   └── data_processor.py
│   ├── exporters/           # 导出模块
│   │   ├── __init__.py
│   │   └── excel_exporter.py
│   └── visualization/       # 可视化模块
│       ├── __init__.py
│       └── charts.py
├── tests/
│   └── __init__.py
├── scripts/
│   └── build_exe.py
├── data/
│   └── .gitkeep
├── notebooks/
├── docs/
├── requirements.txt
├── setup.py
└── README.md
```

## 安装

```bash
# 克隆项目
git clone https://github.com/yourusername/soy-price-monitor.git
cd soy-price-monitor

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
.\venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt
```

## 使用方法

### 运行主程序

```bash
python src/main.py
```

### 打包为 EXE

```bash
python scripts/build_exe.py
```

## 依赖

- efinance - 金融数据获取
- pandas - 数据处理
- openpyxl - Excel 导出
- requests - HTTP 请求
- matplotlib - 图表绘制（预留）

## License

MIT License
