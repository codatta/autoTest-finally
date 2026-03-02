# run.py
# 统一运行入口：解析命令行参数并调用 pytest。
# 我在此处添加注释，并为方便本地使用，自动设置 PYTHONPATH 指向包根（如果尚未设置）。

import argparse
import subprocess
import sys
import os


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-e', '--env', default='test', help='environment name: test/staging/prod')
    parser.add_argument('-m', '--marker', default='smoke', help='pytest marker to run')
    args = parser.parse_args()

    # 如果未设置 PYTHONPATH，则将当前目录（脚本所在目录）加入 PYTHONPATH，便于导入 api_test_framework 包
    pkg_root = os.path.dirname(os.path.abspath(__file__))
    if 'PYTHONPATH' not in os.environ or not os.environ['PYTHONPATH']:
        # 仅在未设置时写入，避免覆盖已有环境设置
        os.environ['PYTHONPATH'] = pkg_root

    # 构造 pytest 命令：按 marker 运行测试，并将 HTML 报告输出到 reports/
    cmd = [sys.executable, '-m', 'pytest', 'testcases', '-m', args.marker,
           '--html=reports/report.html', '--self-contained-html']

    # 使用 subprocess 调用 pytest，若需要获取输出或更复杂的行为可以扩展此处
    subprocess.run(cmd, check=True)


if __name__ == '__main__':
    main()
