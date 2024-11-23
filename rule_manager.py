import os
import re
import ipaddress


# 颜色设置
def colorize(text, color):
    color_map = {
        "yellow": "\033[93m",  # 黄色
        "green": "\033[92m",  # 绿色
        "red": "\033[91m",  # 红色
        "blue": "\033[94m",  # 蓝色
        "dark_blue": "\033[94m",  # 深蓝色
        "reset": "\033[0m",  # 重置
    }
    return f"{color_map.get(color, color_map['reset'])}{text}{color_map['reset']}"


class RuleManager:
    def __init__(self, blacklist_file="blacklist_rules.txt"):
        self.blacklist_file = blacklist_file
        self.rules = self.load_blacklist()

    def load_blacklist(self):
        if os.path.exists(self.blacklist_file):
            with open(self.blacklist_file, "r") as f:
                return [line.strip() for line in f if line.strip()]
        return []

    def save_blacklist(self):
        with open(self.blacklist_file, "w") as f:
            f.write("\n".join(self.rules))

    def validate_rule(self, rule):
        if ".." in rule:
            print(colorize("无效规则：包含连续的点 `..`", "red"))
            return False

        # 支持的IP地址格式：127.0.0.*，127.0.0.1/24等
        ip_pattern = r"^\d{1,3}(\.\d{1,3}){3}(\*/\d+|\.\*)?$"
        domain_pattern = r"^([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}$"

        # IP规则验证
        if re.match(ip_pattern, rule):
            return True

        # 通配符域名规则验证
        if "*" in rule:
            # 转换为正则表达式
            transformed_rule = rule.replace(".", r"\.").replace("*", r".*")
            print(f"转换后的通配符规则为正则：{transformed_rule}")
            try:
                re.compile(transformed_rule)
                return True
            except re.error as e:
                print(f"正则表达式无效：{e}")
                return False

        # 普通域名规则验证
        if re.match(domain_pattern, rule):
            return True

        # CIDR格式验证
        try:
            ipaddress.IPv4Network(rule, strict=False)
            return True
        except ValueError:
            return False

        return False

    def show_blacklist(self):
        print(colorize("\n当前黑名单规则：", "blue"))
        if not self.rules:
            print(colorize("无规则", "yellow"))
        else:
            for idx, rule in enumerate(self.rules, 1):
                print(f"{idx}. {rule}")

    def add_rule(self):
        new_rules = input(
            colorize(
                "请输入要添加的规则（多个规则用逗号`,`分隔，分号`;`结束），返回上一级请输入'0'：",
                "dark_blue",
            )
        ).strip()

        new_rules = (
            new_rules.replace("，", ",").replace("；", ";").rstrip(";").split(",")
        )

        if new_rules[0] == "0":  # 用户输入 '0' 返回上一级
            return

        invalid = []
        added = []

        for rule in new_rules:
            rule = rule.strip()
            if rule in self.rules:
                print(colorize(f"规则 {rule} 已存在，跳过。", "yellow"))
            elif self.validate_rule(rule):
                self.rules.append(rule)
                added.append(rule)
            else:
                invalid.append(rule)

        self.save_blacklist()

        if added:
            print(colorize("已添加以下新规则：", "green"))
            for rule in added:
                print(colorize(rule, "green"))
        if invalid:
            print(colorize("以下规则无效，未添加：", "red"))
            for rule in invalid:
                print(colorize(rule, "red"))

    def remove_rule(self):
        self.show_blacklist()
        to_remove = input(
            colorize(
                "请输入要删除的规则序号（多个规则用逗号`,`分隔，分号`;`结束），返回上一级请输入'0'：",
                "dark_blue",
            )
        ).strip()

        to_remove = (
            to_remove.replace("，", ",").replace("；", ";").rstrip(";").split(",")
        )
        if to_remove[0] == "0":
            return

        to_remove = [seq.strip() for seq in to_remove if seq.strip()]
        invalid = []
        removed = []

        for idx in sorted(map(int, to_remove), reverse=True):
            if 1 <= idx <= len(self.rules):
                removed.append(self.rules.pop(idx - 1))
            else:
                invalid.append(idx)

        self.save_blacklist()

        if removed:
            print(colorize("已删除以下规则：", "green"))
            for rule in removed:
                print(colorize(rule, "green"))
        if invalid:
            print(colorize("以下序号无效，未删除：", "red"))
            for idx in invalid:
                print(colorize(str(idx), "red"))

    def change_rule(self):
        self.show_blacklist()
        while True:
            idx_input = input(
                colorize("请输入要修改的规则序号，返回上一级请输入'0'：", "dark_blue")
            ).strip()
            if idx_input == "0":
                return
            if not idx_input.isdigit():
                print(colorize("无效输入，请输入有效的序号。", "red"))
                continue

            idx = int(idx_input) - 1
            if 0 <= idx < len(self.rules):
                old_rule = self.rules[idx]
                new_rule = input(f"当前规则为 {old_rule}，请输入新的规则：").strip()
                if new_rule:
                    if self.validate_rule(new_rule):
                        if new_rule in self.rules and new_rule != old_rule:
                            print(
                                colorize(
                                    f"规则 {new_rule} 已存在，无法重复添加。", "yellow"
                                )
                            )
                        else:
                            self.rules[idx] = new_rule
                            self.save_blacklist()
                            print(
                                colorize(
                                    f"已更改规则：{old_rule} -> {new_rule}", "green"
                                )
                            )
                    else:
                        print(colorize("新规则无效。", "red"))
                else:
                    print(colorize("新规则不能为空。", "red"))
                break
            else:
                print(colorize("序号无效，请重新输入。", "red"))

    def run(self):
        while True:
            print(colorize("\n规则管理：", "yellow"))
            print(colorize("1. 查看规则", "yellow"))
            print(colorize("2. 增加规则", "yellow"))
            print(colorize("3. 删除规则", "yellow"))
            print(colorize("4. 修改规则", "yellow"))
            print(colorize("0. 退出", "yellow"))
            choice = input(colorize("请选择操作：", "dark_blue"))

            if choice == "1":
                self.show_blacklist()
            elif choice == "2":
                self.add_rule()
            elif choice == "3":
                self.remove_rule()
            elif choice == "4":
                self.change_rule()
            elif choice == "0":
                print(colorize("退出规则管理模块。", "green"))
                break
            else:
                print(colorize("无效选择，请重新输入。", "red"))


if __name__ == "__main__":
    manager = RuleManager()
    manager.run()
