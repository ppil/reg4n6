#!/usr/bin/python

from reg4n6 import common
from reg4n6 import output

def sessionmgr(cfg, hives):
	if "system" in hives.keys():
		if "cset" not in cfg.keys():
			cfg['cset'] = common.get_control_set(hives['system'])
		# Pending file ops
		rows = [["Source", "Destination"]]
		#https://forensicatorj.wordpress.com/2014/06/25/interpreting-the-pendingfilerenameoperations-registry-key-for-forensics/
		ops = common.safe_open(hives["system"], "ControlSet00%s\Control\Session Manager"%cfg['cset'], "PendingFileRenameOperations").value()
		i=0
		while i < len(ops):
			if ops[i]:
				vals = {"Source":ops[i]}
				if ops[i+2]:
					vals["Destination"] = ops[i+2]
				elif ops[i+1] == '' and ops[i+2] == '':
					vals["Destination"] = "Delete"
				output.dict_to_arr(rows, vals)
			i+=4
		output.write_out(cfg, rows, "Pending File Renames", 1)
		# Environment vars
		rows = [["Name", "Value"]]
		for var in common.safe_open(hives["system"], "ControlSet00%s\Control\Session Manager\Environment"%cfg['cset']).values():
			vals={}
			vals["Name"] = var.name()
			vals["Value"] = common.multi_string(var)
			output.dict_to_arr(rows, vals)
		output.write_out(cfg, rows, "System Environment Variables", 1)
