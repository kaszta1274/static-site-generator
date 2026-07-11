import os
from markdown_blocks import markdown_to_html_node

def extract_title(markdown: str) -> str:
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:]
    raise Exception("No h1 header for the title")

def generate_page(from_path: str, template_path: str, dest_path: str) -> None:
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    markdown = ""
    with open(from_path, "r") as f:
        markdown = f.read()

    template = ""
    with open(template_path, "r") as f:
        template = f.read()

    node = markdown_to_html_node(markdown)
    html = node.to_html()

    title = extract_title(markdown)

    page = template.replace("{{ Title }}", title).replace("{{ Content }}", html)

    dest_directory = os.path.dirname(dest_path)
    if not os.path.exists(dest_directory):
        os.makedirs(dest_directory)

    with open(dest_path, "w") as f:
        f.write(page)


def generate_pages_recursive(dir_path_content: str, template_path: str, dest_dir_path: str) -> None:
    file_entries = os.listdir(dir_path_content)
    for file_entry in file_entries:
        current_input_path = os.path.join(dir_path_content, file_entry)
        generated_page_path = os.path.join(dest_dir_path, file_entry)

        if os.path.isfile(current_input_path):
            generate_page(current_input_path, template_path, generated_page_path.replace(".md", ".html"))
        else:
            generate_pages_recursive(current_input_path, template_path, generated_page_path)