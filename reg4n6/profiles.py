#!/usr/bin/python
from reg4n6 import common
from reg4n6 import output

def profiles(cfg, hives):
	rows = [["ID", "Path", "Last Load", "Key Last Write"]]
	if "software" in hives.keys():
		for subkey in common.safe_open(hives["software"], "Microsoft\Windows NT\CurrentVersion\ProfileList").subkeys():
			vals = {}
			vals["ID"] = subkey.name()
			vals["Path"] = subkey.value("ProfileImagePath").value()
			vals["Key Last Write"] = subkey.timestamp().strftime('%a %b %d %Y %H:%M:%S UTC')
			try:
				a = subkey.value("ProfileLoadTimeLow").value()
				b = subkey.value("ProfileLoadTimeHigh").value()
				if a and b:
					a = struct.pack('II', a, b)
					vals["Last Load"] = common.decode_filetime(a)
			except:
				pass
			output.dict_to_arr(rows, vals)
	output.write_out(cfg, rows, "Local Profiles", 1)
