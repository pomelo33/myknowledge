import os
import yaml

# 需要把web和Container下的所有md转换成Jekyll格式，带front matter
# 并复制到 jekyll/notes/ 路径下对应结构，方便Jekyll编译

SOURCE_DIRS = ["web", "Container"]
DEST_ROOT = "jekyll/notes"

def gen_front_matter(title, tags=None):
    data = {"title": title}
    if tags:
        data["tags"] = tags
    return "---\n" + yaml.dump(data, allow_unicode=True) + "---\n\n"

def normalize_title(filename):
    # 用文件名生成标题，去掉扩展名，替换 - 和 _ 为空格，首字母大写
    base = os.path.splitext(filename)[0]
    title = base.replace("-", " ").replace("_", " ").title()
    return title

def process_file(src_path, dest_path):
    with open(src_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 判断是否已有front matter
    if content.startswith("---"):
        print(f"跳过已有 Front Matter: {src_path}")
        return

    # 从路径取tag（目录名）标签
    rel_path = os.path.relpath(src_path)
    parts = rel_path.split(os.sep)
    # 取除文件名外的目录名当tags
    tags = [p.lower() for p in parts[1:-1]]

    title = normalize_title(os.path.basename(src_path))
    front_matter = gen_front_matter(title, tags)

    new_content = front_matter + content

    # 确保目录存在
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(new_content)

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