import os
import shutil
import markdown
from collections import defaultdict

WEB_DIR = 'web'
DOCS_DIR = 'docs'
INDEX_PATH = os.path.join(DOCS_DIR, 'index.md')
TAG_PATH = os.path.join(DOCS_DIR, 'tag.md')

def get_all_md_files():
    md_files = []
    for root, _, files in os.walk(WEB_DIR):
        for file in files:
            if file.endswith('.md'):
                md_files.append(os.path.join(root, file))
    return md_files

def copy_md_and_assets(md_path):
    rel_path = os.path.relpath(md_path, WEB_DIR)
    dst_path = os.path.join(DOCS_DIR, rel_path)
    os.makedirs(os.path.dirname(dst_path), exist_ok=True)
    shutil.copy2(md_path, dst_path)

    # copy 'images' or 'img' folder if exists
    parent = os.path.dirname(md_path)
    rel_parent = os.path.relpath(parent, WEB_DIR)
    for img_dir in ['images', 'img']:
        img_src = os.path.join(parent, img_dir)
        img_dst = os.path.join(DOCS_DIR, rel_parent, img_dir)
        if os.path.isdir(img_src):
            shutil.copytree(img_src, img_dst, dirs_exist_ok=True)

def get_title_from_md(md_path):
    with open(md_path, encoding='utf-8') as f:
        for line in f:
            if line.strip().startswith('#'):
                return line.strip('#').strip()
    return os.path.basename(md_path)

def extract_tags_from_filename(filename):
    base = os.path.splitext(os.path.basename(filename))[0]
    parts = base.split('_')
    return parts[1:] if len(parts) > 1 else []

def build_index_page(pages):
    lines = ['---', 'layout: default', 'title: 所有笔记', '---\n']
    lines.append('# 所有文章\n')
    for title, path in sorted(pages):
        url = path.replace('.md', '')
        lines.append(f'- [{title}]({url})')
    with open(INDEX_PATH, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

def build_tag_page(tag_map):
    lines = ['---', 'layout: default', 'title: 标签云', '---\n']
    lines.append('# 标签云\n')
    for tag, entries in sorted(tag_map.items()):
        lines.append(f'## {tag}')
        for title, url in sorted(entries):
            lines.append(f'- [{title}]({url})')
        lines.append('')
    with open(TAG_PATH, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

def main():
    md_files = get_all_md_files()
    pages = []
    tag_map = defaultdict(list)

    for md_path in md_files:
        copy_md_and_assets(md_path)

        title = get_title_from_md(md_path)
        rel_path = os.path.relpath(md_path, WEB_DIR)
        url = rel_path.replace('\\', '/')
        pages.append((title, url))

        tags = extract_tags_from_filename(os.path.basename(md_path))
        for tag in tags:
            tag_map[tag].append((title, url))

    build_index_page(pages)
    build_tag_page(tag_map)

if __name__ == '__main__':
    main()
