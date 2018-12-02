from subprocess import Popen, PIPE
from re import findall

class TracerouteData:

	def __init__(self, dest):
		if type(dest) is list:
			self.dest = dest
		else:
			self.dest = [dest]
		self.flags=	{
						"m":"255",
						"q":"1",
						"I":"",
						"n":""
					}
		self.ipsList = []
		self.ipsDict = {}

	def updateProtocol(self, protocol):
		switcher = {
			"ICMP":"I",
			"TCP":"T",
			"UDPLITE":"UL",
			"UDP":"U"
		}
		for value in switcher.values():
			if value in self.flags:
				del self.flags[value]
		if protocol in switcher:
			self.flags[switcher[protocol]] = ""
		else:
			print("Protocol not added. " + protocol + " is not one of the options: UDPLITE/UDP/TCP/ICMP.")

	def addFlag(self, flag, value):
		self.flags[flag] = value

	def removeFlag(self, flag):
		del self.flags[flag]

	def traceroute2List(self):
		tr = ["traceroute"]
		for flag, value in self.flags.iteritems():
			option = "-" + flag
			if value != "":
				option += " " + value
			tr.append(option)
		return tr

	def removeLocalIPs(self,ipAddrs):
		for address in ipAddrs:
			if(address.find("192.168") != -1):
				ipAddrs.remove(address)
		return ipAddrs

	def genIPsList(self):
		result = []
		for ip in self.dest:
			process = Popen(self.traceroute2List() + [ip], stdout=PIPE)		# Initialize Popen
			output = process.communicate()[0]								# Get output
			output = output[output.find("\n")+1:]							# Skip the first line
			output = findall("(?:[0-9]{1,3}\.){3}[0-9]{1,3}",output)		# Get IP
			output = self.removeLocalIPs(output)							# Remove all Local IPs since they don't have location data
			result += output
			print("Done with Traceroute of IP: " + ip)
		self.ipsList = result
	
	def genIPsDict(self):
		for ip in self.ipsList:
			if ip in self.ipsDict:
				self.ipsDict[ip] += 1
			else:
				self.ipsDict[ip] = 1

	def genIPs(self):
		self.genIPsList()
		self.genIPsDict()