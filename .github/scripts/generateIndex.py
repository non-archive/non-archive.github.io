import os
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
                    padding: 1rem;
                    border: 1px;
                    border-color: black;
                }
                .folders {
                    display: flex;

                }
            </style>
        </head>
        <body>
    """

    path_real = str(path)
    path_view = str(path).replace("../../", "/")

    html_folders = '\n'.join([f"""
                            <a class="folder" href="{path_real + "/" + folder.replace(".github", "_github").replace(".git", "_git")}">
                                <p>{path_view + "/" + folder}</p>
                            </a>
                            """ for folder in folders])

    html_body = f"""
    <h1>{path_view}</h1>
    <div class="folders">
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