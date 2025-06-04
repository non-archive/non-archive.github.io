extends Node3D
class_name Audio

var audio_scene_path = "res://scenes/files/audio.tscn"
var auto_play: bool = true
var loop_audio: bool = true
var volume_db: float = 0.0
var unit_size: float = 10.0
var max_distance: float = 10.0
var attenuation_model: AudioStreamPlayer3D.AttenuationModel = AudioStreamPlayer3D.ATTENUATION_INVERSE_DISTANCE
var doppler_tracking: AudioStreamPlayer3D.DopplerTracking = AudioStreamPlayer3D.DOPPLER_TRACKING_DISABLED

# Función principal: crear y configurar una escena de audio
func crear_escena_audio(audio_path: String) -> Node3D:
	# Cargar la escena de audio
	var audio_scene = ResourceLoader.load(audio_scene_path)
	if not audio_scene:
		print("❌ Error: No se pudo cargar la escena de audio en: ", audio_scene_path)
		return null
	
	# Instanciar la escena
	var audio_instance = audio_scene.instantiate()
	
	# IMPORTANTE: Desconectar de la plantilla para evitar superposición
	audio_instance.scene_file_path = ""
	
	# Buscar el AudioStreamPlayer3D en la escena instanciada
	var audio_player = _encontrar_audio_player(audio_instance)
	
	if not audio_player:
		print("⚠️ No se encontró AudioStreamPlayer3D en la escena: ", audio_scene_path)
		audio_instance.queue_free()
		return null
	
	# Cargar el stream de audio
	var audio_stream = ResourceLoader.load(audio_path)
	if not audio_stream:
		print("❌ Error cargando stream de audio: ", audio_path)
		audio_instance.queue_free()
		return null
	
	# Configurar el audio player con todos los parámetros
	audio_player.stream = audio_stream
	audio_player.volume_db = volume_db
	audio_player.unit_size = unit_size
	audio_player.max_distance = max_distance
	audio_player.attenuation_model = attenuation_model
	audio_player.doppler_tracking = doppler_tracking
	
	# Configurar loop dependiendo del tipo de stream
	if loop_audio:
		_configurar_loop_audio(audio_stream)
	
	# No reproducir en el editor, solo configurar para runtime
	if auto_play and not Engine.is_editor_hint():
		audio_player.play()
	
	print("✅ Audio cargado correctamente: ", audio_path.get_file())
	
	# Hacer que todos los nodos sean locales al árbol (desconectar de plantilla)
	_hacer_nodos_locales(audio_instance)
	
	# Ocultar hijos del nodo en el editor (colapsado)
	if Engine.is_editor_hint():
		audio_instance.set_display_folded(true)
	
	# Configurar auto-reproducción en runtime
	if auto_play:
		_configurar_autoplay_runtime(audio_instance, audio_player)
	
	# Configurar textos de título y contador de tiempo
	_configurar_textos_ui(audio_instance, audio_path, audio_player)
	
	return audio_instance

func _hacer_nodos_locales(node: Node):
	# Hacer que el nodo sea local (desconectado de la plantilla)
	if Engine.is_editor_hint():
		# En el editor, hacer que el nodo no tenga referencia a escena externa
		node.set_scene_file_path("")
		
		# Hacer que todos los hijos también sean locales
		for child in node.get_children():
			_hacer_nodos_locales(child)
	
	print("✅ Nodos desconectados de la plantilla - ahora son independientes")

func _configurar_textos_ui(audio_instance: Node3D, audio_path: String, audio_player: AudioStreamPlayer3D):
	# Buscar los nodos de texto 3D por nombre
	var titulo_label = audio_instance.find_child("TituloAudio", true, false)
	var contador_label = audio_instance.find_child("ContadorTiempo", true, false)
	
	# Configurar título del archivo
	if titulo_label and titulo_label is Label3D:
		var nombre_archivo = ResourceUID.get_id_path(ResourceUID.text_to_id(audio_path)).replace("res://", "")
		titulo_label.text = nombre_archivo
		print("✅ Título 3D configurado: ", nombre_archivo)
	else:
		print("⚠️ No se encontró el nodo 'TituloAudio' (Label3D) en la escena")
	
	# Configurar contador de tiempo
	if contador_label and contador_label is Label3D:
		contador_label.text = "00:00 / 00:00"
		# Añadir metadata para el script de runtime
		audio_instance.set_meta("contador_label_path", audio_instance.get_path_to(contador_label))
		print("✅ Contador de tiempo 3D configurado")
	else:
		print("⚠️ No se encontró el nodo 'ContadorTiempo' (Label3D) en la escena")

func _configurar_loop_audio(audio_stream: AudioStream):
	# Para diferentes tipos de audio streams
	if audio_stream.has_method("set_loop"):
		audio_stream.set_loop(true)
	elif "loop" in audio_stream:
		audio_stream.loop = true
	elif audio_stream.has_method("set_loop_mode"):
		# Para AudioStreamWAV
		audio_stream.set_loop_mode(AudioStreamWAV.LOOP_FORWARD)
	elif "loop_mode" in audio_stream:
		# Para AudioStreamWAV
		audio_stream.loop_mode = AudioStreamWAV.LOOP_FORWARD
	else:
		print("⚠️ No se pudo configurar loop para el tipo de audio: ", audio_stream.get_class())

func _configurar_autoplay_runtime(audio_instance: Node3D, audio_player: AudioStreamPlayer3D):
	# Añadir metadata para que el nodo sepa que debe reproducirse en runtime
	audio_instance.set_meta("autoplay_runtime", true)
	audio_instance.set_meta("audio_player_path", audio_instance.get_path_to(audio_player))
	
	# Crear un script completo para autoplay y contador de tiempo
	var script_code = """extends Node3D

var audio_player: AudioStreamPlayer3D
var contador_label: Label3D

func _ready():
	if not Engine.is_editor_hint() and has_meta("autoplay_runtime"):
		# Configurar audio player
		var player_path = get_meta("audio_player_path")
		audio_player = get_node(player_path)
		
		# Configurar contador de tiempo
		if has_meta("contador_label_path"):
			var contador_path = get_meta("contador_label_path")
			contador_label = get_node(contador_path)
		
		# Iniciar reproducción
		if audio_player and audio_player is AudioStreamPlayer3D:
			audio_player.play()
			print("🔊 Audio iniciado automáticamente: ", name)

func _process(_delta):
	if audio_player and contador_label and audio_player.playing:
		_actualizar_contador_tiempo()

func _actualizar_contador_tiempo():
	var tiempo_actual = audio_player.get_playback_position()
	var duracion_total = audio_player.stream.get_length()
	
	var minutos_actual = int(tiempo_actual / 60)
	var segundos_actual = int(tiempo_actual) % 60
	var minutos_total = int(duracion_total / 60)
	var segundos_total = int(duracion_total) % 60
	
	contador_label.text = "%02d:%02d / %02d:%02d" % [minutos_actual, segundos_actual, minutos_total, segundos_total]
"""
	
	var script = GDScript.new()
	script.source_code = script_code
	audio_instance.set_script(script)

func _encontrar_audio_player(node: Node) -> AudioStreamPlayer3D:
	# Buscar AudioStreamPlayer3D en el nodo y sus hijos
	if node is AudioStreamPlayer3D:
		return node as AudioStreamPlayer3D
	
	for child in node.get_children():
		var found = _encontrar_audio_player(child)
		if found:
			return found
	
	return null
