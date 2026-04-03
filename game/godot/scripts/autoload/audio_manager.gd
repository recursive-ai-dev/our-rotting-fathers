extends Node
## AudioManager Autoload Singleton
## Handles music, SFX, and voice playback from local files
##
## Usage:
##   AudioManager.play_sfx("combat_hit")
##   AudioManager.play_music("exploration_calm")
##   AudioManager.stop_music()
##   AudioManager.set_sanity_level(0.7)

signal music_changed(track_key: String)
signal sfx_played(sfx_key: String)

const MUSIC_DIR = "res://assets/audio/music/"
const SFX_DIR = "res://assets/audio/sfx/"

# Music tracks (key -> prompt used to generate, for reference)
var MUSIC_TRACKS: Dictionary = {
	"exploration_calm": "Dark ambient drone with distant echoing tones",
	"exploration_tense": "Tense dark ambient with pulsing bass",
	"combat_theme": "Dark tribal percussion with deep war drums",
	"sanity_break": "Dissonant atonal horror soundscape",
	"faction_rotborn": "Organic pulsing ambient with heartbeat rhythms",
	"faction_purified": "Sparse minimal ambient with hollow bone wind",
	"boss_battle": "Epic dark boss music with heavy tribal drums",
	"death_theme": "Mournful dark ambient with slow descending tones",
	"victory_theme": "Slow dark triumph with minor key strings",
	"ambient_drones": "Very slow dark ambient drones, sub bass rumbling"
}

# SFX sounds (key -> prompt used to generate, for reference)
var SFX_SOUNDS: Dictionary = {
	# UI
	"ui_click_bone": "Single dry bone tap click",
	"ui_confirm": "Deep bone snap confirm sound",
	"ui_hover": "Soft flesh brush whisper",
	"ui_error": "Low wet squelch error sound",
	# Movement
	"step_wet": "Single wet squishy footstep",
	"step_bone": "Footstep on dry bone surface",
	"jump": "Springy tendon bounce",
	"land": "Heavy fleshy thud landing",
	# Combat
	"combat_hit": "Wet meaty punch impact",
	"combat_swing": "Whooshing air blade swing",
	"combat_block": "Hard bone on bone clash",
	"combat_crit": "Deep tearing ripping sound",
	"enemy_death": "Squelching collapse dissolving flesh",
	"player_hurt": "Painful flesh wound tear",
	# Magic
	"magic_cast": "Unsettling reversed audio swell",
	"magic_impact": "Deep unnatural bass explosion",
	"magic_heal": "Gentle pulsing organic regrowth",
	"sanity_drift": "Slow whoosh with whispered undertones",
	# Ambient
	"ambient_drip": "Slow dripping water in hollow bone cave",
	"ambient_creak": "Slow structural bone creaking",
	"ambient_whisper": "Distant unintelligible whispering",
	"ambient_breathing": "Deep slow labored breathing",
	"ambient_wind": "Wind howling through hollow bones",
	"heartbeat_slow": "Slow deep heartbeat with bass pulse",
	"heartbeat_fast": "Fast panicked heartbeat",
	# Psychosis
	"psychosis_whisper": "Close whispered voice right in ear",
	"psychosis_ring": "High pitched tinnitus ringing",
	"psychosis_pulse": "Low throbbing bass pulse",
	"psychosis_crack": "Random bone crack nearby"
}

# Audio players
var music_player: AudioStreamPlayer
var ambient_player: AudioStreamPlayer  # For looping ambient sounds
var sfx_player: AudioStreamPlayer2D    # For positional SFX
var voice_player: AudioStreamPlayer

# Volume settings (in dB)
var music_volume_db: float = -10.0
var sfx_volume_db: float = -5.0
var voice_volume_db: float = -3.0
var ambient_volume_db: float = -15.0

# State
var current_music: String = ""
var current_ambient: String = ""
var sanity_level: float = 0.0

# Sanity-based ambient sounds
var LOW_SANITY_AMBIENT: Array = ["psychosis_whisper", "psychosis_ring", "psychosis_pulse"]
var HIGH_SANITY_AMBIENT: Array = ["ambient_drip", "ambient_creak", "ambient_breathing"]


func _ready() -> void:
	_setup_players()


func _setup_players() -> void:
	# Music player (loops)
	music_player = AudioStreamPlayer.new()
	music_player.name = "MusicPlayer"
	music_player.bus = "Music"
	add_child(music_player)
	
	# Ambient player (loops, layered under music)
	ambient_player = AudioStreamPlayer.new()
	ambient_player.name = "AmbientPlayer"
	ambient_player.bus = "Music"
	add_child(ambient_player)
	
	# SFX player
	sfx_player = AudioStreamPlayer.new()
	sfx_player.name = "SFXPlayer"
	sfx_player.bus = "SFX"
	add_child(sfx_player)
	
	# Voice player
	voice_player = AudioStreamPlayer.new()
	voice_player.name = "VoicePlayer"
	voice_player.bus = "Voice"
	add_child(voice_player)


# === MUSIC ===

## Play music track by key
func play_music(track_key: String, fade_in: float = 1.0) -> void:
	if track_key == current_music:
		return
	
	var audio_path = MUSIC_DIR + track_key + ".mp3"
	var audio = load(audio_path)
	
	if not audio:
		push_warning("AudioManager: Music not found: ", track_key)
		return
	
	if fade_in > 0 and music_player.playing:
		_fade_out_music(fade_in)
		await get_tree().create_timer(fade_in * 0.5).timeout
	
	music_player.stream = audio
	music_player.volume_db = music_volume_db
	music_player.play()
	current_music = track_key
	music_changed.emit(track_key)


## Stop music with optional fade
func stop_music(fade_out: float = 0.5) -> void:
	if not music_player.playing:
		return
	
	if fade_out > 0:
		_fade_out_music(fade_out)
		await get_tree().create_timer(fade_out).timeout
		music_player.stop()
		music_player.volume_db = music_volume_db
	else:
		music_player.stop()
	
	current_music = ""
	music_changed.emit("")


func _fade_out_music(duration: float) -> void:
	var tween = create_tween()
	tween.tween_property(music_player, "volume_db", -80.0, duration)


# === AMBIENT ===

## Play looping ambient sound by key
func play_ambient(ambient_key: String, fade_in: float = 2.0) -> void:
	if ambient_key == current_ambient:
		return
	
	var audio_path = SFX_DIR + ambient_key + ".mp3"
	var audio = load(audio_path)
	
	if not audio:
		push_warning("AudioManager: Ambient not found: ", ambient_key)
		return
	
	if ambient_player.playing and fade_in > 0:
		var tween = create_tween()
		tween.tween_property(ambient_player, "volume_db", -80.0, fade_in * 0.5)
		await get_tree().create_timer(fade_in * 0.5).timeout
	
	ambient_player.stream = audio
	ambient_player.volume_db = ambient_volume_db
	ambient_player.play()
	current_ambient = ambient_key


## Stop ambient sound
func stop_ambient(fade_out: float = 1.0) -> void:
	if not ambient_player.playing:
		return
	
	var tween = create_tween()
	tween.tween_property(ambient_player, "volume_db", -80.0, fade_out)
	await get_tree().create_timer(fade_out).timeout
	ambient_player.stop()
	ambient_player.volume_db = ambient_volume_db
	current_ambient = ""


## Update ambient based on sanity level
func update_ambient_for_sanity(sanity: float) -> void:
	sanity_level = sanity
	
	if sanity > 0.7:
		# High sanity: unsettling sounds
		var key = LOW_SANITY_AMBIENT[randi() % LOW_SANITY_AMBIENT.size()]
		play_ambient(key)
	elif sanity > 0.3:
		# Medium sanity: mixed ambient
		var all_ambient = LOW_SANITY_AMBIENT + HIGH_SANITY_AMBIENT
		var key = all_ambient[randi() % all_ambient.size()]
		play_ambient(key)
	else:
		# Low sanity: normal ambient
		var key = HIGH_SANITY_AMBIENT[randi() % HIGH_SANITY_AMBIENT.size()]
		play_ambient(key)


# === SFX ===

## Play a sound effect by key
func play_sfx(sfx_key: String, volume_scale: float = 1.0) -> void:
	var audio_path = SFX_DIR + sfx_key + ".mp3"
	var audio = load(audio_path)
	
	if not audio:
		push_warning("AudioManager: SFX not found: ", sfx_key)
		return
	
	sfx_player.stream = audio
	sfx_player.volume_db = sfx_volume_db + linear_to_db(volume_scale)
	sfx_player.play()
	sfx_played.emit(sfx_key)


## Play a random SFX from a list of keys
func play_random_sfx(sfx_keys: Array, volume_scale: float = 1.0) -> void:
	var key = sfx_keys[randi() % sfx_keys.size()]
	play_sfx(key, volume_scale)


## Play a footstep SFX based on surface type
func play_footstep(surface: String = "default") -> void:
	match surface:
		"flesh", "wet":
			play_sfx("step_wet")
		"bone":
			play_sfx("step_bone")
		_:
			play_sfx("step_wet")


# === VOLUME ===

func set_music_volume(db: float) -> void:
	music_volume_db = db
	if music_player.playing:
		music_player.volume_db = db

func set_sfx_volume(db: float) -> void:
	sfx_volume_db = db

func set_voice_volume(db: float) -> void:
	voice_volume_db = db

func set_ambient_volume(db: float) -> void:
	ambient_volume_db = db
	if ambient_player.playing:
		ambient_player.volume_db = db


# === STATE ===

func get_music_keys() -> Array:
	return MUSIC_TRACKS.keys()

func get_sfx_keys() -> Array:
	return SFX_SOUNDS.keys()

func is_music_playing() -> bool:
	return music_player.playing

func get_current_music() -> String:
	return current_music

func get_current_ambient() -> String:
	return current_ambient
