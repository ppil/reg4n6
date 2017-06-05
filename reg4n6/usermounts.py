#!/usr/bin/python
from reg4n6 import common
from reg4n6 import output

def usermounts(cfg, hives, user_hives):
	for username, uhive in user_hives.iteritems():
		rows = [["Volume GUID", "Last Mounted", "Mount Point", "Nuke on Delete"]]
		for mpkey in common.safe_open(uhive, "Software\Microsoft\Windows\CurrentVersion\Explorer\MountPoints2").subkeys():
			vals = {"Volume GUID":mpkey.name()}
			vals["Last Mounted"] = mpkey.timestamp().strftime('%a %b %d %Y %H:%M:%S UTC')
			# Find NukeOnDelete
			volbb = common.find_keys_name(common.safe_open(uhive, "Software\Microsoft\Windows\CurrentVersion\Explorer\BitBucket\Volume"), mpkey.name(), 1)
			if volbb:
				bbkey = common.safe_open(uhive, volbb[0])
				if bbkey.name() and bbkey.value("NukeOnDelete").value():
					vals["Nuke on Delete"] = "Yes"
				elif bbkey.name():
					vals["Nuke on Delete"] = "No"
			# Find mount point
			if "system" in hives.keys():
				for point in hives["system"].open("MountedDevices").values():
					if mpkey.name() in point.name():
						keys = common.find_value_names(hives["system"].open("MountedDevices"), point.value())
						for key in keys:
							valname = key.split('\\')[-1]
							ptname = point.name().split('\\')[-1]
							if valname != ptname:
								vals["Mount Point"] = key
						break
			output.dict_to_arr(rows, vals)
		output.write_out(cfg, rows, "User Mounts - %s"%username, 1)
