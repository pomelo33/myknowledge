import os
import shutil
from pathlib import Path
import json

SOURCE_DIRS = ['web', 'containerd']
TARGET_DIR = Path('docs/notes')
INDEX_FILE = Path('docs/index.md')
TAG_FILE = Path('docs/tag.md')
TITLE_MAP_FILE = 'title_map.json'  # 存储标题映射的 JSON 文件

# 读取标题映射
def load_title_map():
    if os.path.exists(TITLE_MAP_FILE):
        with open(TITLE_MAP_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

# 提取标签：以 _ 分隔取前半部分
def extract_tag(filename):
    if '_' in filename:
        return filename.split('_')[0]
    return 'untagged'

# 递归复制 md 和 img 资源
def copy_notes():
    all_notes = []
    for src_root in SOURCE_DIRS:
        for root, dirs, files in os.walk(src_root):
            rel_path = os.path.relpath(root, src_root)
            dest_path = TARGET_DIR / rel_path
            os.makedirs(dest_path, exist_ok=True)

            for file in files:
                if file.endswith('.md'):
                    src_file = Path(root) / file
                    dst_file = dest_path / file
                    shutil.copy2(src_file, dst_file)
                    all_notes.append((rel_path, file))
                elif file.lower() in ('images', 'img'):
                    shutil.copytree(Path(root) / file, dest_path / file, dirs_exist_ok=True)
    return all_notes

# 生成 index.md
def generate_index_md(all_notes, title_map):
    lines = ["---", "layout: default", "title: 笔记索引", "---", "# 🗂 笔记索引\n"]
    tree = {}
    for path, file in all_notes:
        title = title_map.get(file, file)
        tree.setdefault(path, []).append((file, title))

    for dir_path in sorted(tree):
        lines.append(f"## {dir_path}/")
        for file, title in sorted(tree[dir_path]):
            link = f"notes/{dir_path}/{file}".replace("\\", "/")
            lines.append(f"- [{title}]({link})")
        lines.append("")
    
    with open(INDEX_FILE, 'w', encoding='utf-8') as f:
        f.write("\n".join(lines))

# 生成 tag.md
def generate_tag_md(all_notes, title_map):
    tag_map = {}
    for path, file in all_notes:
        tag = extract_tag(file)
        title = title_map.get(file, file)
        link = f"notes/{path}/{file}".replace("\\", "/")
        tag_map.setdefault(tag, []).append((title, link))
    
    lines = ["---", "layout: tag", "title: 标签页", "---", "# 🏷 标签\n"]
    for tag in sorted(tag_map):
        lines.append(f"## {tag}")
        for title, link in tag_map[tag]:
            lines.append(f"- [{title}]({link})")
        lines.append("")
    
    with open(TAG_FILE, 'w', encoding='utf-8') as f:
        f.write("\n".join(lines))

if __name__ == '__main__':
    title_map = load_title_map()
    all_notes = copy_notes()
    generate_index_md(all_notes, title_map)
    generate_tag_md(all_notes, title_map)
    print("✅ 构建完成")
