extends Node
## SanityManager Autoload Singleton
## Manages psychosis mechanics, hallucinations, and sanity effects
## 
## The sanity system affects:
## - Visual/audio perception (hallucinations)
## - Available dialogue options
## - Combat abilities and vulnerabilities
## - Story progression and endings

signal sanity_threshold_crossed(threshold: String)
signal hallucination_started(hallucination_id: String)
signal hallucination_ended(hallucination_id: String)

# Sanity thresholds (0.0 to 1.0)
const THRESHOLD_INSANE = 0.2
const THRESHOLD_UNSTABLE = 0.4
const THRESHOLD_FLUCTUATING = 0.6
const THRESHOLD_STABLE = 0.8
const THRESHOLD_SANE = 1.0

# Hallucination categories
enum HallucinationType {
	VISUAL,      # See things that aren't there
	AUDITORY,    # Hear whispers, sounds
	INTERACTIVE, # Can interact with illusions
	ENVIRONMENTAL # World distortions
}

# Active hallucinations
var active_hallucinations: Array[String] = []
var hallucination_intensity: float = 0.0

# Sanity loss/gain tracking
var sanity_loss_total: float = 0.0
var sanity_gain_total: float = 0.0
var consecutive_sanity_losses: int = 0

# Thresholds already crossed (for one-time events)
var crossed_thresholds: Array[String] = []


func _ready() -> void:
	# Connect to GameState sanity changes
	GameState.sanity_changed.connect(_on_sanity_changed)


## Get current sanity status label
func get_sanity_status() -> String:
	var sanity = GameState.player_sanity
	
	if sanity <= THRESHOLD_INSANE:
		return "Insane"
	elif sanity <= THRESHOLD_UNSTABLE:
		return "Unstable"
	elif sanity <= THRESHOLD_FLUCTUATING:
		return "Fluctuating"
	elif sanity <= THRESHOLD_STABLE:
		return "Stable"
	else:
		return "Sane"


## Get sanity status color for UI
func get_sanity_color() -> Color:
	var sanity = GameState.player_sanity
	
	if sanity <= THRESHOLD_INSANE:
		return Color(0.9, 0.1, 0.1)  # Deep red
	elif sanity <= THRESHOLD_UNSTABLE:
		return Color(0.9, 0.5, 0.1)  # Orange-red
	elif sanity <= THRESHOLD_FLUCTUATING:
		return Color(0.9, 0.9, 0.1)  # Yellow
	elif sanity <= THRESHOLD_STABLE:
		return Color(0.3, 0.8, 0.5)  # Green-blue
	else:
		return Color(0.2, 0.9, 0.3)  # Bright green


## Apply sanity damage (from events, combat, exposure)
func apply_sanity_damage(amount: float, source: String = "") -> void:
	var actual_amount = amount * _get_sanity_resistance_multiplier()
	GameState.modify_sanity(-actual_amount)
	
	sanity_loss_total += actual_amount
	consecutive_sanity_losses += 1
	
	# Check for threshold crossings
	_check_thresholds()
	
	# Trigger hallucinations at low sanity
	if GameState.player_sanity < THRESHOLD_UNSTABLE:
		_maybe_trigger_hallucination()


## Restore sanity (from abilities, items, rest)
func restore_sanity(amount: float, source: String = "") -> void:
	var actual_amount = amount * _get_sanity_recovery_multiplier()
	GameState.modify_sanity(actual_amount)
	
	sanity_gain_total += actual_amount
	consecutive_sanity_losses = 0


## Check if a specific hallucination is active
func is_hallucination_active(hallucination_id: String) -> bool:
	return hallucination_id in active_hallucinations


## Start a hallucination effect
func start_hallucination(hallucination_id: String, intensity: float = 1.0) -> void:
	if hallucination_id in active_hallucinations:
		return
	
	active_hallucinations.append(hallucination_id)
	hallucination_intensity = max(hallucination_intensity, intensity)
	hallucination_started.emit(hallucination_id)
	
	print("Hallucination started: ", hallucination_id)


## End a hallucination effect
func end_hallucination(hallucination_id: String) -> void:
	if hallucination_id not in active_hallucinations:
		return
	
	active_hallucinations.erase(hallucination_id)
	hallucination_ended.emit(hallucination_id)
	
	# Recalculate intensity
	if active_hallucinations.is_empty():
		hallucination_intensity = 0.0


## End all hallucinations
func clear_hallucinations() -> void:
	active_hallucinations.clear()
	hallucination_intensity = 0.0


## Get hallucination intensity (0.0 to 1.0)
func get_hallucination_intensity() -> float:
	return hallucination_intensity


## Check if player can access sanity-gated content
func can_access_content(required_sanity: float) -> bool:
	return GameState.player_sanity >= required_sanity


## Get sanity-based dialogue modifiers
func get_dialogue_modifiers() -> Array[String]:
	var modifiers = []
	var sanity = GameState.player_sanity
	
	if sanity <= THRESHOLD_INSANE:
		modifiers.append("delusional")
		modifiers.append("paranoid")
	elif sanity <= THRESHOLD_UNSTABLE:
		modifiers.append("unstable")
		modifiers.append("anxious")
	elif sanity <= THRESHOLD_FLUCTUATING:
		modifiers.append("distracted")
	
	return modifiers


## Calculate combat sanity bonus/penalty
func get_combat_modifier() -> float:
	var sanity = GameState.player_sanity
	
	# Low sanity: damage bonus but accuracy penalty
	if sanity <= THRESHOLD_INSANE:
		return 1.3  # 30% damage boost
	elif sanity <= THRESHOLD_UNSTABLE:
		return 1.15  # 15% damage boost
	elif sanity >= THRESHOLD_STABLE:
		return 0.9  # 10% penalty for being too sane (cautious)
	
	return 1.0  # No modifier


## Trigger sanity-based event
func trigger_sanity_event(event_type: String) -> void:
	var sanity = GameState.player_sity
	
	match event_type:
		"combat_start":
			if sanity <= THRESHOLD_UNSTABLE:
				start_hallucination("enemy_multiplication", 0.5)
		"exploration":
			if sanity <= THRESHOLD_INSANE:
				start_hallucination("false_path", 0.7)
		"dialogue":
			if sanity <= THRESHOLD_FLUCTUATING:
				start_hallucination("whispered_advice", 0.3)


func _on_sanity_changed(new_sanity: float) -> void:
	# Update hallucination intensity based on sanity level
	if new_sanity <= THRESHOLD_UNSTABLE:
		hallucination_intensity = max(0.5, 1.0 - new_sanity)
	else:
		hallucination_intensity = 0.0
		clear_hallucinations()


func _check_thresholds() -> void:
	var sanity = GameState.player_sanity
	var thresholds = [
		{"name": "insane", "value": THRESHOLD_INSANE},
		{"name": "unstable", "value": THRESHOLD_UNSTABLE},
		{"name": "fluctuating", "value": THRESHOLD_FLUCTUATING},
		{"name": "stable", "value": THRESHOLD_STABLE}
	]
	
	for threshold in thresholds:
		if sanity <= threshold.value and threshold.name not in crossed_thresholds:
			crossed_thresholds.append(threshold.name)
			sanity_threshold_crossed.emit(threshold.name)
			_on_threshold_crossed(threshold.name)


func _on_threshold_crossed(threshold_name: String) -> void:
	# Trigger one-time events for threshold crossings
	print("Sanity threshold crossed: ", threshold_name)
	
	match threshold_name:
		"insane":
			start_hallucination("reality_break", 1.0)
		"unstable":
			start_hallucination("peripheral_movement", 0.4)


func _maybe_trigger_hallucination() -> void:
	var sanity = GameState.player_sanity
	var chance = 0.0
	
	if sanity <= THRESHOLD_INSANE:
		chance = 0.3  # 30% chance per sanity hit
	elif sanity <= THRESHOLD_UNSTABLE:
		chance = 0.15  # 15% chance
	
	if randf() < chance:
		var hallucination = _get_random_hallucination()
		if hallucination:
			start_hallucination(hallucination, 0.5)


func _get_random_hallucination() -> String:
	var options = []
	
	if GameState.player_sanity <= THRESHOLD_INSANE:
		options = ["reality_break", "false_npcs", "impossible_geometry", "time_skip"]
	elif GameState.player_sanity <= THRESHOLD_UNSTABLE:
		options = ["peripheral_movement", "whispers", "face_distortion", "blood_trails"]
	
	if options.is_empty():
		return ""
	
	return options[randi() % options.size()]


func _get_sanity_resistance_multiplier() -> float:
	# TODO: Factor in equipment, buffs, faction bonuses
	var multiplier = 1.0
	
	# Example: Certain items reduce sanity damage
	# if GameState.has_equipment("mindward_amulet"):
	#     multiplier *= 0.7
	
	return multiplier


func _get_sanity_recovery_multiplier() -> float:
	# TODO: Factor in equipment, location, faction bonuses
	var multiplier = 1.0
	
	# Example: Resting in safe locations boosts recovery
	# if GameState.current_location.is_safe_zone:
	#     multiplier *= 1.5
	
	return multiplier


## Get sanity tutorial hints
func get_tutorial_hints() -> Array[String]:
	var hints = []
	var sanity = GameState.player_sanity
	
	if sanity > THRESHOLD_STABLE:
		hints.append("Your sanity is stable. Explore without fear.")
	elif sanity > THRESHOLD_FLUCTUATING:
		hints.append("Minor disturbances detected. Monitor your mental state.")
	elif sanity > THRESHOLD_UNSTABLE:
		hints.append("Hallucinations may occur. Seek purification or embrace the madness.")
	else:
		hints.append("Reality is fragmenting. Your choices shape what remains.")
	
	return hints
