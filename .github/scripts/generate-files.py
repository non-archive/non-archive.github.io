import os
import shutil

def generar_index():    
    html_content = """
    <!DOCTYPE html>
    <html lang="es">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>📁 Files</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    text-align: center;
                    margin-top: 100px;
                    background-color: #f0f0f0;
                }
                h1 {
                    color: #333;
                    font-size: 3em;
                }
            </style>
        </head>
        <body>
            <h1>Files</h1>
        </body>
    </html>
    """
    
    # Ruta a la carpeta files/ (dos directorios arriba desde .github/scripts/)
    ruta_files = os.path.join("..", "..", "files")
    
    # Borrar toda la carpeta files/ si existe
    if os.path.exists(ruta_files):
        shutil.rmtree(ruta_files)
        print("🗑️ Carpeta files/ borrada completamente")
    
    # Crear la carpeta files/ de nuevo
    os.makedirs(ruta_files, exist_ok=True)
    print("📁 Carpeta files/ creada")
    
    ruta_index = os.path.join(ruta_files, "index.html")
    
    with open(ruta_index, "w", encoding="utf-8") as archivo:
        archivo.write(html_content)
    
    print("✅ index.html generado correctamente en files/!")

if __name__ == "__main__":
    generar_index()