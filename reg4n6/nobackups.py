#!/usr/bin/python
from reg4n6 import common
from reg4n6 import output

def nobackups(cfg, hives):
	if "system" in hives.keys():
		if "cset" not in cfg.keys():
			cfg['cset'] = common.get_control_set(hives['system'])
		for subkey in common.safe_open(hives['system'], "ControlSet00%s\Control\BackupRestore"%cfg["cset"]).subkeys():
			exs = [["Name", "Value"]]
			if subkey.name() == "FilesNotToBackup":
				ex_name = "Files not to backup"
			elif subkey.name() == "FilesNotToSnapshot":
				ex_name = "Files not to snapshot"
			elif subkey.name() == "KeysNotToRestore":
				ex_name = "Keys not to restore"
			else:
				continue
			for value in subkey.values():
				# Print a row for each reg_multi_sz string
				vals = {"Name":value.name()}
				for i, ex in enumerate(value.value()):
					if len(ex):
						vals["Value"] = ex
						output.dict_to_arr(exs, vals)
			if len(exs) > 1:
				rows = [["Last write"],[subkey.timestamp().strftime('%a %b %d %Y %H:%M:%S UTC')]]
				output.write_out(cfg, rows, ex_name)
				output.write_out(cfg, exs, "", 1)
