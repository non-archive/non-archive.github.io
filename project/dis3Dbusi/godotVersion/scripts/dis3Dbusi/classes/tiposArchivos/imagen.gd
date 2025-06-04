extends Node3D
class_name Imagen

var image_scene_path = "res://scenes/files/image.tscn"
var MAX_SIZE: float = 1.0

# Función principal: crear y configurar una escena de imagen
func crear_escena_imagen(image_path: String) -> Node3D:
	# Cargar la escena de imagen
	var image_scene = ResourceLoader.load(image_scene_path)
	if not image_scene:
		print("❌ Error: No se pudo cargar la escena de imagen en: ", image_scene_path)
		return null
	
	# Instanciar la escena
	var image_instance = image_scene.instantiate()
	
	# IMPORTANTE: Desconectar de la plantilla para evitar superposición
	image_instance.scene_file_path = ""
	
	# Buscar el MeshInstance3D en la escena instanciada
	var mesh_instance = _encontrar_mesh_instance(image_instance)
	
	if not mesh_instance:
		print("⚠️ No se encontró MeshInstance3D en la escena: ", image_scene_path)
		image_instance.queue_free()
		return null
	
	# Cargar la textura de imagen
	var texture = ResourceLoader.load(image_path)
	if not texture:
		print("❌ Error cargando textura de imagen: ", image_path)
		image_instance.queue_free()
		return null
	
	# Configurar el mesh con la textura (creando recursos únicos)
	_configurar_mesh_con_textura(mesh_instance, texture)
	
	print("✅ Imagen cargada correctamente: ", image_path.get_file())
	
	# Hacer que todos los nodos sean locales al árbol (desconectar de plantilla)
	_hacer_nodos_locales(image_instance)
	
	# Ocultar hijos del nodo en el editor (colapsado)
	if Engine.is_editor_hint():
		image_instance.set_display_folded(true)
	
	# Configurar texto de título
	_configurar_texto_titulo(image_instance, image_path)
	
	# Asignar un nombre único a la instancia para evitar conflictos
	var nombre_archivo = _get_real_path(image_path).get_file().get_basename()
	image_instance.name = "Image_" + nombre_archivo + "_" + str(Time.get_unix_time_from_system())
	
	return image_instance

func _configurar_texto_titulo(image_instance: Node3D, image_path: String):
	# Buscar el nodo de texto 3D por nombre
	var titulo_label = image_instance.find_child("TituloImagen", true, false)
	
	# Configurar título del archivo
	if titulo_label and titulo_label is Label3D:
		var nombre_archivo = _get_real_path(image_path).replace("res://", "")
		titulo_label.text = nombre_archivo
		print("✅ Título 3D configurado: ", nombre_archivo)
	else:
		print("⚠️ No se encontró el nodo 'TituloImagen' (Label3D) en la escena")

func _configurar_mesh_con_textura(mesh_instance: MeshInstance3D, texture: Texture2D):
	# Crear material único con la textura
	var material = StandardMaterial3D.new()
	material.albedo_texture = texture
	material.cull_mode = BaseMaterial3D.CULL_DISABLED
	
	# Configurar transparencia si la imagen tiene canal alpha
	if _tiene_canal_alpha(texture):
		material.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA_SCISSOR
		material.no_depth_test = false
		material.shading_mode = BaseMaterial3D.SHADING_MODE_PER_PIXEL
		print("✅ Configurada transparencia alpha scissor para imagen con canal alpha")
	
	# Calcular tamaño apropiado manteniendo proporción
	var size = _calcular_tamaño(texture.get_width(), texture.get_height())
	
	# IMPORTANTE: Duplicar el mesh existente o crear uno nuevo para evitar compartir recursos
	var quad_mesh: QuadMesh
	if mesh_instance.mesh and mesh_instance.mesh is QuadMesh:
		# Duplicar el mesh existente para que cada instancia tenga el suyo propio
		quad_mesh = mesh_instance.mesh.duplicate()
	else:
		# Crear un mesh completamente nuevo
		quad_mesh = QuadMesh.new()
	
	# Configurar el quad con el material único
	quad_mesh.size = size
	quad_mesh.material = material
	
	# Asignar el mesh único a esta instancia
	mesh_instance.mesh = quad_mesh
	
	print("✅ Mesh y material únicos creados para la instancia")

func _tiene_canal_alpha(texture: Texture2D) -> bool:
	# Verificar si la textura tiene canal alpha
	if texture is ImageTexture:
		var image = texture.get_image()
		if image:
			var format = image.get_format()
			# Verificar formatos que incluyen alpha en Godot 4
			return format in [
				Image.FORMAT_RGBA8,
				Image.FORMAT_RGBA4444,
				Image.FORMAT_RGBAF,
				Image.FORMAT_RGBAH
			]
	elif texture.has_method("get_format"):
		# Para otros tipos de textura que puedan tener información de formato
		var format_info = str(texture)
		return "RGBA" in format_info or "alpha" in format_info.to_lower()
	
	# Si no podemos determinar, asumir que podría tener alpha para PNG y similares
	var path = str(texture.resource_path).to_lower()
	return path.ends_with(".png") or path.ends_with(".webp")

func _calcular_tamaño(width: int, height: int) -> Vector2:
	var scale_factor: float
	var final_width = MAX_SIZE
	var final_height = MAX_SIZE
	
	if width >= height:
		scale_factor = MAX_SIZE / width
		final_height = height * scale_factor
	else:
		scale_factor = MAX_SIZE / height
		final_width = width * scale_factor
	
	return Vector2(final_width, final_height)

func _encontrar_mesh_instance(node: Node) -> MeshInstance3D:
	# Buscar MeshInstance3D en el nodo y sus hijos
	if node is MeshInstance3D:
		return node as MeshInstance3D
	
	for child in node.get_children():
		var found = _encontrar_mesh_instance(child)
		if found:
			return found
	
	return null

func _hacer_nodos_locales(node: Node):
	# Hacer que el nodo sea local (desconectado de la plantilla)
	if Engine.is_editor_hint():
		# En el editor, hacer que el nodo no tenga referencia a escena externa
		node.set_scene_file_path("")
		
		# Hacer que todos los hijos también sean locales
		for child in node.get_children():
			_hacer_nodos_locales(child)
	
	print("✅ Nodos desconectados de la plantilla - ahora son independientes")

func _get_real_path(uid_path: String) -> String:
	if uid_path.begins_with("uid://"):
		return ResourceUID.get_id_path(ResourceUID.text_to_id(uid_path))
	return uid_path
