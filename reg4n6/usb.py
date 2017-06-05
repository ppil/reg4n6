#!/usr/bin/python
from reg4n6 import common
from reg4n6 import output
import struct

def usb(cfg, hives, user_hives):
	# http://www.forensicmag.com/article/2012/06/windows-7-registry-forensics-part-5
	# http://www.forensicmag.com/article/2012/08/windows-7-registry-forensics-part-6
	# http://web.archive.org/web/20131227051020/http://studioshorts.com/blog/2012/10/windows-8-device-property-ids-device-enumeration-pnpobject/
	if "system" in hives.keys():
		if "cset" not in cfg.keys():
			cfg['cset'] = common.get_control_set(hives['system'])
		usbstor = hives["system"].open("ControlSet00%s\Enum\USBSTOR"%cfg["cset"])
		rows = [["Class", "Friendly Name", "Serial No.", "Vendor Name", "UID", "Volume GUID", "Drive Letter", "First Attached", "Last Attached","Last mounted (by user)"]]
		for vendor in usbstor.subkeys():
			for device in vendor.subkeys():
				vals = {}
				vals["Vendor Name"] = vendor.name()
				vals["UID"] = device.name()
				vals["ContID"] = device.value("ContainerID").value()
				vals["Serial No."] = '&'.join(device.name().split('&')[:-1])
				if vals["Serial No."][1] == '&':
					vals["Serial No."] = "N/A (%s)"%vals["Serial No."]
				# Check properties for first attached time
				try: # Win ? - 7
					fi_key = hives["system"].open("%s\Properties\{83da6326-97a6-4088-9453-a1923f573b29}\\00000065\\00000000"%(common.norm_path(device.path())))
					vals["First Attached"] = common.decode_filetime(fi_key.value("Data").value())
				except: # win 8 - ?
					fi_key = hives["system"].open("%s\Properties\{83da6326-97a6-4088-9453-a1923f573b29}\\0065"%(common.norm_path(device.path())))
					vals["First Attached"] = str(fi_key.value("(default)").value().strftime('%a %b %d %Y %H:%M:%S UTC'))
				# Check DeviceClasses for last attached time
				for dev in hives["system"].open("ControlSet00%s\Control\DeviceClasses\{53f56307-b6bf-11d0-94f2-00a0c91efb8b}"%cfg["cset"]).subkeys():
					if vals["Vendor Name"] in dev.name():
						vals["Last Attached"] = dev.timestamp().strftime('%a %b %d %Y %H:%M:%S UTC')
				# Parse MountedDevices
				for point in hives["system"].open("MountedDevices").values():
					mduid = ""
					# Is there a better soln to unpack ASCII?
					for char in struct.unpack("<%dH"%(len(point.value())/2), point.value()):
						if char > 32 and char < 127:
							mduid = "%s%s"%(mduid, chr(char))
					# If UID in MountedDevices value, find volume GUID or mount point in name
					if vals["UID"] in mduid: 
						if point.name()[-1] == '}':
							vals["Volume GUID"] = point.name()[-38:]
						elif point.name()[-1] == ':':
							vals["Drive Letter"] = point.name()[-2:]
				# Search NTUSER.dat files for most recent mount
				if "Volume GUID" in vals.keys():
					last_time = 0
					for user, uhive in user_hives.items():
						uguid = common.safe_open(uhive, "Software\Microsoft\Windows\CurrentVersion\Explorer\MountPoints2\\%s"%vals["Volume GUID"])
						# Hives that never mounted this drive will fail
						if uguid.name():
							utime = uguid.timestamp()
							if not last_time:
								last_time = utime
								last_user = user
							elif last_time < utime:
								last_time = utime
								last_user = user
					if last_time:
						vals["Last mounted (by user)"] = "%s (%s)"%(last_time.strftime('%a %b %d %Y %H:%M:%S UTC'), last_user)
				for value in device.values():
					if value.name() == "FriendlyName":
						vals["Friendly Name"] = value.value()
					if value.name() == "Class": # Old
						vals["Class"] = value.value()
					if value.name() == "ClassGUID": # New
						cguid = common.safe_open(hives["system"], "ControlSet00%s\Control\Class\%s"%(cfg["cset"], common.multi_string(value)))
						for valu in cguid.values():
								if valu.name() == "Class":
									vals["Class"] = valu.value()
				output.dict_to_arr(rows, vals)
		rows = output.sort_by_col(rows, "Vendor Name")
		output.write_out(cfg, rows, "USB", 1)
