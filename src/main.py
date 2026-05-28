import os, shutil, sys
from block import Block


def copy_content(src, dst):
    if not os.path.exists(dst):
        os.mkdir(dst)
    for entry in os.listdir(src):
        src_path = os.path.join(src, entry)
        dst_path = os.path.join(dst, entry)
        if os.path.isfile(src_path):
            shutil.copy(src_path, dst_path)
        else:
            copy_content(src_path, dst_path)


def extract_title(markdown):
    for line in markdown.split("\n"):
        if line.startswith("# "):
            return line[2:].strip()
    raise ValueError("No h1 header found in markdown")


def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as f:
        markdown = f.read()
    with open(template_path) as f:
        template = f.read()
    content_html = Block.markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)
    page = template.replace("{{ Title }}", title).replace("{{ Content }}", content_html)
    page = page.replace('href="/', f'href="{basepath}').replace('src="/', f'src="{basepath}')
    dest_dir = os.path.dirname(dest_path)
    if dest_dir:
        os.makedirs(dest_dir, exist_ok=True)
    with open(dest_path, "w") as f:
        f.write(page)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    for entry in os.listdir(dir_path_content):
        src_path = os.path.join(dir_path_content, entry)
        dst_path = os.path.join(dest_dir_path, entry)
        if os.path.isfile(src_path):
            if src_path.endswith(".md"):
                dst_html = dst_path[:-3] + ".html"
                generate_page(src_path, template_path, dst_html, basepath)
        else:
            generate_pages_recursive(src_path, template_path, dst_path, basepath)


if __name__ == "__main__":
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    if os.path.exists("./docs"):
        shutil.rmtree("./docs")
    copy_content("./static", "./docs")
    generate_pages_recursive("./content", "./template.html", "./docs", basepath)
