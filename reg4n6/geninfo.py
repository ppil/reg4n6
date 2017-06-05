#!/usr/bin/python
from reg4n6 import output
from reg4n6 import common

def geninfo(cfg, hives):
	if "system" in hives.keys():
		if "cset" not in cfg.keys():
			cfg["cset"] = common.get_control_set(hives['system'])
		rows = [["Hostname", "Last Shutdown"]]
		pairs={}
		pairs["Hostname"] = common.safe_open(hives['system'], "ControlSet00%s\\Services\\Tcpip\\Parameters"%cfg['cset'], "Hostname").value()
		ft = common.safe_open(hives['system'],"ControlSet00%s\\Control\\Windows"%cfg['cset'],"ShutdownTime").value()
		pairs["Last Shutdown"] = common.decode_filetime(ft)
		output.dict_to_arr(rows, pairs)
		output.write_out(cfg, rows, "General Info")
