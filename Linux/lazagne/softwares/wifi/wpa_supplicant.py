#!/usr/bin/env python
# -*- coding: utf-8 -*- 

#######################
#
# By rpesche
#
#######################

from lazagne.config.write_output import print_debug
from lazagne.config.moduleInfo import ModuleInfo
import re
import os

class Wpa_supplicant(ModuleInfo):
	def __init__(self):
		ModuleInfo.__init__(self, 'wpa_supplicant', 'wifi')

	def parse_file_network(self, fd):
		password 	= None
		ssid 		= None

		for line in fd:
			if re.match('^[ \t]*ssid=', line):
				ssid = (line.split("\"")[1])
			if re.match('^[ \t]*psk=', line):
				password = line.split("\"")[1]
			if re.match('^[ \t]*password=', line):
				password = line.split("\"")[1]
			if re.match('^[ \t]*}', line):
				return (ssid, password)

	def run(self, software_name=None):
		pwdFound 	= []
		wifi_path 	= u'/etc/wpa_supplicant/wpa_supplicant.conf'

		if os.path.exists(wifi_path):
			# Check root access
			if os.getuid() == 0:
				with open(wifi_path) as fd:
					for line in fd:
						if 'network=' in line:
							(ssid,password) = self.parse_file_network(fd)
							if ssid and password:
								pwdFound.append(
									{
										'SSID'		: ssid,
										'Password'	: password,
									}
								)
				return pwdFound
