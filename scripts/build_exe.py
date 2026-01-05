#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
打包脚本：将项目打包成 exe
使用方法: python scripts/build_exe.py
"""

import subprocess
import sys
import os

# 项目根目录
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOURCE_FILE = os.path.join(PROJECT_ROOT, "src", "main.py")


def build_exe():
    """使用 PyInstaller 打包脚本"""
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=大豆价格监控",
        "--onefile",
        "--console",
        "--clean",
        "--noupx",
        f"--paths={PROJECT_ROOT}",
        f"--specpath={PROJECT_ROOT}",
        f"--distpath={os.path.join(PROJECT_ROOT, 'dist')}",
        f"--workpath={os.path.join(PROJECT_ROOT, 'build')}",
        SOURCE_FILE
    ]

    print("=" * 50)
    print("开始打包...")
    print("=" * 50)
    print(f"项目目录: {PROJECT_ROOT}")
    print(f"源文件: {SOURCE_FILE}")

    result = subprocess.run(cmd)

    if result.returncode == 0:
        print("\n" + "=" * 50)
        print("打包成功！")
        print(f"输出目录: {os.path.join(PROJECT_ROOT, 'dist')}")
        print("=" * 50)
    else:
        print("\n打包失败，请检查错误信息。")
        sys.exit(1)


if __name__ == "__main__":
    build_exe()
