import collections

class Solution:
	def __init__(self,lines):
		self.graph = collections.defaultdict(list)
		self.installed = set()
		for line in lines:
			self.print_output(line)

	def print_output(self,line):
		tmp = line.split(' ')
		cmd = tmp[0]

		if cmd == 'DEPEND':
			text = self.handle_depend(tmp[1:])
			if not text:
				print line
			else:
				print text

		elif cmd == 'INSTALL':
			text = self.handle_install(tmp[1:])


	def handle_depend(self,packages):
		root = packages[0]
		for package in packages[1:]:
			if package and root in self.graph:
				self.graph[root].append(package)
			else:
				if package:
					self.graph[root] = [package]

		for package in packages[1:]:
			if package and package not in self.graph:
				self.graph[package] = []

	def handle_install(self,packages):
		def dfs(packages):
			for package in packages:
				if package and package in self.installed:
					return "{0} already installed".format(package)
				else:
					for package in self.graph[pa]
		return dfs(packages)
			



if __name__ == '__main__':
	lines = []
	while True:
	    line = raw_input()
	    if line:
	        lines.append(line)
	    else:
	        break
	sol = Solution(lines)
	print(sol.graph)
