extends Control
## Voice Test UI - Simple interface to test hardcoded voice lines
##
## Press number keys 1-0 to play voice lines

@onready var status_label: Label
@onready var current_text_label: Label
@onready var voice_lines_list: VBoxContainer


func _ready() -> void:
	_build_ui()
	_connect_signals()
	status_label.text = "10 voice lines loaded (local MP3 files)"
	status_label.modulate = Color.GREEN


func _build_ui() -> void:
	var main_vbox = VBoxContainer.new()
	main_vbox.layout_mode = 1
	main_vbox.anchors_preset = 15
	main_vbox.anchor_right = 1.0
	main_vbox.anchor_bottom = 1.0
	main_vbox.grow_horizontal = 2
	main_vbox.grow_vertical = 2
	main_vbox.offset_left = 20
	main_vbox.offset_top = 20
	main_vbox.offset_right = -20
	main_vbox.offset_bottom = -20
	add_child(main_vbox)
	
	status_label = Label.new()
	status_label.layout_mode = 2
	status_label.text = "Loading..."
	status_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	main_vbox.add_child(status_label)
	
	current_text_label = Label.new()
	current_text_label.layout_mode = 2
	current_text_label.text = "Press 1-0 to play voice lines"
	current_text_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	current_text_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	main_vbox.add_child(current_text_label)
	
	main_vbox.add_child(HSeparator.new())
	
	voice_lines_list = VBoxContainer.new()
	voice_lines_list.layout_mode = 2
	main_vbox.add_child(voice_lines_list)
	
	var keys = VoiceGenerator.get_voice_line_keys()
	
	for i in range(min(keys.size(), 10)):
		var key = keys[i]
		var text = VoiceGenerator.get_voice_line_text(key)
		
		var button = Button.new()
		button.text = str(i + 1) + ". [" + key + "]\n" + text
		button.custom_minimum_size = Vector2(0, 50)
		button.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
		button.pressed.connect(_on_voice_line_pressed.bind(key))
		voice_lines_list.add_child(button)


func _connect_signals() -> void:
	VoiceGenerator.voice_started.connect(_on_voice_started)
	VoiceGenerator.voice_finished.connect(_on_voice_finished)


func _on_voice_line_pressed(key: String) -> void:
	VoiceGenerator.speak_line(key)


func _on_voice_started(key: String) -> void:
	var text = VoiceGenerator.get_voice_line_text(key)
	current_text_label.text = "Playing: " + text
	status_label.text = "Playing: " + key
	status_label.modulate = Color.YELLOW


func _on_voice_finished(key: String) -> void:
	current_text_label.text = "Done: " + key
	status_label.text = "10 voice lines loaded (local MP3 files)"
	status_label.modulate = Color.GREEN


func _unhandled_input(event: InputEvent) -> void:
	if not event is InputEventKey or not (event as InputEventKey).pressed:
		return
	
	var keycode = (event as InputEventKey).keycode
	var keys = VoiceGenerator.get_voice_line_keys()
	
	if keycode >= KEY_1 and keycode <= KEY_9:
		var index = keycode - KEY_1
		if index < keys.size():
			_on_voice_line_pressed(keys[index])
	elif keycode == KEY_0:
		if 9 < keys.size():
			_on_voice_line_pressed(keys[9])
