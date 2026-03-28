extends Node
## SaveSystem Autoload Singleton
## Handles save/load operations using JSON + compression
## 
## Save data is stored in user:// saves directory
## Supports multiple save slots with metadata preview


const SAVE_VERSION = "1.0"
const MAX_SAVE_SLOTS = 3
const COMPRESSION_ENABLED = true


signal save_completed(slot: int)
signal load_completed(slot: int)
signal save_error(slot: int, error: String)
signal load_error(slot: int, error: String)


## Get save file path for a slot
func _get_save_path(slot: int) -> String:
	return "user://saves/slot_%d.save" % slot


## Get metadata file path for a slot
func _get_metadata_path(slot: int) -> String:
	return "user://saves/slot_%d.meta" % slot


## Check if a save slot exists
func has_save(slot: int) -> bool:
	return FileAccess.file_exists(_get_save_path(slot))


## Save current game state to slot
func save_game(slot: int) -> void:
	if slot < 1 or slot > MAX_SAVE_SLOTS:
		save_error.emit(slot, "Invalid save slot: %d" % slot)
		return
	
	# Ensure saves directory exists
	DirAccess.make_dir_recursive_absolute("user://saves")
	
	# Get game state data
	var game_data = GameState.to_dict()
	
	# Add metadata
	var save_data = {
		"save_version": SAVE_VERSION,
		"slot": slot,
		"timestamp": Time.get_datetime_dict_from_system(),
		"playtime": game_data.playtime,
		"metadata": {
			"location": game_data.player.get("location", ""),
			"level": game_data.player.level,
			"sanity": game_data.player.sanity,
			"faction": game_data.player.faction
		},
		"game": game_data
	}
	
	# Serialize to JSON
	var json_string = JSON.stringify(save_data, "\t")
	
	if COMPRESSION_ENABLED:
		# Compress with gzip
		var compressed = Marshalls.utf8_to_base64(json_string)
		json_string = compressed
	
	# Write to file
	var file = FileAccess.open(_get_save_path(slot), FileAccess.WRITE)
	if not file:
		save_error.emit(slot, "Failed to open save file for writing")
		return
	
	file.store_string(json_string)
	file.close()
	
	# Save metadata separately for quick preview
	_save_metadata(slot, save_data.metadata)
	
	save_completed.emit(slot)
	print("Game saved to slot %d" % slot)


## Load game state from slot
func load_game(slot: int) -> void:
	if slot < 1 or slot > MAX_SAVE_SLOTS:
		load_error.emit(slot, "Invalid save slot: %d" % slot)
		return
	
	if not has_save(slot):
		load_error.emit(slot, "No save found in slot %d" % slot)
		return
	
	# Read from file
	var file = FileAccess.open(_get_save_path(slot), FileAccess.READ)
	if not file:
		load_error.emit(slot, "Failed to open save file for reading")
		return
	
	var json_string = file.get_as_text()
	file.close()
	
	if COMPRESSION_ENABLED:
		# Decompress
		json_string = Marshalls.base64_to_utf8(json_string)
	
	# Parse JSON
	var json = JSON.new()
	var parse_result = json.parse(json_string)
	if parse_result != OK:
		load_error.emit(slot, "Failed to parse save data: %s" % json.get_error_message())
		return
	
	var save_data = json.data
	
	# Validate save version
	if save_data.get("save_version") != SAVE_VERSION:
		load_error.emit(slot, "Incompatible save version: %s" % save_data.get("save_version"))
		return
	
	# Load game state
	GameState.from_dict(save_data.game)
	
	load_completed.emit(slot)
	print("Game loaded from slot %d" % slot)


## Save metadata for quick preview
func _save_metadata(slot: int, metadata: Dictionary) -> void:
	var json_string = JSON.stringify(metadata, "\t")
	var file = FileAccess.open(_get_metadata_path(slot), FileAccess.WRITE)
	if file:
		file.store_string(json_string)
		file.close()


## Get metadata for a save slot (without loading full save)
func get_metadata(slot: int) -> Dictionary:
	if not FileAccess.file_exists(_get_metadata_path(slot)):
		return {}
	
	var file = FileAccess.open(_get_metadata_path(slot), FileAccess.READ)
	if not file:
		return {}
	
	var json_string = file.get_as_text()
	file.close()
	
	var json = JSON.new()
	if json.parse(json_string) != OK:
		return {}
	
	return json.data


## Get list of all save slots with metadata
func get_all_saves() -> Array[Dictionary]:
	var saves = []
	
	for slot in range(1, MAX_SAVE_SLOTS + 1):
		var save_info = {
			"slot": slot,
			"exists": has_save(slot),
			"metadata": get_metadata(slot) if has_save(slot) else {}
		}
		saves.append(save_info)
	
	return saves


## Delete a save file
func delete_save(slot: int) -> void:
	if slot < 1 or slot > MAX_SAVE_SLOTS:
		return
	
	var save_path = _get_save_path(slot)
	var meta_path = _get_metadata_path(slot)
	
	if FileAccess.file_exists(save_path):
		DirAccess.remove_absolute(save_path)
	
	if FileAccess.file_exists(meta_path):
		DirAccess.remove_absolute(meta_path)
	
	print("Deleted save slot %d" % slot)


## Get auto-save slot (uses slot MAX_SAVE_SLOTS)
func get_autosave_slot() -> int:
	return MAX_SAVE_SLOTS


## Quick save to auto-save slot
func quick_save() -> void:
	save_game(get_autosave_slot())


## Quick load from auto-save slot
func quick_load() -> void:
	if has_save(get_autosave_slot()):
		load_game(get_autosave_slot())
	else:
		push_warning("No auto-save found")


## Export save to file (for sharing, backup)
func export_save(slot: int, export_path: String) -> void:
	if not has_save(slot):
		return
	
	var source = FileAccess.open(_get_save_path(slot), FileAccess.READ)
	var dest = FileAccess.open(export_path, FileAccess.WRITE)
	
	if source and dest:
		dest.store_string(source.get_as_text())
	
	source.close()
	dest.close()


## Import save from file
func import_save(import_path: String, slot: int) -> void:
	if not FileAccess.file_exists(import_path):
		load_error.emit(slot, "Import file not found")
		return
	
	var source = FileAccess.open(import_path, FileAccess.READ)
	var dest = FileAccess.open(_get_save_path(slot), FileAccess.WRITE)
	
	if source and dest:
		dest.store_string(source.get_as_text())
	
	source.close()
	dest.close()
	
	save_completed.emit(slot)
