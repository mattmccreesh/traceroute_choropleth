from subprocess import Popen, PIPE
from re import findall

class TracerouteData:

	def __init__(self, dest):
		self.dest = dest
		self.flags=	{
						"m":"255",
						"q":"1",
						"I":"",
						"n":""
					}

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
		tr.append(self.dest)
		return tr

	def removeLocalIPs(self,ipAddrs):
		for address in ipAddrs:
			if(address.find("192.168") != -1):
				ipAddrs.remove(address)
		return ipAddrs

	def genIPs(self):
		process = Popen(self.traceroute2List(), stdout=PIPE)
		output = process.communicate()[0]
		output = output[output.find("\n")+1:]
		output = findall("(?:[0-9]{1,3}\.){3}[0-9]{1,3}",output)
		output = self.removeLocalIPs(output)
		return output