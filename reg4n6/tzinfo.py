#!/usr/bin/python
from reg4n6 import common
from reg4n6 import output

def tzinfo(cfg, hives):
	if "system" in hives.keys():
		if "cset" not in cfg.keys():
			cfg["cset"] = common.get_control_set(hives['system'])
		rows =[["Timezone name", "Active bias", "Bias", "Standard bias", "Daylight bias"]]
		pairs={}
		for value in common.safe_open(hives["system"], "ControlSet00%s\Control\TimeZoneInformation"%cfg['cset']).values():
			if value.name() == "TimeZoneKeyName":
				pairs["Timezone name"] = value.value()
			if value.name() == "ActiveTimeBias":
				pairs["Active bias"] = utc_bias(value.value())
			if value.name() == "Bias":
				pairs["Bias"] = utc_bias(value.value())
			if value.name() == "StandardBias":
				pairs["Standard bias"] = utc_bias(value.value())
			if value.name() == "DaylightBias":
				pairs["Daylight bias"] = utc_bias(value.value())
		output.dict_to_arr(rows,pairs)
		output.write_out(cfg, rows, "Timezone")

def utc_bias(bias):
	# Handle 32-bit two's compliment negatives
	if bias&0x80000000:
		bias = (0xffffffff^bias)+1
	unsign_bias = bias/60
	if unsign_bias > 0:
		utc = "UTC-%d"%unsign_bias
	else:
		utc = "UTC+%d"%unsign_bias
	return utc
	
