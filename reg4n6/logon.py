#!/usr/bin/python

from reg4n6 import output
from reg4n6 import common

def logon(cfg, hives):
	rows=[['Default Domain', 'Default Username', 'Last Username', 'Shell', 'Userinit', 'Start Options', 'Firmware Part', 'System Part']]
	vals = {}
	if "software" in hives.keys():
			vals["Userinit"] = common.safe_open(hives["software"], "Microsoft\Windows NT\CurrentVersion\Winlogon", "Userinit").value()
			vals["Shell"] = common.safe_open(hives["software"], "Microsoft\Windows NT\CurrentVersion\Winlogon", "Shell").value()
			vals["Default Username"] = common.safe_open(hives["software"], "Microsoft\Windows NT\CurrentVersion\Winlogon", "DefaultUserName").value()
			vals["Default Domain"] = common.safe_open(hives["software"], "Microsoft\Windows NT\CurrentVersion\Winlogon", "DefaultDomainName").value()
			vals["Last Username"] = common.safe_open(hives["software"], "Microsoft\Windows NT\CurrentVersion\Winlogon", "LastUsedUsername").value()
	if "system" in hives.keys():
		if "cset" not in cfg.keys():
			cfg["cset"] = common.get_control_set(hives['system'])
		vals["Start Options"] = common.safe_open(hives["system"], "ControlSet00%s\Control"%cfg['cset'], "SystemStartOptions").value()
		vals["Firmware Part"] = common.safe_open(hives["system"], "ControlSet00%s\Control"%cfg['cset'], "FirmwareBootDevice").value()
		vals["System Part"] = common.safe_open(hives["system"], "ControlSet00%s\Control"%cfg['cset'], "SystemBootDevice").value()
	output.dict_to_arr(rows, vals)
	output.write_out(cfg, rows, "Startup/Winlogon")
