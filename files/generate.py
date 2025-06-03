# inspired in distribusi

def generar_index():
    
    html_content = """
    <!DOCTYPE html>
    <html lang="es">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Archivos</title>
        </head>
        <body>
            <h1>Archivos</h1>
        </body>
    </html>
    """
    
    with open("files/index.html", "w", encoding="utf-8") as archivo:
        archivo.write(html_content)
    
    print("✅ index.html generado correctamente!")

if __name__ == "__main__":
    generar_index()