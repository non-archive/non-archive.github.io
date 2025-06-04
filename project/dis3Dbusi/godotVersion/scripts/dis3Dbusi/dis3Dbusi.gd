@tool
extends Node3D

enum Type { FOLDER, FILE, OCEAN_ARCHIVE }
enum Distribution { TREE, GRID, RANDOM }

@export var type: Type = Type.FILE : set = set_type
@export_file var filepath = "" : set = set_filepath
@export_dir var folderpath = "" : set = set_folderpath
@export var id: String = "" : set = set_id
@export var subfolders: bool = false
@export var distribution: Distribution = Distribution.RANDOM
@export_tool_button("Generate") var generate = generar_contenido

func _ready():
	if not Engine.is_editor_hint() and get_child_count() == 0:
		generar_contenido()

func set_type(value: Type):
	type = value
	update_configuration_warnings()

func set_filepath(value: String):
	filepath = value
	update_configuration_warnings()

func set_folderpath(value: String):
	folderpath = value
	update_configuration_warnings()

func set_id(value: String):
	id = value
	update_configuration_warnings()

func generar_contenido():
	borrar_contenido()
	match type:
		Type.FILE:
			if filepath != "":
				crear_archivo()
			else:
				crear_placeholder()
		Type.FOLDER, Type.OCEAN_ARCHIVE:
			crear_placeholder()

func crear_archivo():
	var archivo = Archivo.new(filepath)
	var node = archivo.get_mesh()  # Ahora puede ser Node3D o MeshInstance3D
	node.name = archivo._get_real_path(filepath).replace("res://", "")
	add_child(node)
	definir_owner(node)

func crear_placeholder():
	var mesh_instance = MeshInstance3D.new()
	# Generar nombre único para evitar conflictos
	mesh_instance.name = "placeholder_" + str(Time.get_unix_time_from_system())
	
	var sphere_mesh = SphereMesh.new()
	sphere_mesh.radius = 0.2
	sphere_mesh.height = 0.4
	
	var material = StandardMaterial3D.new()
	material.albedo_color = Color.MAGENTA
	sphere_mesh.material = material
	
	mesh_instance.mesh = sphere_mesh
	add_child(mesh_instance)
	definir_owner(mesh_instance)

func definir_owner(node: Node):
	if Engine.is_editor_hint():
		# Hacer que el nodo sea completamente local (sin referencia a escena externa)
		if node.has_method("set_scene_file_path"):
			node.set_scene_file_path("")
		
		# Configurar el propietario
		node.set_owner(get_tree().edited_scene_root)
		
		# Si es un Node3D con hijos, configurar propietarios recursivamente
		_configurar_propietarios_recursivo(node)
		
		print("✅ Nodo ", node.name, " configurado como local e independiente")
	else:
		node.set_owner(self)

func _configurar_propietarios_recursivo(node: Node):
	for child in node.get_children():
		if Engine.is_editor_hint():
			# Hacer que cada hijo también sea independiente
			if child.has_method("set_scene_file_path"):
				child.set_scene_file_path("")
			
			child.set_owner(get_tree().edited_scene_root)
		_configurar_propietarios_recursivo(child)

func borrar_contenido():
	print("🗑️ Limpiando contenido previo...")
	
	for child in get_children():
		# Limpiar cualquier referencia a escenas externas antes de eliminar
		if child.has_method("set_scene_file_path"):
			child.set_scene_file_path("")
		
		# Marcar para eliminación
		child.call_deferred("queue_free")
	
	print("✅ Contenido limpiado correctamente")
