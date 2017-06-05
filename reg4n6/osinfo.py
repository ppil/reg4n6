#!/usr/bin/python
from reg4n6 import common
from reg4n6 import output

def osinfo(cfg, hives):
	if "software" in hives.keys():
		rows =[["Registered Owner", "Registered Org", "Operating System", "Service Pack", "Product ID", "Install Type", "Install Date", "Build String (ext)", "Install Path", "Source Path"]]
		pairs={}
		for value in common.safe_open(hives["software"], "Microsoft\Windows NT\CurrentVersion").values():
			if value.name() == "ProductName":
				pairs["Operating System"] = value.value()
			elif value.name() == "CSDVersion":
				pairs["Service Pack"] = value.value()
			elif value.name() == "BuildLabEx":
				pairs["Build String (ext)"] = value.value()
			elif value.name() == "InstallDate":
				pairs["Install Date"] = common.decode_epoch(value.value())
			elif value.name() == "ProductId":
				pairs["Product ID"] = value.value()
			elif value.name() == "RegisteredOwner":
				pairs["Registered Owner"] = value.value()
			elif value.name() == "RegisteredOrganization":
				pairs["Registered Org"] = value.value()
			elif value.name() == "PathName":
				pairs["Install Path"] = value.value()
			elif value.name() == "SourcePath":
				pairs["Source Path"] = value.value()
			elif value.name() == "InstallationType":
				pairs["Install Type"] = value.value()
			elif value.name() == "":
				pairs[""] = value.value()
		output.dict_to_arr(rows, pairs)
		output.write_out(cfg, rows, "OS Info")
