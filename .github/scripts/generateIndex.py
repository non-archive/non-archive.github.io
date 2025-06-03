import os
from pathlib import Path

def generateIndex(path, files, folders):

    html_header = """
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
                :hover.folder{
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

    path_real = str(path).replace("../../", "/")
    path_view = str(path).replace("../../", "/").replace("_github", ".github").replace("_git", ".git")

    html_folders = '\n'.join([f"""
                            <a class="folder" href="{path_real + "/" + folder.replace(".github", "_github").replace(".git", "_git")}">
                                <p>{"/" +folder}</p>
                            </a>
                            """ for folder in folders if folder != ".git"])

    html_body = f"""
    <h1>{path_view.replace("/files", "/")}</h1>
    <div class="files">
    <a class="folder" href="{str(Path(path_real).parent)}"><p>..back</p></a>
        {html_folders}
    </div>
"""

    html_footer = """
        </body>
    </html>
    """

    html_content = html_header + html_body + html_footer

    path_index = os.path.join(path, "index.html")

    with open(path_index, "w", encoding="utf-8") as archivo:
        archivo.write(html_content)