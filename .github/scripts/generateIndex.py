import os
from pathlib import Path
from typing import List

# Returns the HTML header with embedded CSS styles.
def get_html_header() -> str:
    return """
    <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>📁</title>
            <style>
                body {
                    margin: 50px;
                }
                .folder {
                    padding: 0.2em 1.2em;
                    padding-bottom: 2em;
                    border: 1px;
                    border-color: black;
                    border-style: solid;
                    border-radius: 0.2em 0.2em 0 0;
                    background-color: rgb(255, 245, 106);
                }
                .folder:hover {
                    background-color: rgb(197, 189, 82);
                }
                .files {
                    display: flex;
                    gap: 1.0em;
                    flex-wrap: wrap;
                }
            </style>
        </head>
        <body>
    """

# Returns the HTML footer section.
def get_html_footer() -> str:
    return """
        </body>
    </html>
    """

# Normalizes a path for URL usage by replacing special directories.
def normalize_path_for_url(path: str) -> str:
    return path.replace("../../", "/").replace(".github", "_github").replace(".git", "_git")

# Normalizes a path for display purposes.
def normalize_path_for_display(path: str) -> str:
    return path.replace("../../", "/").replace("_github", ".github").replace("_git", ".git")

# Checks if a folder should be excluded from the index.
def should_exclude_folder(folder_name: str) -> bool:
    excluded_folders = {"files", ".git", "__pycache__"}
    return folder_name in excluded_folders

# Generates HTML links for folders.
def generate_folder_links(path_real: str, folders: List[str]) -> str:

    folder_links = []
    
    for folder in folders:
        if not should_exclude_folder(folder):
            folder_url = normalize_path_for_url(folder)
            folder_link = f"""
            <a class="folder" href="{path_real}/{folder_url}">
                <p>/{folder}</p>
            </a>
            """

            folder_links.append(folder_link)
    
    return '\n'.join(folder_links)

# Generates the main HTML body content.
def generate_html_body(path: Path, path_real: str, path_view: str, folders: List[str]) -> str:
    # Generate back button
    parent_path = str(Path(path_real).parent)
    back_button = f'<a class="folder" href="{parent_path}"><p>..back</p></a>'
    
    # Generate folder links
    folder_links = generate_folder_links(path_real, folders)
    
    # Clean path for title display
    title_path = path_view.replace("/files", "/")
    
    return f"""<h1>{title_path}</h1>
<div class="files">
    {back_button}
    {folder_links}
</div>"""

# Generates an HTML index file for the given directory.
def generateIndex(path: Path, files: List[str], folders: List[str]) -> None:
    
    # Convert paths for different purposes
    path_real = normalize_path_for_url(str(path))
    path_view = normalize_path_for_display(str(path))
    
    # Generate HTML components
    html_header = get_html_header()
    html_body = generate_html_body(path, path_real, path_view, folders)
    html_footer = get_html_footer()
    
    # Combine all HTML content
    html_content = html_header + html_body + html_footer
    
    # Write to index.html file
    index_path = path / "index.html"
    with open(index_path, "w", encoding="utf-8") as file:
        file.write(html_content)