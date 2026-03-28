extends Node
## FactionManager Autoload Singleton
## Manages faction reputations, quests, and allegiances
## 
## The four major factions:
## - Purified: Seek to cleanse the rot
## - Rotborn Embrace: Worship the decay
## - Sane Council: Maintain rational governance
## - Spore Prophets: Interpret the god's dreams

signal faction_reputation_changed(faction_id: String, new_value: int)
signal faction_alignment_changed(new_faction: String)

enum FactionID {
	PURIFIED = 0,
	ROTBORN = 1,
	COUNCIL = 2,
	PROPHETS = 3
}

const FACTION_NAMES = {
	"purified": "The Purified",
	"rotborn": "Rotborn Embrace",
	"council": "The Sane Council",
	"prophets": "Spore Prophets"
}

const FACTION_COLORS = {
	"purified": Color(0.8, 0.85, 0.9, 1.0),  # Pale blue-white
	"rotborn": Color(0.7, 0.3, 0.3, 1.0),     # Blood red
	"council": Color(0.6, 0.65, 0.7, 1.0),    # Slate gray
	"prophets": Color(0.4, 0.7, 0.4, 1.0)     # Spore green
}

# Reputation thresholds
const THRESHOLD_HOSTILE = -75
const THRESHOLD_UNFRIENDLY = -25
const THRESHOLD_NEUTRAL = 25
const THRESHOLD_FAVORABLE = 75


func _ready() -> void:
	pass


## Get display name for faction
func get_faction_name(faction_id: String) -> String:
	return FACTION_NAMES.get(faction_id, "Unknown")


## Get faction color for UI
func get_faction_color(faction_id: String) -> Color:
	return FACTION_COLORS.get(faction_id, Color.WHITE)


## Get reputation status label
func get_reputation_status(reputation: int) -> String:
	if reputation <= THRESHOLD_HOSTILE:
		return "Hostile"
	elif reputation <= THRESHOLD_UNFRIENDLY:
		return "Unfriendly"
	elif reputation <= THRESHOLD_NEUTRAL:
		return "Neutral"
	elif reputation <= THRESHOLD_FAVORABLE:
		return "Favorable"
	else:
		return "Allied"


## Get reputation color for UI
func get_reputation_color(reputation: int) -> Color:
	if reputation <= THRESHOLD_HOSTILE:
		return Color(0.9, 0.2, 0.2)  # Red
	elif reputation <= THRESHOLD_UNFRIENDLY:
		return Color(0.9, 0.6, 0.2)  # Orange
	elif reputation <= THRESHOLD_NEUTRAL:
		return Color(0.9, 0.9, 0.2)  # Yellow
	elif reputation <= THRESHOLD_FAVORABLE:
		return Color(0.2, 0.7, 0.9)  # Light blue
	else:
		return Color(0.2, 0.9, 0.5)  # Green


## Check if player can access faction area
func can_access_faction_area(faction_id: String) -> bool:
	var reputation = GameState.faction_reputation.get(faction_id, 0)
	# Hostile factions block access
	return reputation > THRESHOLD_HOSTILE


## Check if faction quest is available
func is_quest_available(quest_faction: String, quest_id: String) -> bool:
	# Check if already completed
	if quest_id in GameState.completed_quests:
		return false
	
	# Check reputation requirement (default: not hostile)
	var reputation = GameState.faction_reputation.get(quest_faction, 0)
	return reputation > THRESHOLD_HOSTILE


## Get available faction quests
func get_available_quests(faction_id: String) -> Array[Dictionary]:
	# TODO: Query quest database for faction-specific quests
	var available = []
	
	if not is_quest_available(faction_id, ""):
		return available
	
	# Placeholder - actual quest data from resources/
	return available


## Award faction reputation bonus (for quests, events)
func award_reputation(faction_id: String, base_amount: int, multiplier: float = 1.0) -> void:
	var amount = int(base_amount * multiplier)
	GameState.modify_faction_reputation(faction_id, amount)
	faction_reputation_changed.emit(faction_id, GameState.faction_reputation[faction_id])


## Check faction-specific dialogue options
func get_faction_dialogue_options(faction_id: String, base_options: Array) -> Array:
	var reputation = GameState.faction_reputation.get(faction_id, 0)
	var available_options = []
	
	for option in base_options:
		var req_rep = option.get("required_reputation", THRESHOLD_HOSTILE)
		if reputation >= req_rep:
			available_options.append(option)
	
	return available_options


## Get player's dominant faction alignment
func get_player_alignment() -> String:
	return GameState.get_dominant_faction()


## Check if player is aligned with a specific faction
func is_aligned_with(faction_id: String) -> bool:
	return get_player_alignment() == faction_id


## Get all faction relationships (for diplomacy system)
func get_faction_relationships() -> Dictionary:
	# TODO: Define faction inter-relationships
	# Example: Purified hate Rotborn, Council tolerates all, etc.
	return {
		"purified": {
			"rotborn": -100,    # Holy enemies
			"council": -20,     # Disapprove of compromise
			"prophets": -50     # See as heretics
		},
		"rotborn": {
			"purified": -100,   # Holy enemies
			"council": -30,     # See as blind
			"prophets": 20      # Respect visions
		},
		"council": {
			"purified": 10,     # Allies of convenience
			"rotborn": -40,     # See as dangerous
			"prophets": 0       # Tolerate
		},
		"prophets": {
			"purified": -30,    # See as closed-minded
			"rotborn": 10,      # Share mystical leanings
			"council": 0        # Neutral
		}
	}


## Calculate effective reputation (with relationship modifiers)
func get_effective_reputation(faction_id: String) -> int:
	var base_rep = GameState.faction_reputation.get(faction_id, 0)
	
	# TODO: Apply relationship modifiers from other factions
	# Example: If allied with Purified, Rotborn rep decreases
	
	return base_rep
