import os
import json

BASE_DIR = "note"
OUTPUT_FILE = "_sidebar.md"
MAP_FILE = "name_map.json"

# 设置忽略的文件/目录关键字（全部小写）
IGNORE_DIR_KEYWORDS = ["app","docs","scripts"]
IGNORE_FILE_KEYWORDS = ["test", "template"]

# 加载中文映射
with open(MAP_FILE, "r", encoding="utf-8") as f:
    name_map = json.load(f)

def format_display_name(name):
    name_no_ext = os.path.splitext(name)[0]
    return name_map.get(name_no_ext.lower(), name_no_ext.replace("-", " ").title())

def should_ignore_dir(dir_name):
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
            if os.path.isdir(full_path):
                if should_ignore_dir(entry):
                    continue
                display_name = format_display_name(entry)
                lines.append("  " * indent + f"- {display_name}")
                walk(full_path, indent + 1)
            elif entry.endswith(".md"):
                if should_ignore_file(entry):
                    continue
                rel_path = full_path.replace("\\", "/")
                display_name = format_display_name(entry)
                lines.append("  " * indent + f"- [{display_name}]({rel_path})")

    walk(BASE_DIR)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"✅ 已生成带分组结构的 {OUTPUT_FILE}，并应用忽略规则")

if __name__ == "__main__":
    generate_sidebar()
