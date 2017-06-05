#!/usr/bin/python

from reg4n6 import common
from reg4n6 import output
import struct

def networks(cfg,hives):
	if "software" in hives.keys():
		rows=[['Name', 'Description', 'Category', 'Type', 'Managed', 'Gateway MAC', 'DNS suffix', 'Created', 'Last connected']]
		for profile in common.safe_open(hives["software"], "Microsoft\Windows NT\CurrentVersion\NetworkList\Profiles").subkeys():
			vals = {}
			for value in profile.values():
				if value.name() == "ProfileName":
					vals["Name"] = common.multi_string(value)
				elif value.name() == "Description":
					vals["Description"] = common.multi_string(value)
				elif value.name() == "NameType":
					n = value.value()
					if n == 0x06:
						vals["Type"] = "Wired"
					elif n == 0x17:
						vals["Type"] = "Mobile (%d)"%n
					elif n == 0x47:
						vals["Type"] = "Wireless"
					elif n == 0xf3:
						vals["Type"] = "Mobile (%d)"%n
					else:
						vals["Type"] = "Unknown (%d)"%n
				elif value.name() == "Managed":
					vals["Managed"] = "Yes" if value.value() else "No"
				elif value.name() == "Category":
					n = value.value()
					if not n:
						vals["Category"] = "Public"
					elif n == 1:
						vals["Category"] = "Private"
					elif n == 2:
						vals["Category"] = "Domain"
					else:
						vals["Category"] = "Other (%d)"%n
				elif value.name() == "DateCreated":
					vals["Created"] = common.decode_systemtime(value.value())
				elif value.name() == "DateLastConnected":
					vals["Last connected"] = common.decode_systemtime(value.value())
			sig = common.find_keys_value(hives['software'].open("Microsoft\Windows NT\CurrentVersion\NetworkList\Signatures"),profile.name(),2)
			if sig:
						vals["DNS suffix"] = common.safe_open(hives["software"], sig[0], "DnsSuffix").value()
						vals["Gateway MAC"] = bin_to_mac(common.safe_open(hives["software"], sig[0], "DefaultGatewayMac").value())
			output.dict_to_arr(rows, vals)
		output.write_out(cfg, rows, "Networks", 1)

def bin_to_mac(value):
	if not value:
		return ""
	octets = struct.unpack("<6c", value)
	return ':'.join([octet.encode('hex') for octet in octets])
	
