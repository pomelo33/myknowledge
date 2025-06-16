import os
import shutil
import yaml

# 源笔记目录列表
SOURCE_DIRS = ["web", "Container"]
# Jekyll 目标目录
DEST_ROOT = "docs/notes"

def gen_front_matter(title, tags=None):
    data = {"title": title}
    if tags:
        data["tags"] = tags
    # 使用 allow_unicode 保证中文不会被转义成\u编码
    return "---\n" + yaml.dump(data, allow_unicode=True) + "---\n\n"

def normalize_title(filename):
    # 去掉扩展名，替换 -, _ 为 空格，首字母大写
    base = os.path.splitext(filename)[0]
    title = base.replace("-", " ").replace("_", " ").title()
    return title

def copy_assets(src_dir, dest_dir):
    # 支持复制多个资源文件夹，比如 img, images, assets
    asset_folders = ["img", "images", "assets","docs"]
    for folder in asset_folders:
        src_path = os.path.join(src_dir, folder)
        dest_path = os.path.join(dest_dir, folder)
        if os.path.exists(src_path):
            if os.path.exists(dest_path):
                shutil.rmtree(dest_path)
            shutil.copytree(src_path, dest_path)
            print(f"复制资源目录: {src_path} -> {dest_path}")

# def process_file(src_path, dest_path):
#     with open(src_path, "r", encoding="utf-8") as f:
#         content = f.read()

#     # 如果已经有 Front Matter，则跳过添加，直接复制文件
#     if content.startswith("---"):
#         print(f"跳过已有 Front Matter 的文件: {src_path}")
#         # 仍然复制图片资源
#         src_dir = os.path.dirname(src_path)
#         dest_dir = os.path.dirname(dest_path)
#         copy_assets(src_dir, dest_dir)

#         os.makedirs(dest_dir, exist_ok=True)
#         shutil.copy2(src_path, dest_path)
#         return

#     # 生成标题
#     title = normalize_title(os.path.basename(src_path))

#     # 根据路径自动生成标签，取除文件名外的路径段作为标签，全部小写
#     rel_path = os.path.relpath(src_path)
#     parts = rel_path.split(os.sep)
#     # 移除文件名 和 1级目录（web 或 Container），仅保留中间路径作为标签
#     tags = [p.lower() for p in parts[1:-1]] if len(parts) > 2 else []

#     front_matter = gen_front_matter(title, tags)

#     new_content = front_matter + content

#     # 确保目标目录存在
#     os.makedirs(os.path.dirname(dest_path), exist_ok=True)

#     # 写入新文件
#     with open(dest_path, "w", encoding="utf-8") as f:
#         f.write(new_content)

#     # 复制图片文件夹
#     src_dir = os.path.dirname(src_path)
#     dest_dir = os.path.dirname(dest_path)
#     copy_assets(src_dir, dest_dir)

#     print(f"转换并生成: {dest_path}")
def process_file(src_path, dest_path):
    with open(src_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 省略已有front matter的处理...

    # 生成标题
    title = normalize_title(os.path.basename(src_path))

    # 取文件名去扩展名部分
    filename = os.path.splitext(os.path.basename(src_path))[0]

    # 按下划线分割，取第一个作为标签
    first_tag = filename.split("_")[0].lower()

    tags = [first_tag]

    front_matter = gen_front_matter(title, tags)

    new_content = front_matter + content

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(new_content)

    # 复制图片资源等
    src_dir = os.path.dirname(src_path)
    dest_dir = os.path.dirname(dest_path)
    copy_assets(src_dir, dest_dir)

    print(f"转换并生成: {dest_path}")

def walk_and_convert():
    for src_root in SOURCE_DIRS:
        for dirpath, _, files in os.walk(src_root):
            for file in files:
                if file.endswith(".md"):
                    src_file = os.path.join(dirpath, file)
                    # 目标路径替换根目录 src_root-> DEST_ROOT/src_root
                    rel_path = os.path.relpath(src_file, src_root)
                    dest_file = os.path.join(DEST_ROOT, src_root, rel_path)
                    process_file(src_file, dest_file)

if __name__ == "__main__":
    walk_and_convert()
