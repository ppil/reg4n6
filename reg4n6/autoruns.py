#!/usr/bin/python

from reg4n6 import common
from reg4n6 import output

def autoruns(cfg, hives, user_hives):
	rows=[['Source', 'Name', 'Run Value']]
	keys = ["Run", "RunOnce", "RunOnceEx"]
	if "software" in hives.keys():
		for key in keys:
			for run in common.safe_open(hives["software"], "Microsoft\Windows\CurrentVersion\%s"%key).values():
				vals = {"Source":"Software:%s"%key}
				vals["Name"] = run.name()
				vals["Run Value"] = run.value()
				output.dict_to_arr(rows, vals)
	for username, uhive in user_hives.iteritems():
		for key in keys:
			for run in common.safe_open(uhive, "Software\Microsoft\Windows\CurrentVersion\%s"%key).values():
				vals = {"Source":"%s:%s"%(username, key)}
				vals["Name"] = run.name()
				vals["Run Value"] = run.value()
				output.dict_to_arr(rows, vals)
	output.write_out(cfg, rows, "Autoruns", 1)
