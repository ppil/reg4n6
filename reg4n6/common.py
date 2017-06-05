from Registry import Registry
from datetime import datetime
import struct
import time
import unicodedata

# Return a null/empty whatever for all RegistryKey methods
class fake_key(object):
	def timestamp(self):
		return datetime.fromtimestamp(0)
	def name(self):
		return ""
	def path(self):
		return ""
	def parent(self):
		return ""
	def subkeys(self):
		return []
	def subkey(self, a=0):
		return fake_key()
	def find_key(self, a=0):
		return fake_key()
	def value(self, a=0):
		return ""
	def values(self):
		return []
	def value_type(self):
		return 0
	def values_number(self):
		return 0
	def subkeys_number(self):
		return 0

# Fail safe, because things sometimes just don't exist
def safe_open(hive, key, value=False):
	ret = fake_key()
	try:
		if value:
			ret = hive.open(key).value(value)
		else:
			ret = hive.open(key)
	except:
		pass
	return ret
		
def unicode_to_ascii(data):
	if isinstance(data, unicode):
		return unicodedata.normalize('NFKD', data).encode("ascii", 'ignore')
	else:
		return data

def decode_systemtime(timestamp):
	months = [0,"Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
	days = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
	year, month, weekday, day, hr, mn, sec, ms = struct.unpack("<8h",timestamp)
	return "%s %s %d %d %02d:%02d:%02d.%02d"%(days[weekday],months[month],day,year,hr,mn,sec,ms)

def decode_filetime(timestamp, f=1):
	reg_ts = Registry.RegistryParse.parse_windows_timestamp(struct.unpack("<Q", timestamp)[0])
	if f:
		return reg_ts.strftime('%a %b %d %Y %H:%M:%S UTC')
	return reg_ts
	
def decode_epoch(epoch):
	return time.strftime('%a %b %d %Y %H:%M:%S UTC', time.gmtime(epoch))
	

# Get active control set
def get_control_set(syshive):
	for v in syshive.open("Select").values():
		if v.name() == "Current":
			return v.value()

# Strip hive portion of key path
def norm_path(path):
	return '\\'.join(path.split('\\')[1:])

# Search value names based on value (usermounts)
def find_value_names(key,value):
	found = []
	for val in key.values():
			if val.value() == value:
				path = key.path().split('\\')[1:]
				found.append(val.name())
	return found

# Search keys based on name
def find_keys_name(base,name,depth):
	keys = []
	for subkey in base.subkeys():
		if subkey.name() == name:
			keys.append('\\'.join(subkey.path().split('\\')[1:]))
		if depth and subkey.subkeys():
				ret = find_keys_name(subkey, name, depth-1)
				for key in ret: 
					keys.append(key)
	return keys
	
# Search keys based on value
def find_keys_value(key,value,depth=1):
	found = []
	for val in key.values():
			if multi_string(val) == value:
				path = key.path().split('\\')[1:]
				found.append('\\'.join(path))
	if depth and key.subkeys():
		for subkey in key.subkeys():
			ret = find_keys_value(subkey, value, depth-1)
			if ret:
				found.append(ret)
	return found

# Return one string from whatever string-like datatype (because sometimes arrays are unexpectedly a thing)
def multi_string(entry):
	if entry.value_type() == Registry.RegSZ or entry.value_type() == Registry.RegExpandSZ:
		return entry.value()
	elif entry.value_type() == Registry.RegMultiSZ:
		strs=[val for val in entry.value() if val]
		return ', '.join(strs)
