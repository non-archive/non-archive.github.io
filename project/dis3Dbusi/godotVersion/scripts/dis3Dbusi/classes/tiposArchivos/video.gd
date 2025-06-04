extends Node3D
class_name Video

var video_scene_path = "res://scenes/files/video.tscn"
var auto_play: bool = true
var loop_video: bool = true
var volume_db: float = 0.0
var MAX_SIZE: float = 2.0

# 🔊 Parámetros para audio 3D
var enable_3d_audio: bool = false
var unit_size: float = 10.0
var max_distance: float = 10.0
var attenuation_model: AudioStreamPlayer3D.AttenuationModel = AudioStreamPlayer3D.ATTENUATION_INVERSE_DISTANCE

# Variables para tracking del video actual
var current_video_path: String = ""
var current_video_real_path: String = ""

# Función principal: crear y configurar una escena de video
func crear_escena_video(video_path: String, audio_3d: bool = false) -> Node3D:
	print("🎬 [Video] Iniciando creación de escena para: ", video_path)
	enable_3d_audio = audio_3d
	
	# Guardar paths para uso posterior
	current_video_path = video_path
	current_video_real_path = _get_real_path(video_path)
	print("🎬 [Video] Path real: ", current_video_real_path)
	
	# Cargar la escena de video
	var video_scene = ResourceLoader.load(video_scene_path)
	if not video_scene:
		print("❌ Error: No se pudo cargar la escena de video en: ", video_scene_path)
		return null
	
	# Instanciar la escena
	var video_instance = video_scene.instantiate()
	video_instance.scene_file_path = ""
	
	# Buscar componentes
	var video_player = _encontrar_video_player(video_instance)
	var mesh_instance = _encontrar_mesh_instance(video_instance)
	
	if not video_player or not mesh_instance:
		print("❌ Error: Componentes faltantes en la escena de video")
		video_instance.queue_free()
		return null
	
	# Cargar el stream de video
	var video_stream = ResourceLoader.load(video_path)
	if not video_stream or not video_stream is VideoStream:
		print("❌ Error: No se pudo cargar el video: ", video_path)
		_mostrar_ayuda_formato()
		video_instance.queue_free()
		return null
	
	# 🔊 Configurar audio 3D ANTES de configurar el video player
	var audio_player_3d = null
	if enable_3d_audio:
		audio_player_3d = _configurar_audio_3d(video_instance)
		if not audio_player_3d:
			print("⚠️ [Audio3D] No se pudo configurar, usando audio normal")
			enable_3d_audio = false
	
	# Configurar el video player (silenciado si hay audio 3D)
	_configurar_video_player(video_player, video_stream, enable_3d_audio)
	
	# Configurar el mesh para mostrar el video
	_configurar_mesh_video(mesh_instance, video_player)
	
	# Configurar UI y controles
	_configurar_controles_ui(video_instance, video_path, video_player)
	
	# Configurar autoplay en runtime
	if auto_play:
		_configurar_autoplay_runtime(video_instance, video_player, audio_player_3d)
	
	# Hacer nodos locales y configurar nombre
	_hacer_nodos_locales(video_instance)
	_configurar_nombre_unico(video_instance)
	
	if Engine.is_editor_hint():
		video_instance.set_display_folded(true)
	
	var status = "Audio 3D" if enable_3d_audio else "Audio Normal"
	print("✅ [Video] Creado correctamente con ", status)
	
	return video_instance

# 🔊 Configurar audio 3D separado
func _configurar_audio_3d(video_instance: Node3D) -> AudioStreamPlayer3D:
	print("🔊 [Audio3D] Iniciando configuración...")
	
	# Buscar archivo de audio separado  
	var audio_path = _buscar_archivo_audio_separado()
	if not audio_path:
		print("❌ [Audio3D] No se encontró archivo de audio separado")
		_mostrar_ayuda_audio_3d()
		return null
	
	print("🎵 [Audio3D] Archivo encontrado: ", audio_path)
	
	# Cargar el stream de audio
	var audio_stream = ResourceLoader.load(audio_path)
	if not audio_stream or not audio_stream is AudioStream:
		print("❌ [Audio3D] Error cargando audio: ", audio_path)
		return null
	
	# Crear y configurar AudioStreamPlayer3D
	var audio_player_3d = AudioStreamPlayer3D.new()
	audio_player_3d.name = "AudioPlayer3D"
	audio_player_3d.stream = audio_stream
	audio_player_3d.volume_db = volume_db
	audio_player_3d.unit_size = unit_size
	audio_player_3d.max_distance = max_distance
	audio_player_3d.attenuation_model = attenuation_model
	
	# Configurar loop si es necesario
	if loop_video:
		_configurar_loop_audio_3d(audio_stream)
	
	# Añadir al árbol
	video_instance.add_child(audio_player_3d)
	
	print("✅ [Audio3D] Configurado correctamente")
	return audio_player_3d

# 🔍 Buscar archivo de audio separado
func _buscar_archivo_audio_separado() -> String:
	if current_video_real_path == "":
		print("❌ [Audio3D] Path del video no disponible")
		return ""
	
	# Obtener el nombre base sin extensión
	var base_name = current_video_real_path.get_file().get_basename()
	var directory = current_video_real_path.get_base_dir()
	
	print("🔍 [Audio3D] Buscando audio para: ", base_name)
	print("🔍 [Audio3D] En directorio: ", directory)
	
	# Posibles sufijos y extensiones
	var suffixes = ["_audio", "_sound", "_3d", ""]
	var extensions = [".ogg", ".wav", ".mp3"]
	
	# Buscar combinaciones
	for suffix in suffixes:
		for extension in extensions:
			var audio_filename = base_name + suffix + extension
			var full_audio_path = directory + "/" + audio_filename
			
			print("🔍 [Audio3D] Probando: ", full_audio_path)
			
			# Verificar si el archivo existe
			if FileAccess.file_exists(full_audio_path):
				print("✅ [Audio3D] Encontrado: ", full_audio_path)
				return full_audio_path
			
			# También probar sin el directorio (path relativo)
			if FileAccess.file_exists(audio_filename):
				print("✅ [Audio3D] Encontrado (relativo): ", audio_filename)
				return audio_filename
	
	return ""

# Configurar loop para audio 3D
func _configurar_loop_audio_3d(audio_stream):
	if audio_stream.has_method("set_loop"):
		audio_stream.set_loop(true)
	elif "loop" in audio_stream:
		audio_stream.loop = true

# Configurar video player
func _configurar_video_player(video_player: VideoStreamPlayer, video_stream: VideoStream, silenciar: bool = false):
	video_player.stream = video_stream
	
	if silenciar:
		video_player.volume_db = -80  # Silenciar para usar audio 3D
		print("🔇 [Video] Audio silenciado - usando Audio 3D separado")
	else:
		video_player.volume_db = volume_db
	
	if loop_video:
		video_player.loop = true
	
	# No reproducir automáticamente en el editor
	if auto_play and not Engine.is_editor_hint():
		video_player.play()

# Configurar mesh para mostrar video
func _configurar_mesh_video(mesh_instance: MeshInstance3D, video_player: VideoStreamPlayer):
	var material = StandardMaterial3D.new()
	material.cull_mode = BaseMaterial3D.CULL_DISABLED
	material.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
	
	# Duplicar mesh para evitar compartir recursos
	var quad_mesh: QuadMesh
	if mesh_instance.mesh and mesh_instance.mesh is QuadMesh:
		quad_mesh = mesh_instance.mesh.duplicate()
	else:
		quad_mesh = QuadMesh.new()
	
	# Calcular tamaño proporcional
	var video_size = _obtener_dimensiones_video(video_player)
	var size = _calcular_tamaño(int(video_size.x), int(video_size.y))
	
	quad_mesh.size = size
	quad_mesh.material = material
	mesh_instance.mesh = quad_mesh
	
	print("✅ [Video] Mesh configurado: ", video_size, " -> ", size)

# Obtener dimensiones del video
func _obtener_dimensiones_video(video_player: VideoStreamPlayer) -> Vector2:
	# En runtime, usar textura si está disponible
	if not Engine.is_editor_hint() and video_player.is_playing():
		var video_texture = video_player.get_video_texture()
		if video_texture and video_texture.get_width() > 0:
			return Vector2(video_texture.get_width(), video_texture.get_height())
	
	# Fallback: proporciones por defecto
	if Engine.is_editor_hint():
		return Vector2(1080, 1080)  # Cuadrado para editor
	else:
		return Vector2(1920, 1080)  # 16:9 para runtime

# Configurar controles UI
func _configurar_controles_ui(video_instance: Node3D, video_path: String, _video_player: VideoStreamPlayer):
	# Configurar título
	var titulo_label = video_instance.find_child("TituloVideo", true, false)
	if titulo_label and titulo_label is Label3D:
		var nombre_archivo = current_video_real_path.replace("res://", "")
		if enable_3d_audio:
			nombre_archivo += " [3D Audio]"
		titulo_label.text = nombre_archivo
		print("✅ [UI] Título configurado: ", nombre_archivo)
	
	# Configurar contador
	var contador_label = video_instance.find_child("ContadorTiempo", true, false)
	if contador_label and contador_label is Label3D:
		contador_label.text = "00:00"
		video_instance.set_meta("contador_label_path", video_instance.get_path_to(contador_label))
		print("✅ [UI] Contador configurado")

# Configurar autoplay para runtime
func _configurar_autoplay_runtime(video_instance: Node3D, video_player: VideoStreamPlayer, audio_player_3d = null):
	# Guardar metadata
	video_instance.set_meta("autoplay_runtime", true)
	video_instance.set_meta("video_player_path", video_instance.get_path_to(video_player))
	video_instance.set_meta("enable_3d_audio", enable_3d_audio)
	
	if audio_player_3d:
		video_instance.set_meta("audio_player_3d_path", video_instance.get_path_to(audio_player_3d))
	
	# Script para runtime
	var script_code = """extends Node3D

var video_player: VideoStreamPlayer
var audio_player_3d: AudioStreamPlayer3D
var contador_label: Label3D
var mesh_instance: MeshInstance3D
var has_3d_audio: bool = false
var sync_tolerance: float = 0.1

func _ready():
	if not Engine.is_editor_hint() and has_meta("autoplay_runtime"):
		print("🎬 [Runtime] Configurando video...")
		
		_configurar_referencias()
		_configurar_textura_video()
		_iniciar_reproduccion()

func _configurar_referencias():
	# Video player
	if has_meta("video_player_path"):
		video_player = get_node(get_meta("video_player_path"))
	
	# Contador
	if has_meta("contador_label_path"):
		contador_label = get_node(get_meta("contador_label_path"))
	
	# Audio 3D
	has_3d_audio = get_meta("enable_3d_audio", false)
	if has_3d_audio and has_meta("audio_player_3d_path"):
		audio_player_3d = get_node(get_meta("audio_player_3d_path"))
		print("🔊 [Runtime] Audio 3D encontrado")
	
	# Mesh
	mesh_instance = _encontrar_mesh_instance(self)

func _configurar_textura_video():
	if video_player and mesh_instance and mesh_instance.mesh:
		var material = mesh_instance.mesh.material
		if material is StandardMaterial3D:
			material.albedo_texture = video_player.get_video_texture()

func _iniciar_reproduccion():
	if video_player:
		video_player.play()
		print("🎬 [Runtime] Video iniciado: ", name)
	
	if has_3d_audio and audio_player_3d:
		audio_player_3d.play()
		print("🔊 [Runtime] Audio 3D iniciado: ", name)

func _process(_delta):
	if video_player and video_player.is_playing():
		# Actualizar contador
		if contador_label:
			_actualizar_contador()
		
		# Sincronizar audio 3D
		if has_3d_audio and audio_player_3d:
			_sincronizar_audio_3d()
		
		# Ajustar dimensiones del mesh
		_ajustar_dimensiones_mesh()

func _actualizar_contador():
	var tiempo = video_player.stream_position
	var minutos = int(tiempo / 60)
	var segundos = int(tiempo) % 60
	contador_label.text = "%02d:%02d" % [minutos, segundos]

func _sincronizar_audio_3d():
	# Sincronizar estado
	if video_player.is_playing() and not audio_player_3d.playing:
		audio_player_3d.play()
	elif not video_player.is_playing() and audio_player_3d.playing:
		audio_player_3d.stop()
	
	# Sincronizar posición si ambos están reproduciéndose
	if video_player.is_playing() and audio_player_3d.playing:
		var video_pos = video_player.stream_position
		var audio_pos = audio_player_3d.get_playback_position()
		
		if abs(video_pos - audio_pos) > sync_tolerance:
			audio_player_3d.seek(video_pos)

func _ajustar_dimensiones_mesh():
	if not mesh_instance or not mesh_instance.mesh:
		return
	
	var video_texture = video_player.get_video_texture()
	if video_texture and video_texture.get_width() > 0:
		var width = video_texture.get_width()
		var height = video_texture.get_height()
		var new_size = _calcular_tamaño_proporcional(width, height)
		
		if mesh_instance.mesh is QuadMesh:
			var current_size = mesh_instance.mesh.size
			if abs(current_size.x - new_size.x) > 0.01 or abs(current_size.y - new_size.y) > 0.01:
				mesh_instance.mesh.size = new_size

func _calcular_tamaño_proporcional(width: int, height: int) -> Vector2:
	var MAX_SIZE: float = 2.0
	var scale_factor: float
	
	if width >= height:
		scale_factor = MAX_SIZE / width
		return Vector2(MAX_SIZE, height * scale_factor)
	else:
		scale_factor = MAX_SIZE / height
		return Vector2(width * scale_factor, MAX_SIZE)

func _encontrar_mesh_instance(node: Node) -> MeshInstance3D:
	if node is MeshInstance3D:
		return node
	for child in node.get_children():
		var found = _encontrar_mesh_instance(child)
		if found:
			return found
	return null
"""
	
	var script = GDScript.new()
	script.source_code = script_code
	video_instance.set_script(script)

# Funciones auxiliares
func _calcular_tamaño(width: int, height: int) -> Vector2:
	var scale_factor: float
	if width >= height:
		scale_factor = MAX_SIZE / width
		return Vector2(MAX_SIZE, height * scale_factor)
	else:
		scale_factor = MAX_SIZE / height
		return Vector2(width * scale_factor, MAX_SIZE)

func _encontrar_video_player(node: Node) -> VideoStreamPlayer:
	if node is VideoStreamPlayer:
		return node
	for child in node.get_children():
		var found = _encontrar_video_player(child)
		if found:
			return found
	return null

func _encontrar_mesh_instance(node: Node) -> MeshInstance3D:
	if node is MeshInstance3D:
		return node
	for child in node.get_children():
		var found = _encontrar_mesh_instance(child)
		if found:
			return found
	return null

func _hacer_nodos_locales(node: Node):
	if Engine.is_editor_hint():
		node.set_scene_file_path("")
		for child in node.get_children():
			_hacer_nodos_locales(child)

func _configurar_nombre_unico(video_instance: Node3D):
	var base_name = current_video_real_path.get_file().get_basename()
	var suffix = "_3D" if enable_3d_audio else ""
	var timestamp = str(Time.get_unix_time_from_system())
	video_instance.name = "Video_" + base_name + suffix + "_" + timestamp

func _get_real_path(uid_path: String) -> String:
	if uid_path.begins_with("uid://"):
		var uid_id = ResourceUID.text_to_id(uid_path)
		var real_path = ResourceUID.get_id_path(uid_id)
		if real_path != "":
			return real_path
		else:
			print("⚠️ [UID] No se pudo resolver: ", uid_path)
			return uid_path
	return uid_path

# Mensajes de ayuda
func _mostrar_ayuda_formato():
	print("💡 SUGERENCIA: Godot 4 solo soporta formato .ogv (Ogg Theora)")
	print("💡 Convierte con: ffmpeg -i video.mp4 -codec:v libtheora -qscale:v 9 -codec:a libvorbis -qscale:a 8 -r 30 video.ogv")

func _mostrar_ayuda_audio_3d():
	print("💡 Para usar Audio 3D, extrae el audio del video:")
	print("💡 ffmpeg -i ", current_video_real_path.get_file(), " -vn -acodec libvorbis -q:a 8 ", current_video_real_path.get_file().get_basename(), "_audio.ogg")
	print("💡 Coloca el archivo .ogg en la misma carpeta que el video")
