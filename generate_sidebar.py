import os
import json

# 基础设置
BASE_DIR = "note"
OUTPUT_FILE = "_sidebar.md"
MAP_FILE = "name_map.json"

# 加载映射表
with open(MAP_FILE, "r", encoding="utf-8") as f:
    name_map = json.load(f)

def format_display_name(name):
    name_no_ext = os.path.splitext(name)[0]
    return name_map.get(name_no_ext.lower(), name_no_ext.replace("-", " ").title())

def generate_sidebar():
    lines = []

    def walk(dir_path, indent=0):
        entries = sorted(os.listdir(dir_path))
        for entry in entries:
            full_path = os.path.join(dir_path, entry)
            if os.path.isdir(full_path):
                display_name = format_display_name(entry)
                lines.append("  " * indent + f"- {display_name}")
                walk(full_path, indent + 1)
            elif entry.endswith(".md"):
                rel_path = os.path.join(dir_path, entry).replace("\\", "/")
                display_name = format_display_name(entry)
                lines.append("  " * indent + f"- [{display_name}]({rel_path})")

    walk(BASE_DIR)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"✅ 成功生成 {OUTPUT_FILE}")

if __name__ == "__main__":
    generate_sidebar()