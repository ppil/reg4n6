#!/usr/bin/python

from reg4n6 import common
from reg4n6 import output
import struct
		
def nicinfo(cfg, hives):
	if "system" in hives.keys():
		if "cset" not in cfg.keys():
			cfg["cset"] = common.get_control_set(hives['system'])
		
		rows = [["Name", "Description", "DHCP", "IP Address", "Mask", "Nameserver", "Default Gateway", "Gateway MAC", "Domain", "DHCP Server", "Lease Obtained", "Lease Ends"]]
		for i, subkey in enumerate(common.safe_open(hives['system'], "ControlSet00%s\\Services\\Tcpip\\Parameters\\Interfaces"%cfg['cset']).subkeys()):
			nic = {}
			# Get connection name
			conn_key = common.find_keys_name(hives['system'].open("ControlSet00%s\\Control\\Network"%cfg['cset']), subkey.name(), 2)
			if conn_key:
				conn_val = common.safe_open(hives['system'], "%s\\Connection"%conn_key[0], "Name").value()
				nic['Name'] = conn_val
			# Get description
			if "software" in hives.keys():
				nic_key = common.find_keys_value(hives['software'].open("Microsoft\\Windows NT\\CurrentVersion\\NetworkCards"),subkey.name(),1)
				if nic_key:
					nic['Description'] = common.safe_open(hives["software"], nic_key[0], "Description").value()
			# Get everything else
			for value in subkey.values():
				if value.name() == "EnableDHCP":
					if value.value():
						nic["DHCP"] = "Yes"
					else:
						nic["DHCP"] = "No"
				elif value.name() == "DhcpServer":
					nic["DHCP Server"] = common.multi_string(value)
				elif value.name() == "GatewayHardware" or value.name() == "DhcpGatewayHardware":
					nic["Gateway MAC"] = ':'.join([octal.encode('hex') for octal in struct.unpack("<14c",value.value())[-6:]])
				elif value.name() == "NameSever" or value.name() == "DhcpNameServer":
					nic["Nameserver"] = value.value()
				elif value.name() == "IPAddress" or value.name() == "DhcpIPAddress":
					nic["IP Address"] = common.multi_string(value)
				elif value.name() == "SubnetMask" or value.name() == "DhcpSubnetMask":
					nic["Mask"] = common.multi_string(value)
				elif value.name() == "DefaultGateway" or value.name() == "DhcpDefaultGateway":
					nic["Default Gateway"] = common.multi_string(value)
				elif value.name() == "Domain" or value.name() == "DhcpDomain":
					nic["Domain"] = value.value()
				elif value.name() == "LeaseObtainedTime":
					if value.value():
						nic["Lease Obtained"] = common.decode_epoch(value.value())
				elif value.name() == "LeaseTerminatesTime":
					if value.value():
						nic["Lease Ends"] = common.decode_epoch(value.value())
			output.dict_to_arr(rows, nic)
		output.write_out(cfg, rows, "TCP/IP", 1)
