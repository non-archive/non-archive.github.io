import os
from pathlib import Path
from typing import List
from generateTags import *

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
      html,
      body {
        height: 100%;
        width: 100%;
        margin: 0px;
      }
      main {
        display: flex;
        flex-direction: column;
        height: 100%;
        margin: 0 50px;
      }
      .files {
        display: flex;
        gap: 1em;
        flex-wrap: wrap;
        margin-bottom: 1em;
      }
      .main-files {
        flex-grow: 1;
        gap: 4em;
      }
      .folder {
        padding: 0.2em 1.2em;
        padding-bottom: 2em;
        border: 1px;
        border-color: black;
        border-style: solid;
        border-radius: 0.2em 0.2em 0 0;
        background-color: rgb(255, 245, 106);
        height: fit-content;
      }
      .folder:hover {
        background-color: rgb(197, 189, 82);
      }
      img {
        max-width: 400px;
      }
      .file-name {
        margin: 0px;
        display: block;
      }
      .footer {
        text-align: end;
      }
      .text-content {
        max-width: 600px;
        max-height: 600px;
        overflow: auto;
      }
      model-viewer {
        width: 600px;
        height: 600px;
      }
      iframe {
        width: 600px;
        height: 600px;
      }
      /* Extra small devices (phones, 600px and down) */
      @media only screen and (max-width: 800px) {
        .folder {
          padding: 0 0.3em;
        }
        .files {
          gap: 0.5em;
        }
        h1 {
          font-size: x-large;
        }
        main {
          margin: 0 10px;
        }
        iframe {
          width: 100%;
          height: 400px;
        }
        .iframe-div{
            width: 100%;
        }
        img{
          width: 100%;
          height: auto;
        }
        .image-div{
          width: 100%;
        }
        model-viewer {
        width: 100%;
        height: 400px;
      }
      .model-div{
        width: 100%;
      }
      }
    </style>
        </head>
        <body>
        <main>
    """

# Returns the HTML footer section.
def get_html_footer() -> str:
    return """
        <div class="footer"><p>inspired by Distribusi</p></div>
        </main>
        <script type="module" src="https://ajax.googleapis.com/ajax/libs/model-viewer/4.0.0/model-viewer.min.js"></script>
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
def generate_html_body(path: Path, path_real: str, path_view: str, files: List[str], folders: List[str]) -> str:
    # Generate back button
    parent_path = str(Path(path_real).parent)
    back_button = f'<a class="folder" href="{parent_path}"><p>...back</p></a>'
    
    # Generate folder links
    folder_links = generate_folder_links(path_real, folders)
    files_tags = generateTags(files, path_view.replace("/files/", "/"))
    
    # Clean path for title display
    title_path = path_view.replace("/files/", "/").replace("/files", "/")
    
    return f"""
        <h1>{title_path}</h1>
            <div class="files">
                {back_button}
                {folder_links}
            </div>
            <div class="files main-files">
                {files_tags}
            </div>
        """

# Generates an HTML index file for the given directory.
def generateIndex(path: Path, files: List[str], folders: List[str]) -> None:
    
    # Convert paths for different purposes
    path_real = normalize_path_for_url(str(path))
    path_view = normalize_path_for_display(str(path))
    
    # Generate HTML components
    html_header = get_html_header()
    html_body = generate_html_body(path, path_real, path_view, files, folders)
    html_footer = get_html_footer()
    
    # Combine all HTML content
    html_content = html_header + html_body + html_footer
    
    # Write to index.html file
    index_path = path / "index.html"
    with open(index_path, "w", encoding="utf-8") as file:
        file.write(html_content)