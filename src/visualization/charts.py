"""图表生成模块"""

from typing import Optional
import matplotlib.pyplot as plt
import pandas as pd


class ChartGenerator:
    """图表生成器"""

    def __init__(self):
        plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS']
        plt.rcParams['axes.unicode_minus'] = False

    def plot_price_trend(self, df: pd.DataFrame, title: str = "价格趋势",
                         save_path: Optional[str] = None):
        """
        绘制价格趋势图

        Args:
            df: 包含日期和收盘价的DataFrame
            title: 图表标题
            save_path: 保存路径
        """
        if df is None or df.empty:
            print("⚠️ 无数据可绘制")
            return

        fig, ax = plt.subplots(figsize=(12, 6))

        ax.plot(pd.to_datetime(df["日期"]), df["收盘"], marker='o', markersize=2)

        ax.set_title(title)
        ax.set_xlabel("日期")
        ax.set_ylabel("收盘价")
        ax.grid(True, alpha=0.3)

        plt.xticks(rotation=45)
        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=150)
            print(f"📊 图表已保存至：{save_path}")

        plt.show()

    def plot_volume(self, df: pd.DataFrame, title: str = "成交量",
                    save_path: Optional[str] = None):
        """绘制成交量图"""
        if df is None or df.empty:
            print("⚠️ 无数据可绘制")
            return

        fig, ax = plt.subplots(figsize=(12, 6))

        ax.bar(pd.to_datetime(df["日期"]), df["成交量"], alpha=0.7)

        ax.set_title(title)
        ax.set_xlabel("日期")
        ax.set_ylabel("成交量")
        ax.grid(True, alpha=0.3)

        plt.xticks(rotation=45)
        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=150)
            print(f"📊 图表已保存至：{save_path}")

        plt.show()

    def create_price_comparison(self, dfs: dict, save_path: Optional[str] = None):
        """
        创建价格对比图

        Args:
            dfs: 字典，key为合约名称，value为DataFrame
            save_path: 保存路径
        """
        fig, ax = plt.subplots(figsize=(14, 7))

        for name, df in dfs.items():
            if df is not None and not df.empty:
                ax.plot(pd.to_datetime(df["日期"]), df["收盘"], marker='o',
                        markersize=2, label=name)

        ax.set_title("多合约价格对比")
        ax.set_xlabel("日期")
        ax.set_ylabel("收盘价")
        ax.legend()
        ax.grid(True, alpha=0.3)

        plt.xticks(rotation=45)
        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=150)
            print(f"📊 图表已保存至：{save_path}")

        plt.show()
