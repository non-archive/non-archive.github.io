import os
import json
from http.server import SimpleHTTPRequestHandler, HTTPServer
import threading
import webbrowser
import hashlib

FILE_TYPES = {
    "txt": "text", "json": "text", "csv": "text", "md": "text",
    "png": "image", "jpg": "image", "jpeg": "image", "webp": "image", "svg": "image", "bmp": "image",
    "wav": "audio", "mp3": "audio", "ogg": "audio",
    "glb": "model", "gltf": "model", "obj": "model", "blend": "model", "fbx": "model",
    "ttf": "font", "otf": "font", "woff": "font", "woff2": "font",
    "mp4": "video", "webm": "video",
    "zip": "archive", "rar": "archive", "7z": "archive",
    "doc": "document", "docx": "document", "pdf": "document",
    "xls": "spreadsheet", "xlsx": "spreadsheet",
    "html": "html"
}

FOLDER_JSON_NAME = "metadata.json"

def identify_type(filename):
    ext = filename.rsplit('.', 1)[-1].lower() if '.' in filename else ''
    return FILE_TYPES.get(ext, 'unknown')

def get_file_hash(file_path):
    """Calcula un hash del contenido del archivo para identificar duplicados"""
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def scan_directory_graph(base_path):
    """
    Genera una estructura de grafo con nodos y enlaces sin incluir "data" en las rutas
    """
    nodes = []
    links = []
    file_mapping = {}  # para rastrear archivos duplicados: {hash: [(carpeta1, archivo1), (carpeta2, archivo2), ...]}
    
    def collect_nodes_and_files(rel_path="", parent_id=None):
        # Ruta completa para esta carpeta
        full_path = os.path.join(base_path, rel_path)
        
        # Ignorar la carpeta raíz "data" para los IDs
        if rel_path == "":
            # No agregamos el nodo "data"
            # Procesamos directamente sus contenidos
            for entry in sorted(os.listdir(full_path)):
                if entry.startswith(".") or entry == FOLDER_JSON_NAME:
                    continue
                    
                entry_path = os.path.join(full_path, entry)
                
                if os.path.isdir(entry_path):
                    # Procesar subcarpetas del directorio raíz
                    collect_nodes_and_files(entry, None)
            return
        
        # ID de carpeta sin incluir "data/"
        folder_id = rel_path.replace("\\", "/")
        
        # Agregar nodo para esta carpeta
        nodes.append({"id": folder_id})
        
        # Si tiene padre, agregar enlace jerárquico (type 0)
        if parent_id is not None:
            add_link(parent_id, folder_id, 0)
        
        # Verificar si existe metadata.json previo
        json_path = os.path.join(full_path, FOLDER_JSON_NAME)
        existing_data = {}
        if os.path.exists(json_path):
            try:
                with open(json_path, "r", encoding="utf-8") as f:
                    existing_data = json.load(f)
            except:
                existing_data = {}  # Si hay error al leer el archivo, tratarlo como nuevo
        
        # Mapeo de archivos existentes para mantener datos personalizados
        existing_files_map = {}
        if "files" in existing_data:
            for file_info in existing_data["files"]:
                if "name" in file_info:
                    existing_files_map[file_info["name"]] = file_info
        
        # Recopilar archivos en esta carpeta
        folder_files = []
        subfolders = []
        
        for entry in sorted(os.listdir(full_path)):
            if entry.startswith(".") or entry == FOLDER_JSON_NAME:
                continue
                
            entry_path = os.path.join(full_path, entry)
            entry_rel = os.path.join(rel_path, entry)
            
            if os.path.isdir(entry_path):
                # Es un directorio
                subfolders.append(entry)
                # Procesar recursivamente la subcarpeta
                collect_nodes_and_files(entry_rel, folder_id)
            else:
                # Es un archivo
                file_info = {
                    "type": identify_type(entry),
                    "name": entry
                }
                
                # Preservar propiedades personalizadas del archivo si existía previamente
                if entry in existing_files_map:
                    prev_file = existing_files_map[entry]
                    # Preservar el campo "data" si existe
                    if "data" in prev_file:
                        file_info["data"] = prev_file["data"]
                    # Preservar otros campos que puedan existir (excepto type y name que ya se establecieron)
                    for key, value in prev_file.items():
                        if key not in ["type", "name", "link"] and key not in file_info:
                            file_info[key] = value
                
                folder_files.append(file_info)
                
                # Calcular hash del archivo para detectar duplicados
                try:
                    file_hash = get_file_hash(entry_path)
                    if file_hash not in file_mapping:
                        file_mapping[file_hash] = []
                    # Guardar tupla (folder_id, file_name) para después agregar enlaces
                    file_mapping[file_hash].append((folder_id, entry))
                except:
                    pass  # Ignorar errores al leer archivos
        
        # Crear archivo metadata.json para esta carpeta
        folder_data = {"path": "/" + full_path, "files": folder_files}
        if subfolders:
            folder_data["subfolders"] = [{"name": subfolder} for subfolder in subfolders]
        
        # Guardar el metadata.json (sin los enlaces aún)
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(folder_data, f, indent=2, ensure_ascii=False)
    
    def add_link(source, target, link_type):
        """Agrega un enlace evitando duplicados y enlaces inversos"""
        # Verificar si ya existe este enlace o su inverso (para type 1)
        for link in links:
            if (link["source"] == source and link["target"] == target and link["type"] == link_type) or \
               (link_type == 1 and link["source"] == target and link["target"] == source and link["type"] == 1):
                return
        
        links.append({
            "source": source,
            "target": target,
            "type": link_type
        })
    
    def update_metadata_links():
        """Actualiza los archivos metadata.json con enlaces a archivos duplicados"""
        # Procesar los hashes de archivos para encontrar duplicados
        for file_hash, occurrences in file_mapping.items():
            if len(occurrences) > 1:
                # Hay al menos dos archivos con el mismo contenido
                for folder_id, file_name in occurrences:
                    folder_path = os.path.join(base_path, folder_id)
                    json_path = os.path.join(folder_path, FOLDER_JSON_NAME)
                    
                    # Leer el metadata.json de esta carpeta
                    try:
                        with open(json_path, "r", encoding="utf-8") as f:
                            folder_data = json.load(f)
                            
                        # Buscar y actualizar el archivo en el metadata
                        for file_info in folder_data.get("files", []):
                            if file_info.get("name") == file_name:
                                # Añadir enlaces a todas las otras ubicaciones
                                links = []
                                for other_folder, other_file in occurrences:
                                    if other_folder != folder_id:  # No enlazar consigo mismo
                                        links.append(other_folder)
                                
                                if links:
                                    # Si hay otros archivos idénticos, agregar el primer enlace
                                    file_info["link"] = links[0]
                                
                                break
                        
                        # Guardar el metadata actualizado
                        with open(json_path, "w", encoding="utf-8") as f:
                            json.dump(folder_data, f, indent=2, ensure_ascii=False)
                    except Exception as e:
                        print(f"Error al actualizar {json_path}: {str(e)}")
    
    # Comenzar el escaneo desde la raíz
    collect_nodes_and_files()
    
    # Crear enlaces para archivos duplicados (type 1)
    for file_hash, occurrences in file_mapping.items():
        if len(occurrences) > 1:
            # Hay al menos dos carpetas con este archivo
            folders_with_file = [folder_id for folder_id, _ in occurrences]
            for i in range(len(folders_with_file)):
                for j in range(i+1, len(folders_with_file)):
                    add_link(folders_with_file[i], folders_with_file[j], 1)
    
    # Actualizar los metadata.json con los enlaces
    update_metadata_links()
    
    return {"nodes": nodes, "links": links}

# Generar estructura.json con el formato de grafo
estructura_grafo = scan_directory_graph("data")
with open("estructura.json", "w", encoding="utf-8") as f:
    json.dump(estructura_grafo, f, indent=2, ensure_ascii=False)
print("✅ estructura.json generado como grafo sin incluir 'data'")

# Servidor HTTP en la raíz
PORT = 1312
def abrir_navegador():
    webbrowser.open(f"http://localhost:{PORT}/")

def iniciar_servidor():
    handler = SimpleHTTPRequestHandler
    httpd = HTTPServer(("localhost", PORT), handler)
    print(f"🌐 Servidor iniciado en http://localhost:{PORT}")
    httpd.serve_forever()

threading.Timer(1, abrir_navegador).start()
iniciar_servidor()