from setuptools import setup, find_packages

setup(
    name="soy-price-monitor",
    version="1.0.0",
    description="大豆价格监控与数据分析系统",
    author="Your Name",
    author_email="your.email@example.com",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.10",
    install_requires=[
        "efinance>=0.5.0",
        "pandas>=2.0.0",
        "openpyxl>=3.1.0",
        "requests>=2.31.0",
        "matplotlib>=3.7.0",
    ],
    entry_points={
        "console_scripts": [
            "soy-monitor=src.main:main",
        ],
    },
)
