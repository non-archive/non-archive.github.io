class_name Archivo

# Añadir al diccionario FILE_TYPES en archivo.gd:
const FILE_TYPES = {
	"txt": "text", "json": "text", "csv": "text", "md": "text",
	"png": "image", "jpg": "image", "jpeg": "image", "webp": "image", 
	"svg": "image", "bmp": "image",
	"wav": "audio", "mp3": "audio", "ogg": "audio",
	"ogv": "video",  # <-- SOLO .ogv ESTÁ SOPORTADO EN GODOT 4
	"glb": "model", "gltf": "model", "obj": "model", "blend": "model", "fbx": "model",
	"ttf": "font", "otf": "font", "woff": "font", "woff2": "font",
	"zip": "archive", "rar": "archive", "7z": "archive",
	"doc": "document", "docx": "document", "pdf": "document",
	"xls": "spreadsheet", "xlsx": "spreadsheet",
	"import": "import", "html": "html"
}

var filepath: String
var real_path: String
var file_type: String

func _init(uid_path: String):
	filepath = uid_path
	real_path = _get_real_path(uid_path)
	file_type = _identify_file_type(real_path)

func _get_real_path(uid_path: String) -> String:
	if uid_path.begins_with("uid://"):
		return ResourceUID.get_id_path(ResourceUID.text_to_id(uid_path))
	return uid_path

func _identify_file_type(file: String) -> String:
	var extension = file.get_extension().to_lower()
	return FILE_TYPES.get(extension, "unknown")

# Actualizar el método get_mesh() para incluir video:
func get_mesh() -> Node3D:
	if file_type == "image":
		return _crear_imagen()
	elif file_type == "audio":
		return _crear_audio()
	elif file_type == "video":  # <-- AÑADIR ESTA CONDICIÓN
		return _crear_video()
	else:
		return _crear_generico()

func _crear_video() -> Node3D:
	print("🎬 [DEBUG] _crear_video() - Inicio")
	print("🎬 [DEBUG] filepath: ", filepath)
	
	# Usar la clase Video para crear y configurar la escena
	var video_factory = Video.new()
	
	# 🔊 OPCIÓN: Cambiar 'false' por 'true' para habilitar audio 3D
	# var video_visualization = video_factory.crear_escena_video(filepath, true)  # CON audio 3D
	var video_visualization = video_factory.crear_escena_video(filepath, true)  # SIN audio 3D (por defecto)
	
	if video_visualization:
		video_visualization.set_meta("es_contenido_generado", true)
		print("✅ [DEBUG] VideoVisualization creado correctamente")
	else:
		print("❌ [DEBUG] Error creando VideoVisualization, usando genérico")
		return _crear_generico()
	
	# Limpiar la factory (no la necesitamos en el árbol)
	video_factory.queue_free()
	
	print("🎬 [DEBUG] _crear_video() - Fin, retornando: ", video_visualization)
	return video_visualization

func _crear_imagen() -> Node3D:
	print("🖼️ [DEBUG] _crear_imagen() - Inicio")
	print("🖼️ [DEBUG] filepath: ", filepath)
	
	# Usar la clase Imagen para crear y configurar la escena
	var imagen_factory = Imagen.new()
	var imagen_visualization = imagen_factory.crear_escena_imagen(filepath)
	
	if imagen_visualization:
		imagen_visualization.set_meta("es_contenido_generado", true)
		print("✅ [DEBUG] ImageVisualization creado correctamente")
	else:
		print("❌ [DEBUG] Error creando ImageVisualization, usando genérico")
		return _crear_generico()
	
	# Limpiar la factory (no la necesitamos en el árbol)
	imagen_factory.queue_free()
	
	print("🖼️ [DEBUG] _crear_imagen() - Fin, retornando: ", imagen_visualization)
	return imagen_visualization

func _crear_audio() -> Node3D:
	print("🎵 [DEBUG] _crear_audio() - Inicio")
	print("🎵 [DEBUG] filepath: ", filepath)
	
	# Usar la clase Audio para crear y configurar la escena
	var audio_factory = Audio.new()
	var audio_visualization = audio_factory.crear_escena_audio(filepath)
	
	if audio_visualization:
		audio_visualization.set_meta("es_contenido_generado", true)
		print("✅ [DEBUG] AudioVisualization creado correctamente")
	else:
		print("❌ [DEBUG] Error creando AudioVisualization, usando genérico")
		return _crear_generico()
	
	# Limpiar la factory (no la necesitamos en el árbol)
	audio_factory.queue_free()
	
	print("🎵 [DEBUG] _crear_audio() - Fin, retornando: ", audio_visualization)
	return audio_visualization

func _crear_generico() -> Node3D:
	var mesh_instance = MeshInstance3D.new()
	mesh_instance.name = real_path
	
	var sphere_mesh = SphereMesh.new()
	sphere_mesh.radius = 0.2
	sphere_mesh.height = 0.4
	
	var material = StandardMaterial3D.new()
	material.albedo_color = Color(1.0, 0.75, 0.0)  # Color ámbar
	sphere_mesh.material = material
	
	mesh_instance.mesh = sphere_mesh
	mesh_instance.set_meta("es_contenido_generado", true)
	
	return mesh_instance
