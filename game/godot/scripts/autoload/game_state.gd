extends Node
## GameState Autoload Singleton
## Manages global game state, player data, and world flags
## 
## The GameState persists across scene changes and tracks:
## - Player stats, inventory, equipment
## - World exploration progress
## - Quest states and objectives
## - Story flags and key decisions

signal sanity_changed(new_value: float)
signal health_changed(new_value: int)
signal faction_changed(faction_id: String)
signal flag_changed(flag_name: String, value: Variant)

# Player core stats
var player_level: int = 1
var player_experience: int = 0
var player_health: int = 100
var player_max_health: int = 100
var player_sanity: float = 1.0  # 1.0 = fully sane, 0.0 = complete psychosis
var player_sanity_max: float = 1.0

# Character build
var player_class: String = ""
var player_faction: String = "council"  # Default: Sane Council
var player_stats: Dictionary = {
	"strength": 5,
	"dexterity": 5,
	"intelligence": 5,
	"willpower": 5
}

# World state
var current_location: String = "withered_hand_start"
var discovered_locations: Array[String] = []
var world_flags: Dictionary = {}  # Story progression, key events

# Quest tracking
var active_quests: Array[Dictionary] = []
var completed_quests: Array[String] = []

# Inventory (simplified - full system in resources/)
var inventory: Array[Dictionary] = []
var equipment: Dictionary = {
	"head": null,
	"chest": null,
	"legs": null,
	"weapon": null,
	"accessory": null
}

# Faction reputations (-100 to 100)
var faction_reputation: Dictionary = {
	"purified": 0,
	"rotborn": 0,
	"council": 10,  # Start slightly favorable
	"prophets": 0
}

# Game metadata
var playtime_seconds: float = 0.0
var save_slot: int = 1


func _ready() -> void:
	# GameState persists across scene changes
	pass


## Modify sanity and emit signal
## Positive delta = gain sanity, negative = lose sanity
func modify_sanity(delta: float) -> void:
	player_sanity = clamp(player_sanity + delta, 0.0, player_sanity_max)
	sanity_changed.emit(player_sanity)


## Modify health and emit signal
func modify_health(delta: int) -> void:
	player_health = clamp(player_health + delta, 0, player_max_health)
	health_changed.emit(player_health)


## Set faction reputation
## faction_id: "purified", "rotborn", "council", "prophets"
func set_faction_reputation(faction_id: String, value: int) -> void:
	value = clamp(value, -100, 100)
	faction_reputation[faction_id] = value
	faction_changed.emit(faction_id)


## Modify faction reputation
func modify_faction_reputation(faction_id: String, delta: int) -> void:
	if faction_id in faction_reputation:
		set_faction_reputation(faction_id, faction_reputation[faction_id] + delta)


## Get faction with highest reputation
func get_dominant_faction() -> String:
	var best_faction: String = "council"
	var best_value: int = -101
	
	for faction in faction_reputation:
		if faction_reputation[faction] > best_value:
			best_value = faction_reputation[faction]
			best_faction = faction
	
	return best_faction


## Set a world flag
func set_flag(flag_name: String, value: Variant) -> void:
	world_flags[flag_name] = value
	flag_changed.emit(flag_name, value)


## Get a world flag (returns default_value if not set)
func get_flag(flag_name: String, default_value: Variant = null) -> Variant:
	return world_flags.get(flag_name, default_value)


## Check if a location has been discovered
func is_location_discovered(location_id: String) -> bool:
	return location_id in discovered_locations


## Mark a location as discovered
func discover_location(location_id: String) -> void:
	if not is_location_discovered(location_id):
		discovered_locations.append(location_id)


## Add experience points
func add_experience(amount: int) -> void:
	player_experience += amount
	# TODO: Implement level-up logic


## Serialize game state for saving
func to_dict() -> Dictionary:
	return {
		"version": "1.0",
		"timestamp": Time.get_unix_time_from_system(),
		"playtime": playtime_seconds,
		"player": {
			"level": player_level,
			"experience": player_experience,
			"health": player_health,
			"max_health": player_max_health,
			"sanity": player_sanity,
			"class": player_class,
			"faction": player_faction,
			"stats": player_stats
		},
		"world": {
			"location": current_location,
			"discovered": discovered_locations,
			"flags": world_flags
		},
		"quests": {
			"active": active_quests,
			"completed": completed_quests
		},
		"inventory": inventory,
		"equipment": equipment,
		"factions": faction_reputation
	}


## Load game state from dictionary
func from_dict(data: Dictionary) -> void:
	if "player" in data:
		var p = data.player
		player_level = p.get("level", 1)
		player_experience = p.get("experience", 0)
		player_health = p.get("health", 100)
		player_max_health = p.get("max_health", 100)
		player_sanity = p.get("sanity", 1.0)
		player_class = p.get("class", "")
		player_faction = p.get("faction", "council")
		player_stats = p.get("stats", player_stats)
	
	if "world" in data:
		var w = data.world
		current_location = w.get("location", "")
		discovered_locations = w.get("discovered", [])
		world_flags = w.get("flags", {})
	
	if "quests" in data:
		var q = data.quests
		active_quests = q.get("active", [])
		completed_quests = q.get("completed", [])
	
	if "inventory" in data:
		inventory = data.inventory
	
	if "equipment" in data:
		equipment = data.equipment
	
	if "factions" in data:
		faction_reputation = data.factions
	
	playtime_seconds = data.get("playtime", 0.0)
