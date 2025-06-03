import os
def generateIndex(ruta, files, folders):

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
            </style>
        </head>
        <body>
    """

    html_folders = []

    for folder in folders:
        html_folders.append(f"""
        <a href="{folder}">{folder}</a>
        """)

    html_body = f"""
    <h1>{str(ruta).replace("../../", "/")}</h1>
    <div>
    
    </div>
"""

    html_footer = """
        </body>
    </html>
    """

    html_content = html_header + html_body + html_footer

    ruta_index = os.path.join(ruta, "index.html")

    with open(ruta_index, "w", encoding="utf-8") as archivo:
        archivo.write(html_content)