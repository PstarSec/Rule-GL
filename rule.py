import os
import sys
import argparse
from rule_manager import RuleManager
from file_filter import FileFilter  # 确保导入的模块名是正确的
import random  # 导入 random 模块用于随机选择颜色


# 颜色设置
def colorize(text, color):
    color_map = {
        "yellow": "\033[93m",  # 黄色
        "green": "\033[92m",  # 绿色
        "red": "\033[91m",  # 红色
        "blue": "\033[94m",  # 蓝色
        "purple": "\033[95m",  # 紫色
        "reset": "\033[0m",  # 重置
    }
    return f"{color_map.get(color, color_map['reset'])}{text}{color_map['reset']}"


# 随机选择颜色
def random_colorize(text):
    color_map = [
        "\033[91m",  # 红色
        "\033[92m",  # 绿色
        "\033[93m",  # 黄色
        "\033[94m",  # 蓝色
        "\033[95m",  # 紫色
        "\033[96m",  # 青色
        "\033[97m",  # 白色
    ]

    # 为每个字符随机选择颜色
    colored_text = ""
    for char in text:
        colored_text += random.choice(color_map) + char

    return colored_text + "\033[0m"  # 重置颜色


# 输出日志（艺术字 + 作者）
def print_log():
    art = """
 _  /\ \/ / ___|      / ___| |
  / /  \  / |  _ _____| |  _| |
 / /_  /  \ |_| |_____| |_| | |___
/____|/_/\_\____|      \____|_____--Author: 摘星怪sec
"""
    # 输出艺术字，每行随机彩色
    art_lines = art.strip().split("\n")  # 去除首尾空白字符并分割为行
    for line in art_lines:
        print(random_colorize(line))  # 输出每行艺术字，并应用随机颜色


# 规则管理模块
def manage_rules():
    print_log()  # 输出日志
    rule_manager = RuleManager()
    rule_manager.run()


# 文件过滤模块
def filter_file(input_file, output_file):
    print_log()  # 输出日志
    file_filter = FileFilter()  # 使用 FileFilter 类
    file_filter.filter_file(input_file, output_file)  # 调用 filter_file 方法


# 自定义帮助信息输出
def custom_help():
    print_log()  # 输出日志
    print(
        """
options:
  -h, --help    显示此帮助消息并退出，提供所有命令的详细使用说明。
  -u            输入文件路径，支持 .txt 格式文件。用于过滤操作的原始文件。
  -o            输出文件路径。若提供的是目录，则自动生成文件名。
  -ul           进入规则管理模块，可动态管理规则。

FLAGS (规则管理模式专用参数，需使用 -ul 启用):
  --z=增加      添加新的规则，支持多个规则以逗号`,`分隔。
                示例: --z="127.0.0.1,*.gov.cn"
  --s=删除      删除指定规则，通过规则序号选择删除目标。
  --g=更改      修改指定规则，支持编辑已有规则内容。

EXAMPLES:
  python rule.py -u "input.txt" -o "output.txt"
      过滤 input.txt 文件内容并将结果保存至 output.txt 文件中。

  python rule.py -u "input.txt"
      过滤 input.txt 文件内容并将结果保存至当前目录下的自动生成文件中。

  python rule.py -ul
      进入规则管理模块，可选择添加、删除或修改规则。

  python rule.py -u "input.txt" -o "output.txt" - 选择保留命中的文本或过滤后的文本:
      执行过滤操作时，您可以选择以下两种方式：
      1. 只保留命中的文本（即匹配到规则的文本）
      2. 保留过滤后的文本（不包含命中规则的文本）
      
注意:
  1. 规则添加时需要遵循有效的 IP 或域名格式。
  2. 输出文件路径若为目录，系统会自动生成带时间戳的文件名以避免覆盖。
  3. 执行过滤操作前，确保规则库中至少有一个可用规则。
"""
    )


# 主函数
def main():
    # 解析命令行参数
    parser = argparse.ArgumentParser(description="GL-ZXG工具", add_help=False)
    parser.add_argument(
        "-h", "--help", help="显示此帮助信息", action="store_true"
    )  # 手动添加帮助选项
    parser.add_argument("-u", help="输入文件路径", type=str)
    parser.add_argument(
        "-o", help="输出文件路径", type=str, default=os.getcwd()
    )  # 默认是当前路径
    parser.add_argument("-ul", help="进入规则管理模块", action="store_true")

    args = parser.parse_args()

    # 如果传入了 -h 或 --help，显示帮助信息
    if args.help:
        custom_help()  # 自定义帮助输出
        return

    # 进入规则管理模块
    if args.ul:
        manage_rules()  # 进入规则管理模块
    # 进行文件过滤
    elif args.u and args.o:  # 确保提供了输入文件路径和输出文件路径
        input_file = args.u
        output_file = args.o  # 如果没有提供输出路径，将使用默认路径
        filter_file(input_file, output_file)  # 调用文件过滤功能
    else:
        print("没有提供任何有效的参数。请输入 '-h' 或 '--help' 获取帮助。")


if __name__ == "__main__":
    main()
