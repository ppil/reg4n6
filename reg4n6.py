#!/usr/bin/python
# Registry forensics for incident response
# Peter Pilarski

import sys, os
from getopt import getopt, GetoptError
from reg4n6.geninfo import geninfo
from reg4n6.autoruns import autoruns
from reg4n6.tzinfo import tzinfo
from reg4n6.osinfo import osinfo
from reg4n6.logon import logon
from reg4n6.sessionmgr import sessionmgr
from reg4n6.services import services
from reg4n6.profiles import profiles
from reg4n6.nicinfo import nicinfo
from reg4n6.networks import networks
from reg4n6.samusers import samusers
from reg4n6.uninstalls import uninstalls
from reg4n6.nobackups import nobackups
from reg4n6.usb import usb
from reg4n6.userassist import userassist
from reg4n6.usermounts import usermounts
from Registry import Registry

version = "1.2 (beta)"

def main():
	cfg = read_args()
	hives, user_hives = open_hives(cfg)
	geninfo(cfg, hives)
	tzinfo(cfg, hives)
	osinfo(cfg,hives)
	logon(cfg, hives)
	sessionmgr(cfg, hives)
	autoruns(cfg, hives, user_hives)
	nicinfo(cfg, hives)
	networks(cfg, hives)
	services(cfg, hives)
	profiles(cfg, hives)
	samusers(cfg, hives)
	nobackups(cfg, hives)
	usb(cfg, hives, user_hives)
	uninstalls(cfg, hives)
	userassist(cfg, user_hives)
	usermounts(cfg, hives, user_hives)
	if cfg["format"] == "html":
		init_html(cfg)
		
def usage():
	print """Registry Forensics for Incident Response v%s
	
Usage: %s --mount <mount_dir>


-o [filename], --output [filename]
	Specify output file. Default: STDOUT

-f [fmt], --format [fmt]
	Specify output format. Default: ASCII
	Supported formats: html, ascii
	
-m [path], --mount [path]
	Specify mount point of Windows OS
	
--users [list,of,users]
	Specify user(s) to focus on. Other ntuser hives are ignored.
	
--ntuser [path]
	Specify path to an ntuser hive. Can occur more than once.

--system [path]
	Specify path to system hive
	
--software [path]
	Specify path to software hive
	
--sam [path]
	Specify path to sam hive
"""%(version, sys.argv[0])
	
def read_args():
	cfg = {}
	cfg["format"] = "ascii"
	cfg["users"] = []
	cfg["titles"] = []
	try:
		opts, args = getopt(sys.argv[1:], 'hm:f:o:', ["help","mount=","format=","output=","system=","software=", "sam=", "ntuser=", "users="])
	except GetoptError as err:
		sys.stdout.write(str(err))
		usage() # RTFM
		sys.exit(2)
	for o, a in opts: # option, argument
		if o in ("-h", "--help"):
			usage()
			sys.exit(0)
		elif o in ("-o", "--output"):
			cfg['outfile'] = a
		elif o in ("-f", "--format"):
			cfg['format'] = a.lower()
		elif o == "--system":
			cfg['system'] = a
		elif o == "--software":
			cfg['software'] = a
		elif o == "--sam":
			cfg['sam'] = a
		elif o == "--ntuser":
			cfg['users'].append(a)
		elif o == "--users":
			cfg['scope'] = [u.lower() for u in a.split(',')]
		elif o in ("-m","--mount"):
			cfg["mount"] = a
			cfg = find_hives(cfg, a)
	if "outfile" in cfg.keys():
		cfg["outfh"] = open(cfg["outfile"], 'a')
	else:
		cfg["outfh"] = sys.stdout
	return cfg

# Because glob() is case sensitive and the insensitive regex is hideous
def find_hives(cfg, path):
	# Get system hives
	cfg_dir = os.path.join(path,"Windows","System32","config")
	for fn in os.listdir(cfg_dir):
		if fn.lower() == "system":
			cfg["system"] = os.path.join(cfg_dir, fn)
		elif fn.lower() == "software":
			cfg["software"] = os.path.join(cfg_dir, fn)
		elif fn.lower() ==  "security" in fn.lower():
			cfg["security"] = os.path.join(cfg_dir, fn)
		elif fn.lower() == "sam":
			cfg["sam"] = os.path.join(cfg_dir, fn)
	# Get user hives
	if os.path.exists(os.path.join(path,"Users")):
		user_base = os.path.join(path, "Users")
	else:
		user_base = os.path.join(path, "Documents and Settings")
	for user in os.listdir(user_base):
		user_path = os.path.join(user_base, user)
		if os.path.isdir(user_path):
			for fn in os.listdir(user_path):
				if fn.lower() == "ntuser.dat":
					cfg["users"].append(os.path.join(user_path, fn))
	return cfg

def open_hives(cfg):
	hives = {}
	if "system" in cfg.keys() and os.path.isfile(cfg["system"]):
		hives["system"] = Registry.Registry(open(cfg["system"],'rb'))
	if "software" in cfg.keys() and os.path.isfile(cfg["software"]):
		hives["software"] = Registry.Registry(open(cfg["software"],'rb'))
	if "sam" in cfg.keys() and os.path.isfile(cfg["sam"]):
		hives["sam"] = Registry.Registry(open(cfg["sam"],'rb'))
	user_hives = {}
	for user in cfg["users"]: # in case Users and "Documents and Settings"
		username = user_from_path(cfg, user)
		if "scope" in cfg.keys() and username.lower() not in cfg["scope"]:
			continue
		user_hives[username] = Registry.Registry(open(user,'rb'))
	return hives, user_hives


def user_from_path(cfg, path):
	return os.path.split(os.path.split(path)[0])[1]

def init_html(cfg):
	filename = cfg['outfh'].name
	cfg['outfh'].close()
	tables = open(filename).read()
	head = """<!DOCTYPE html>
<head><title>test</title>
<style>
table{margin-left:3%;}
td{padding:2px 4px 2px 4px;
	white-space:nowrap;}
th{background-color:#c6c6c6;}
a{
	color: inherit;
	font: initial;
	text-decoration: none;
}
a:hover{
	text-decoration: underline;
}
div#index{
	margin-left:3%;
	display: block;
	border: none;
}
div{
	margin: 1px;
	display:inline-block;
	border-bottom: 1px dashed #808080;
}
table, th, td {
    border: 1px solid #808080;
    border-collapse: collapse;
}
</style></head>
"""
	index = "<h2>Index</h2>"
	for title in cfg['titles']:
		index += "<div id='index'><a href=#%s>- %s</a></div>\n"%(title.replace(' ',''), title)
	index += "</div>"
	head = "%s%s<br>"%(head,index)
	output = "%s%s"%(head, tables)
	fh = open(filename, 'w')
	fh.write(output)

main()
