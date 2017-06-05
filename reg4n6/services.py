#!/usr/bin/python

from reg4n6 import common
from reg4n6 import output

def services(cfg, hives):
	rows = [["Name", "Type", "Start", "Error Control", "Group", "Service Dll", "Display Name", "Image Path"]]
	if "system" in hives.keys():
		if "cset" not in cfg.keys():
			cfg["cset"] = common.get_control_set(hives['system'])
		for svc in common.safe_open(hives["system"], "ControlSet00%s\Services"%cfg['cset']).subkeys():
			vals = {}
			keypath = '\\'.join(svc.path().split('\\')[1:])
			vals["Name"] = svc.name()
			# http://windowsitpro.com/windows-server/jsi-tip-0324-registry-entries-services
			# http://nt4ref.zcm.com.au/mansd.htm
			vals["Type"] = common.safe_open(hives["system"], keypath, "Type").value()
			if vals["Type"] != '':
				if vals["Type"] == 0x1:
					vals["Type"] = "Kernel-mode Driver"
				elif vals["Type"] == 0x2:
					vals["Type"] = "Filesystem Driver"
				elif vals["Type"] == 0x4:
					vals["Type"] = "Argument Group"
				elif vals["Type"] == 0x10:
					vals["Type"] = "Win32 Dedicated"
				elif vals["Type"] == 0x20:
					vals["Type"] = "Win32 Shared"
				elif vals["Type"] == 0x110:
					vals["Type"] = "Win32 Dedicated Interactive"
				elif vals["Type"] == 0x120:
					vals["Type"] = "Win32 Shared Interactive"
				else:
					vals["Type"] = "Unknown: 0x%x"%int(vals["Type"])
			vals["Start"] = common.safe_open(hives["system"], keypath, "Start").value()
			if vals["Start"] != '':
				if vals["Start"] == 0x0:
					vals["Start"] = "Boot"
				elif vals["Start"] == 0x1:
					vals["Start"] = "System"
				elif vals["Start"] == 0x2:
					vals["Start"] = "Automatic"
				elif vals["Start"] == 0x3:
					vals["Start"] = "Manual"
				elif vals["Start"] == 0x4:
					vals["Start"] = "Disabled"
				else:
					vals["Start"] = "Unknown: 0x%x"%int(vals["Start"])
			vals["Error Control"] = common.safe_open(hives["system"], keypath, "ErrorControl").value()
			if vals["Error Control"] != '':
				if vals["Error Control"] == 0x0:
					vals ["Error Control"] = "Ignore"
				elif vals["Error Control"] == 0x1:
					vals ["Error Control"] = "Normal"
				elif vals["Error Control"] == 0x2:
					vals ["Error Control"] = "Severe"
				elif vals["Error Control"] == 0x3:
					vals ["Error Control"] = "Critical"
				else:
					vals["Error Control"] = "Unknown: 0x%x"%int(vals["Error Control"])
			vals["Image Path"]  = common.multi_string(common.safe_open(hives["system"], keypath, "ImagePath"))
			vals["Group"]  = common.safe_open(hives["system"], keypath, "Group").value()
			vals["Display Name"]  = common.safe_open(hives["system"], keypath, "DisplayName").value()
			vals["Service Dll"]  = common.safe_open(hives["system"], "%s\Parameters"%(keypath), "ServiceDll").value()
			output.dict_to_arr(rows, vals)
	output.write_out(cfg, rows, "Services", 1)
