import os
import re
import sys
import argparse
from datetime import datetime


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


class FileFilter:
    def __init__(self, blacklist_file="blacklist_rules.txt"):
        self.blacklist_file = blacklist_file
        self.rules = self.load_blacklist()

    def load_blacklist(self):
        """加载黑名单规则"""
        if os.path.exists(self.blacklist_file):
            with open(self.blacklist_file, "r") as f:
                return [line.strip() for line in f if line.strip()]
        print(f"黑名单文件 {self.blacklist_file} 不存在！")
        return []

    def match_pattern(self, rule, line):
        """匹配规则"""
        if "*" in rule:
            rule = rule.replace("*", ".*")
        return re.search(rule, line)

    def filter_file(self, input_file, output_file):
        """过滤文件并保存"""
        if not os.path.exists(input_file):
            print(f"输入文件 {input_file} 不存在！")
            return

        # 检查输出路径是否为目录，如果是，自动生成文件名
        if os.path.isdir(output_file):
            print(f"输出路径 {output_file} 是目录，自动生成文件名！")
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = os.path.join(output_file, f"output_{timestamp}.txt")

        # 如果输出路径的父目录不存在，则创建
        output_dir = os.path.dirname(output_file)
        if output_dir and not os.path.exists(output_dir):
            print(f"输出目录 {output_dir} 不存在，正在创建...")
            os.makedirs(output_dir)

        with open(input_file, "r", encoding="utf-8") as f:
            lines = f.readlines()

        # 存储命中的规则和对应文本（去重）
        matched_rules = {}
        matched_texts_set = set()  # 使用 set 去重

        # 过滤掉包含黑名单规则的行
        filtered_lines = [
            line
            for line in lines
            if not any(self.match_pattern(rule, line) for rule in self.rules)
        ]

        # 记录命中的规则及其文本
        for line in lines:
            for rule in self.rules:
                if self.match_pattern(rule, line):
                    if rule not in matched_rules:
                        matched_rules[rule] = 0
                    matched_rules[rule] += 1
                    matched_texts_set.add(line.strip())  # 添加到去重集合

        # 去除空行后写入文件
        filtered_lines = [line for line in filtered_lines if line.strip()]

        # 输出统计信息
        original_line_count = len(lines)  # 原始文本行数
        filtered_line_count = len(filtered_lines)  # 过滤后的文本行数

        print(f"\n过滤完成：")
        print(f"原始文本行数: {colorize(original_line_count, 'yellow')}")
        print(f"过滤后的文本行数: {colorize(filtered_line_count, 'yellow')}")
        print(f"命中的规则名称:")
        for rule in matched_rules:
            print(colorize(rule, "red"))

        # 输出命中的文本内容带序号
        print(f"命中的文本(数)如下:")
        for idx, text in enumerate(sorted(matched_texts_set), 1):  # 排序后编号
            print(colorize(f"{idx}: {text}", "blue"))

        # 写入输出文件
        with open(output_file, "w", encoding="utf-8") as f:
            f.writelines(filtered_lines)

        print(f"过滤完成，结果保存到：{colorize(output_file, 'purple')}")


# 示例：执行文件过滤
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="过滤文件脚本")
    parser.add_argument("-u", "--input", required=True, help="输入文件路径")
    parser.add_argument(
        "-o",
        "--output",
        help="输出文件路径，默认保存在当前脚本目录下的 output_<timestamp>.txt",
    )

    args = parser.parse_args()

    # 如果没有提供输出路径，则使用当前脚本目录下的 output_<timestamp>.txt
    if args.output:
        output_file = args.output
    else:
        # 获取当前脚本的路径
        script_dir = os.getcwd()  # 使用当前工作目录

        # 获取当前时间戳
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # 如果提供的输出路径是目录，生成带时间戳的文件名
        output_file = os.path.join(script_dir, f"output_{timestamp}.txt")

    input_file = args.input

    # 执行过滤操作
    file_filter = FileFilter()  # 创建文件过滤器实例
    file_filter.filter_file(input_file, output_file)  # 执行过滤操作
