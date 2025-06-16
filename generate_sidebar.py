import os
import json

BASE_DIR = "note"
OUTPUT_FILE = "_sidebar.md"
HOME_FILE = "HOME.md"
MAP_FILE = "name_map.json"

# 忽略目录关键字（任意包含即可忽略）
IGNORE_DIR_KEYWORDS = ["temp","app","docs","scripts"]

# 忽略文件关键字（任意包含即可忽略）
IGNORE_FILE_KEYWORDS = ["test",  "template"]

# 精确忽略的目录路径列表（相对 BASE_DIR，使用正斜杠）
EXACT_IGNORE_DIR_PATHS = [
    # "k8s/old_version",  # 示例，按需添加
]

# 读取英文转中文映射表
with open(MAP_FILE, "r", encoding="utf-8") as f:
    name_map = json.load(f)

def format_display_name(name):
    name_no_ext = os.path.splitext(name)[0]
    return name_map.get(name_no_ext.lower(), name_no_ext.replace("-", " ").title())

def should_ignore_dir(dir_name, rel_path):
    # 先看是否在精确忽略路径内
    if rel_path in EXACT_IGNORE_DIR_PATHS:
        return True
    # 否则判断是否包含忽略关键字
    return any(keyword in dir_name.lower() for keyword in IGNORE_DIR_KEYWORDS)

def should_ignore_file(file_name):
    name_no_ext = os.path.splitext(file_name)[0].lower()
    return any(keyword in name_no_ext for keyword in IGNORE_FILE_KEYWORDS)

def generate_sidebar():
    lines = []

    def walk(dir_path, indent=0):
        entries = sorted(os.listdir(dir_path))
        for entry in entries:
            full_path = os.path.join(dir_path, entry)
            rel_path = os.path.relpath(full_path, BASE_DIR).replace("\\", "/")

            if os.path.isdir(full_path):
                if should_ignore_dir(entry, rel_path):
                    # print(f"忽略目录: {rel_path}")
                    continue
                display_name = format_display_name(entry)
                lines.append("  " * indent + f"- {display_name}")
                walk(full_path, indent + 1)
            elif entry.endswith(".md"):
                if should_ignore_file(entry):
                    # print(f"忽略文件: {rel_path}")
                    continue
                display_name = format_display_name(entry)
                lines.append("  " * indent + f"- [{display_name}]({rel_path})")

    walk(BASE_DIR)

    content = "\n".join(lines)
    
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    with open(HOME_FILE, "w", encoding="utf-8") as f:
        f.write("# 📚 导航\n\n" + content)

    print(f"✅ 生成成功：{OUTPUT_FILE} 与 {HOME_FILE} 同步完成")

if __name__ == "__main__":
    generate_sidebar()
