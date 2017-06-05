#!/usr/bin/python

from reg4n6 import common
from reg4n6 import output


# Installed software
def uninstalls(cfg, hives):
	if "software" in hives.keys():
		rows = [["Publisher", "Name", "Version", "Installed", "Install Src", "Install Dst"]]
		keys = common.safe_open(hives["software"], "Microsoft\Windows\CurrentVersion\Uninstall").subkeys() + common.safe_open(hives["software"], "Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall").subkeys()
		for key in common.find_keys_name(common.safe_open(hives['software'], "Microsoft\Windows\CurrentVersion\Installer\UserData"), "InstallProperties", 3):
			keys.append(common.safe_open(hives['software'], key))
		for uninstall in keys:
			vals = {}
			vals["Installed"] = uninstall.timestamp().strftime('%a %b %d %Y %H:%M:%S UTC')
			for val in uninstall.values():
				if val.name() == "DisplayName":
					vals["Name"] = common.unicode_to_ascii(val.value())
				elif val.name() == "DisplayVersion":
					vals["Version"] = common.unicode_to_ascii(val.value())
				elif val.name() == "Publisher":
					vals["Publisher"] = common.unicode_to_ascii(val.value())
				elif val.name() == "InstallSource":
					vals["Install Src"] = common.unicode_to_ascii(val.value())
				elif val.name() == "InstallLocation":
					vals["Install Dst"] = common.unicode_to_ascii(val.value())
			# Skip subkeys with no relevant values
			if "Name" not in vals.keys() and "Version" not in vals.keys() and "Install Dst" not in vals.keys():
				continue
			output.dict_to_arr(rows, vals)
		dedup(rows)
		rows = output.sort_by_col(rows, "Name")
		output.write_out(cfg, rows, "Software", 1)

# If name, version, and install dst match: delete row (UserData overlap)
def dedup(rows):
	# For each row
	for i, row in enumerate(rows):
		# Compare against rows with higher indices
		for j, row2 in enumerate(rows[i+1:]):
			if row[1] == row2[1] and row[2] == row2[2] and row[5] == row2[5]:
				del rows[i+1+j]
	return rows
