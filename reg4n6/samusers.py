#!/usr/bin/python

from reg4n6 import common
from reg4n6 import output
import struct

def samusers(cfg, hives):
	rows = [["RID", "Name", "Flags", "Login Count", "Last Login", "Failed Logins", "Last Failed Login", "Password Created", "Password Expires", "Full Name", "Comment", "Home Dir", "Logon Script", "Profile Path", "Workstations"]]
	if "sam" in hives.keys():
		for usr in common.safe_open(hives["sam"], "SAM\Domains\Account\Users\Names").subkeys():
			vals = {}
			vals["Name"] = usr.name()
			vals["RID"] = usr.value("(default)").value_type()
			rid = hives["sam"].open("SAM\Domains\Account\Users\\0000%04X"%vals["RID"])
			f = rid.value('F').value()
			v = rid.value('V').value()
			try:
				vals["Last Login"] = common.decode_filetime(f[8:16])
			except: pass
			try:
				vals["Password Created"] = common.decode_filetime(f[24:32])
			except: pass
			try:
				vals["Password Expires"] = common.decode_filetime(f[32:40])
			except: pass
			try:
				vals["Last Failed Login"] = common.decode_filetime(f[40:48])
			except: pass
			# http://www.pigstye.net/forensics/password.html
			try:
				vals["Flags"] = []
				acb = struct.unpack("H", f[56:58])[0]
				if acb&0x001:
					vals["Flags"].append("DISABLED")
				if acb&0x002:
					vals["Flags"].append("HOMEDIRREQ")
				if acb&0x004:
					vals["Flags"].append("PWNOTREQ")
				if acb&0x008:
					vals["Flags"].append("TEMPDUP")
				#~ if acb&0x010:
					#~ vals["Flags"].append("NORMAL")
				if acb&0x020:
					vals["Flags"].append("MNS")
				if acb&0x040:
					vals["Flags"].append("DOMTRUST")
				if acb&0x080:
					vals["Flags"].append("WSTRUST")
				if acb&0x100:
					vals["Flags"].append("SRVTRUST")
				if acb&0x200:
					vals["Flags"].append("PWNOEXP")
				if acb&0x400:
					vals["Flags"].append("AUTOLOCK")
				vals["Flags"] = ", ".join(vals["Flags"])
			except: pass
			counts = struct.unpack("HH",f[64:68])
			vals["Failed Logins"] = counts[0]
			vals["Login Count"] = counts[1]
			try:
				username_o = struct.unpack('<L', v[12:16])[0]+0xcc
				username_l = struct.unpack('<L', v[16:20])[0]
				fullname_o = struct.unpack('<L', v[24:28])[0]+0xcc
				fullname_l = struct.unpack('<L', v[28:32])[0]
				vals["Full Name"] = v[fullname_o:fullname_o+fullname_l].replace('\0','')
				comment_o = struct.unpack('<L', v[36:40])[0]+0xcc
				comment_l = struct.unpack('<L', v[40:44])[0]
				vals["Comment"] = v[comment_o:comment_o+comment_l].replace('\0','')
				homedrive_o = struct.unpack('<L', v[84:88])[0]+0xcc
				homedrive_l = struct.unpack('<L', v[88:92])[0]
				vals["Home Drive"] = v[homedrive_o:homedrive_o+homedrive_l].replace('\0','')
				homedir_o = struct.unpack('<L', v[72:76])[0]+0xcc
				homedir_l = struct.unpack('<L', v[76:80])[0]
				vals["Home Dir"] = v[homedir_o:homedir_o+homedir_l].replace('\0','')
				vals["Home Dir"] = "%s%s"%(vals["Home Drive"], vals["Home Dir"])
				logonscript_o = struct.unpack('<L', v[96:100])[0]+0xcc
				logonscript_l = struct.unpack('<L', v[100:104])[0]
				vals["Logon Script"] = v[logonscript_o:logonscript_o+logonscript_l].replace('\0','')
				profilepath_o = struct.unpack('<L', v[108:112])[0]+0xcc
				profilepath_l = struct.unpack('<L', v[112:116])[0]
				vals["Profile Path"] = v[profilepath_o:profilepath_o+profilepath_l].replace('\0','')
				workstations_o = struct.unpack('<L', v[120:124])[0]+0xcc
				workstations_l = struct.unpack('<L', v[124:128])[0]
				vals["Workstations"] = v[workstations_o:workstations_o+workstations_l].replace('\0','')
			except: pass
			output.dict_to_arr(rows, vals)
	rows = output.sort_by_col(rows,"RID")
	output.write_out(cfg, rows, "Local Users", 1)
	
