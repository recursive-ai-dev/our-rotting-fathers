extends Node
## AudioManager Autoload Singleton
## Handles music, SFX, and voice playback with adaptive layers
## 
## Features:
## - Crossfade music transitions
## - Volume buses for mixing
## - Psychosis-based audio filters
## - Positional SFX for 2D space

const AUDIO_BUS_MASTER = "Master"
const AUDIO_BUS_MUSIC = "Music"
const AUDIO_BUS_SFX = "SFX"
const AUDIO_BUS_VOICE = "Voice"

# Audio players
var music_player: AudioStreamPlayer
var sfx_player: AudioStreamPlayer
var voice_player: AudioStreamPlayer

# Current state
var current_music: String = ""
var music_volume_db: float = -10.0
var sfx_volume_db: float = -5.0
var voice_volume_db: float = -3.0

# Psychosis audio effects
var psychosis_filter: AudioEffectFilter


func _ready() -> void:
	_setup_audio_players()
	_setup_audio_buses()


func _setup_audio_players() -> void:
	music_player = AudioStreamPlayer.new()
	music_player.name = "MusicPlayer"
	music_player.bus = AUDIO_BUS_MUSIC
	add_child(music_player)
	
	sfx_player = AudioStreamPlayer.new()
	sfx_player.name = "SFXPlayer"
	sfx_player.bus = AUDIO_BUS_SFX
	add_child(sfx_player)
	
	voice_player = AudioStreamPlayer.new()
	voice_player.name = "VoicePlayer"
	voice_player.bus = AUDIO_BUS_VOICE
	add_child(voice_player)
	
	# Connect signals
	music_player.finished.connect(_on_music_finished)


func _setup_audio_buses() -> void:
	# Audio buses are defined in project.godot default_bus_layout.tres
	# This is just for volume tracking
	pass


## Play music track with optional crossfade
## track_path: Resource path to audio file (e.g., "res://assets/audio/music/exploration_01.ogg")
## fade_in_seconds: Crossfade duration (0 = instant)
func play_music(track_path: String, fade_in_seconds: float = 1.0) -> void:
	if track_path == current_music:
		return
	
	var track = load(track_path)
	if not track:
		push_warning("AudioManager: Music track not found: ", track_path)
		return
	
	if fade_in_seconds > 0 and music_player.playing:
		# Crossfade: fade out current, fade in new
		var tween = create_tween()
		tween.tween_property(music_player, "volume_db", -80.0, fade_in_seconds)
		tween.parallel().call_method(_play_new_music, track)
	else:
		music_player.stream = track
		music_player.volume_db = music_volume_db
		music_player.play()
	
	current_music = track_path


func _play_new_music(track: AudioStream) -> void:
	music_player.stream = track
	music_player.volume_db = music_volume_db
	music_player.play()


## Stop music with fade out
func stop_music(fade_out_seconds: float = 1.0) -> void:
	if not music_player.playing:
		return
	
	var tween = create_tween()
	tween.tween_property(music_player, "volume_db", -80.0, fade_out_seconds)
	tween.tween_callback(music_player.stop)
	current_music = ""


## Play a sound effect
## sfx_path: Resource path to audio file
## volume_scale: Optional volume multiplier (0.0-1.0)
func play_sfx(sfx_path: String, volume_scale: float = 1.0) -> void:
	var sfx = load(sfx_path)
	if not sfx:
		push_warning("AudioManager: SFX not found: ", sfx_path)
		return
	
	sfx_player.stream = sfx
	sfx_player.volume_db = sfx_volume_db + linear_to_db(volume_scale)
	sfx_player.play()


## Play positional SFX (volume based on distance)
## position: World position of sound source
## max_distance: Distance at which sound becomes inaudible
func play_positional_sfx(sfx_path: String, position: Vector2, max_distance: float = 1000.0) -> void:
	var player_pos = _get_player_position()
	var distance = player_pos.distance_to(position)
	
	if distance > max_distance:
		return
	
	var volume_scale = 1.0 - (distance / max_distance)
	volume_scale = clamp(volume_scale, 0.0, 1.0)
	play_sfx(sfx_path, volume_scale)


func _get_player_position() -> Vector2:
	# TODO: Get actual player position from game scene
	return Vector2.ZERO


## Play voice line (dialogue, narration)
## voice_path: Resource path to audio file
func play_voice(voice_path: String) -> void:
	var voice = load(voice_path)
	if not voice:
		push_warning("AudioManager: Voice not found: ", voice_path)
		return
	
	voice_player.stream = voice
	voice_player.volume_db = voice_volume_db
	voice_player.play()


## Stop voice playback
func stop_voice() -> void:
	voice_player.stop()


## Set music volume (in dB)
func set_music_volume(volume_db: float) -> void:
	music_volume_db = volume_db
	if music_player.playing:
		music_player.volume_db = volume_db


## Set SFX volume (in dB)
func set_sfx_volume(volume_db: float) -> void:
	sfx_volume_db = volume_db


## Set voice volume (in dB)
func set_voice_volume(volume_db: float) -> void:
	voice_volume_db = volume_db


## Apply psychosis audio filter
## intensity: 0.0 (none) to 1.0 (maximum distortion)
func set_psychosis_filter(intensity: float) -> void:
	intensity = clamp(intensity, 0.0, 1.0)
	# TODO: Implement actual audio filter effects
	# Examples: reverb, pitch shift, binaural beats
	pass


func _on_music_finished() -> void:
	# Signal for chained music playback
	pass


## Get currently playing music track path
func get_current_music() -> String:
	return current_music


## Check if music is currently playing
func is_music_playing() -> bool:
	return music_player.playing


## Check if voice is currently playing
func is_voice_playing() -> bool:
	return voice_player.playing
