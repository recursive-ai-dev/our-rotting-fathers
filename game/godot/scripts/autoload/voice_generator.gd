extends Node
## Voice Generator Autoload Singleton
## Plays hardcoded voice lines from local MP3 files
##
## Usage:
##   VoiceGenerator.speak_line("intro_narrator")
##   VoiceGenerator.speak_all()
##
## Voice lines are stored in res://assets/audio/voice/

signal voice_started(key: String)
signal voice_finished(key: String)

const VOICE_DIR = "res://assets/audio/voice/"

# Hardcoded voice lines (key -> text for reference)
var VOICE_LINES: Dictionary = {
	"intro_narrator": "The god is dead. His flesh feeds the world. But his bones... his bones still whisper.",
	"combat_start": "Steel drawn. Blood spilled. The rot demands sacrifice.",
	"combat_victory": "The flesh yields. The bones remember.",
	"combat_defeat": "You fall. The rot consumes another.",
	"low_sanity": "The whispers grow louder. You cannot unhear them now.",
	"faction_rotborn": "We are the children of decay. We embrace the rot.",
	"faction_purified": "Silence is purity. Speech is contamination.",
	"discovery": "Something stirs beneath the skin of this place.",
	"death": "Return to the flesh. Return to the cycle.",
	"heal": "The rot recedes. For now."
}

var _voice_player: AudioStreamPlayer
var _current_key: String = ""
var _is_playing: bool = false


func _ready() -> void:
	_voice_player = AudioStreamPlayer.new()
	_voice_player.name = "VoicePlayer"
	_voice_player.bus = "Voice"
	_voice_player.finished.connect(_on_voice_finished)
	add_child(_voice_player)


## Play a voice line by key
func speak_line(key: String) -> void:
	if _is_playing:
		stop()
	
	if not VOICE_LINES.has(key):
		push_warning("VoiceGenerator: Voice line not found: ", key)
		return
	
	var audio_path = VOICE_DIR + key + ".mp3"
	var audio = load(audio_path)
	
	if not audio:
		push_warning("VoiceGenerator: Audio file not found: ", audio_path)
		return
	
	_current_key = key
	_voice_player.stream = audio
	_voice_player.play()
	_is_playing = true
	voice_started.emit(key)


## Play all voice lines sequentially (for testing)
func speak_all() -> void:
	if _is_playing:
		stop()
	
	_play_next_in_sequence(0)


func _play_next_in_sequence(index: int) -> void:
	var keys = VOICE_LINES.keys()
	
	if index >= keys.size():
		return
	
	_current_key = keys[index]
	var audio_path = VOICE_DIR + _current_key + ".mp3"
	var audio = load(audio_path)
	
	if audio:
		_voice_player.stream = audio
		_voice_player.play()
		_is_playing = true
		voice_started.emit(_current_key)
		
		# Wait for finish then play next
		await _voice_player.finished
		await get_tree().create_timer(0.5).timeout
		_play_next_in_sequence(index + 1)


## Stop current voice playback
func stop() -> void:
	if _is_playing:
		_voice_player.stop()
		_is_playing = false
		voice_finished.emit(_current_key)


## Check if a voice line file exists
func has_voice_line(key: String) -> bool:
	var audio_path = VOICE_DIR + key + ".mp3"
	return ResourceLoader.exists(audio_path)


## Get list of available voice line keys
func get_voice_line_keys() -> Array:
	return VOICE_LINES.keys()


## Get voice line text by key
func get_voice_line_text(key: String) -> String:
	return VOICE_LINES.get(key, "")


## Get current playing key
func get_current_key() -> String:
	return _current_key


## Check if voice is currently playing
func is_playing() -> bool:
	return _is_playing


func _on_voice_finished() -> void:
	_is_playing = false
	voice_finished.emit(_current_key)
