import os
import shutil
import json
from collections import defaultdict

SOURCE_DIRS = ['web', 'containerd']
RESOURCE_DIRS = ['img', 'images', 'docs']
DEST_DIR = 'docs/notes'
DOCS_DIR = 'docs'

def load_title_mapping(json_file):
    with open(json_file, 'r', encoding='utf-8') as f:
        return json.load(f)

def should_copy_file(file_path):
    return file_path.endswith('.md')

def should_copy_dir(dirname):
    return any(d in dirname for d in RESOURCE_DIRS)

def copy_notes(src_root, dst_root, title_map):
    sidebar_lines = []
    readme_structure = defaultdict(
        lambda: defaultdict(
            lambda: defaultdict(list)))  # 一级->二级->三级->[(标题, 路径)]

    for src_dir in SOURCE_DIRS:
        if not os.path.exists(src_dir):
            continue

        for root, dirs, files in os.walk(src_dir):
            rel_path = os.path.relpath(root, src_dir)
            parts = rel_path.split(os.sep) if rel_path != '.' else []

            first = src_dir
            second = parts[0] if len(parts) > 0 else ""
            third = parts[1] if len(parts) > 1 else ""

            # 映射目录名
            first_name = title_map.get("dirs", {}).get(first, first)
            second_name = title_map.get("dirs", {}).get(second, second) if second else ""
            third_name = title_map.get("dirs", {}).get(third, third) if third else ""

            dst_path = os.path.join(DEST_DIR, *filter(None, [first_name, second_name, third_name]))
            os.makedirs(dst_path, exist_ok=True)

            for d in dirs:
                if should_copy_dir(d):
                    shutil.copytree(os.path.join(root, d), os.path.join(dst_path, d), dirs_exist_ok=True)

            for file in files:
                if should_copy_file(file):
                    src_file_path = os.path.join(root, file)
                    dst_file_path = os.path.join(dst_path, file)
                    shutil.copy2(src_file_path, dst_file_path)

                    relative_md_path = os.path.relpath(dst_file_path, DOCS_DIR)
                    web_path = relative_md_path.replace(os.sep, '/')
                    title = title_map.get("titles", {}).get(file, os.path.splitext(file)[0])

                    indent_level = web_path.count('/') - 1
                    sidebar_lines.append(f"{'  ' * indent_level}- [{title}]({web_path})")

                    readme_structure[first_name][second_name][third_name].append((title, web_path))

    return sidebar_lines, readme_structure

def write_docsify_files(sidebar_lines, readme_structure):
    readme_path = os.path.join(DOCS_DIR, 'README.md')
    sidebar_path = os.path.join(DOCS_DIR, '_sidebar.md')

    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write("# 欢迎使用我的笔记站\n\n")
        # f.write("下方是按目录结构整理的笔记列表：\n")

        for first in readme_structure:
            f.write(f"\n## {first}\n")
            for second in readme_structure[first]:
                if second:
                    f.write(f"\n### {second}\n")
                for third in readme_structure[first][second]:
                    if third:
                        f.write(f"\n#### {third}\n")
                    for title, path in readme_structure[first][second][third]:
                        f.write(f"- [{title}]({path})\n")

    with open(sidebar_path, 'w', encoding='utf-8') as f:
        f.write("- [首页](README.md)\n")
        for line in sidebar_lines:
            f.write(f"{line}\n")

def main():
    title_map = load_title_mapping('title_map.json')
    if os.path.exists(DEST_DIR):
        shutil.rmtree(DEST_DIR)
    os.makedirs(DEST_DIR, exist_ok=True)

    sidebar_lines, readme_structure = copy_notes('.', DEST_DIR, title_map)
    write_docsify_files(sidebar_lines, readme_structure)
    print("✅ README.md 已生成三级目录结构，笔记复制完成。")

if __name__ == '__main__':
    main()
