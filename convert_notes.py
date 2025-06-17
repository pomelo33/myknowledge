import os
import shutil
import json
from datetime import datetime
from pathlib import Path

# ====== 配置区域 ======
DST_ROOT = Path("docs/notes")
INDEX_FILE = Path("docs/index.md")
TAG_FILE = Path("docs/tag.md")
TITLE_MAP_FILE = Path("title_map.json")
USE_MTIME = False  # True 表示使用修改时间排序，False 表示创建时间

# 忽略这些目录
IGNORE_DIRS = {"docs", ".git", "__pycache__", ".vscode", ".idea","scripts","app"}

# 图片目录关键词
IMAGE_DIR_NAMES = {"images", "img", "assets","docs"}
# ======================

# 加载标题映射
TITLE_MAP = {}
if TITLE_MAP_FILE.exists():
    with TITLE_MAP_FILE.open("r", encoding="utf-8") as f:
        TITLE_MAP = json.load(f)


def get_note_sources():
    return [d for d in Path(".").iterdir() if d.is_dir() and d.name not in IGNORE_DIRS]


def clean_dst_dir():
    if DST_ROOT.exists():
        shutil.rmtree(DST_ROOT)
    DST_ROOT.mkdir(parents=True)


def copy_notes_from_sources():
    for source_root in get_note_sources():
        for file in source_root.rglob("*"):
            if file.is_file():
                rel_path = file.relative_to(source_root)
                dst_path = DST_ROOT / source_root.name / rel_path
                dst_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(file, dst_path)


def collect_articles():
    articles = []
    for md_file in DST_ROOT.rglob("*.md"):
        try:
            filename = md_file.stem
            title = TITLE_MAP.get(filename, filename)
            tag = filename.split("_")[0]

            stat = md_file.stat()
            time_used = stat.st_mtime if USE_MTIME else stat.st_ctime
            timestamp = datetime.fromtimestamp(time_used)
            rel_path = md_file.relative_to("docs")

            articles.append({
                "title": title,
                "path": rel_path.as_posix(),
                "tags": [tag],
                "created": timestamp,
                "parts": rel_path.parts[1:-1],  # 目录层级：notes/xxx/yyy/xxx.md
            })
        except Exception as e:
            print(f"[⚠️] Error reading {md_file}: {e}")
    return sorted(articles, key=lambda x: x["created"])


def write_index(articles):
    lines = ["# 📚 我的笔记目录", "", "[TOC]", ""]
    current_indent = ""

    def indent(level):
        return "  " * level + "- "

    def build_tree(items):
        tree = {}
        for art in items:
            current = tree
            for part in art["parts"]:
                current = current.setdefault(part, {})
            current.setdefault("__articles__", []).append(art)
        return tree

    def render_tree(tree, depth=0):
        for key, value in sorted(tree.items()):
            if key == "__articles__":
                for art in value:
                    lines.append(indent(depth) + f"[{art['title']}]({art['path']}) - {art['created'].strftime('%Y-%m-%d')}")
            else:
                lines.append(indent(depth) + f"**{key}**")
                render_tree(value, depth + 1)

    tree = build_tree(articles)
    render_tree(tree)

    INDEX_FILE.write_text("\n".join(lines), encoding="utf-8")


def write_tag_index(articles):
    tag_map = {}
    for art in articles:
        for tag in art["tags"]:
            tag_map.setdefault(tag, []).append(art)

    lines = ["# 🏷️ 标签索引", ""]
    for tag in sorted(tag_map):
        lines.append(f"## {tag}")
        for art in tag_map[tag]:
            lines.append(f"- [{art['title']}]({art['path']}) - {art['created'].strftime('%Y-%m-%d')}")
        lines.append("")

    TAG_FILE.write_text("\n".join(lines), encoding="utf-8")

ARCHIVE_FILE = Path("docs/archive.md")

# 文档归档页面
def write_archive_index(articles):
    archive_map = {}
    for art in articles:
        y_m = art["created"].strftime("%Y-%m")
        archive_map.setdefault(y_m, []).append(art)

    lines = ["# 🗃️ 文章归档", ""]
    for y_m in sorted(archive_map.keys(), reverse=True):
        display_time = datetime.strptime(y_m, "%Y-%m").strftime("%Y 年 %m 月")
        lines.append(f"## {display_time}")
        for art in sorted(archive_map[y_m], key=lambda x: x["created"]):
            lines.append(f"- [{art['title']}]({art['path']}) - {art['created'].strftime('%Y-%m-%d')}")
        lines.append("")

    ARCHIVE_FILE.write_text("\n".join(lines), encoding="utf-8")


def main():
    print("📂 清理构建目录...")
    clean_dst_dir()
    print("📥 复制笔记文件中...")
    copy_notes_from_sources()
    print("🧩 收集文章信息...")
    articles = collect_articles()
    print("📄 生成 index.md...")
    write_index(articles)
    print("🏷️ 生成 tag.md...")
    write_tag_index(articles)
    print("✅ 构建完成，共处理文章：", len(articles))
    write_archive_index(articles)
    print("🗃️ 生成 archive.md...")


if __name__ == "__main__":
    main()
