#!/usr/bin/env python3
import os, re, json, datetime, nbformat
from markdown import markdown
from nbconvert import HTMLExporter
from jinja2 import Template

TEMPLATE_PATH = "templates/post_template.html"
FOLDERS = ["blogs", "projects"]

def load_template():
    with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
        return Template(f.read())

def extract_metadata(text):
    title_match = re.search(r'^#\s+(.+)', text, re.MULTILINE)
    title = title_match.group(1).strip() if title_match else "Untitled"
    date_match = re.search(r'^date:\s*(.+)$', text, re.MULTILINE)
    date = date_match.group(1).strip() if date_match else datetime.date.today().isoformat()
    return title, date

def convert_md_to_html(md_path):
    with open(md_path, "r", encoding="utf-8") as f:
        text = f.read()
    title, date = extract_metadata(text)
    html_content = markdown(text, extensions=["fenced_code", "tables", "codehilite"])
    return title, date, html_content

def convert_notebook_to_html(nb_path):
    nb = nbformat.read(nb_path, as_version=4)
    exporter = HTMLExporter()
    exporter.exclude_input_prompt = True
    exporter.exclude_output_prompt = True
    exporter.template_name = "classic"
    (body, resources) = exporter.from_notebook_node(nb)
    title = os.path.splitext(os.path.basename(nb_path))[0].replace("_", " ").title()
    date = datetime.date.today().isoformat()
    return title, date, body

def build_html(src_path, template):
    ext = os.path.splitext(src_path)[1]
    if ext in [".md", ".qmd"]:
        title, date, html_content = convert_md_to_html(src_path)
    elif ext == ".ipynb":
        title, date, html_content = convert_notebook_to_html(src_path)
    else:
        return None

    rendered = template.render(
        title=title,
        date=date,
        content=html_content,
        year=datetime.date.today().year,
    )
    out_path = src_path.rsplit(".", 1)[0] + ".html"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(rendered)
    return {"title": title, "url": out_path.replace("\\", "/")}

def build_folder(folder):
    print(f"📦 Building {folder}/...")
    template = load_template()
    posts = []
    for fn in os.listdir(folder):
        if fn.endswith((".md", ".qmd", ".ipynb")):
            post = build_html(os.path.join(folder, fn), template)
            if post:
                posts.append(post)
    posts.sort(key=lambda x: x["title"])  # optional: sort by title
    with open(os.path.join(folder, "list.json"), "w", encoding="utf-8") as f:
        json.dump(posts, f, indent=2, ensure_ascii=False)
    print(f"✅ {len(posts)} posts processed in {folder}/")

if __name__ == "__main__":
    for folder in FOLDERS:
        build_folder(folder)
