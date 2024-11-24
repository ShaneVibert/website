# 1. Imports at the top
import os
import shutil
from gencontent import generate_page


# 2. Function definitions
def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    # List all entries in the content directory
    for entry in os.listdir(dir_path_content):
        # Create full path
        entry_path = os.path.join(dir_path_content, entry)

        # If it's a directory, recurse into it
        if os.path.isdir(entry_path):
            # Create the corresponding directory in public
            relative_path = os.path.relpath(entry_path, dir_path_content)
            new_dest_path = os.path.join(dest_dir_path, relative_path)
            os.makedirs(new_dest_path, exist_ok=True)

            # Recurse into subdirectory
            generate_pages_recursive(entry_path, template_path, new_dest_path)

        # If it's a markdown file, generate the HTML
        elif entry.endswith('.md'):
            # Get the output path
            relative_path = os.path.relpath(entry_path, dir_path_content)
            output_path = os.path.join(dest_dir_path, relative_path.replace('.md', '.html'))

            # Create the directory if it doesn't exist
            os.makedirs(os.path.dirname(output_path), exist_ok=True)

            # Generate the page
            generate_page(entry_path, template_path, output_path)


def copy_files_recursive(src, dst):
    if not os.path.exists(dst):
        os.makedirs(dst)
    for item in os.listdir(src):
        src_item = os.path.join(src, item)
        dst_item = os.path.join(dst, item)
        if os.path.isdir(src_item):
            copy_files_recursive(src_item, dst_item)
        else:
            shutil.copy2(src_item, dst_item)


# Get the base directory (one level up from the script location)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main():
    # Define paths relative to BASE_DIR
    dir_path_content = os.path.join(BASE_DIR, "content")
    dir_path_public = os.path.join(BASE_DIR, "public")
    dir_path_static = os.path.join(BASE_DIR, "static")
    path_template = os.path.join(BASE_DIR, "template.html")

    # Delete old public directory if it exists
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)

    # Create a fresh public directory
    os.makedirs(dir_path_public)

    # Generate all pages recursively
    generate_pages_recursive(dir_path_content, path_template, dir_path_public)


if __name__ == "__main__":
    main()