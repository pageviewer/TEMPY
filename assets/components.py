class SourceCode:

	def __init__(self):
		self.number_of_lines = 0
		self.content = []
		self.empty = [] # True or False
		self.indentation = []
		self.data = []

	def add_line(self, c, b, i):
		self.number_of_lines += 1
		self.content.append(c)
		self.empty.append(b)
		self.indentation.append(i)

	def print_line(self, number):
		print(str(number-1) + ': ' + self.content[number-1])

	def __str__(self):
		content = ''
		for x in range(0,len(self.content)):
			content += str(x+1) + ': ' + self.content[x]
		return content

class Method:

	def __init__(self, name, initial_line = -1, final_line = -1):
		self.name = name
		self.initial_line = initial_line
		self.final_line = final_line
		self.class_name = ""

	def set_final_line(self, final_line):
		self.final_line = final_line

	def set_class_name(self, class_name):
		self.class_name = class_name

	def __str__(self):
		return (self.name +' (' + str(self.initial_line) +' ~ ' + str(self.final_line) + ') / Class: ' + self.class_name)

class Classe:

	def __init__(self, name, initial_line=-1, final_line=-1):
		self.name = name
		self.initial_line = initial_line
		self.final_line = final_line
		self.methods = []

	def add_method(self, method):
		self.methods.append( method )

	def set_final_line(self, value):
		self.final_line = value

	def __str__(self):
		return (self.name +' (' + str(self.initial_line) + ' ~ ' + str(self.final_line) + ')')

class Data:

	def __init__(self):
		self.classes = []
		self.methods = []

	def add_class(self, c):
		self.classes.append( c )

	def add_method(self, m):
		self.methods.append( m )

	def __str__(self):
		s = 'CLASSES:\n'
		for x in range(0,len(self.classes)):
			s += self.classes[x].name+'('+str(self.classes[x].initial_line)+'~'+str(self.classes[x].final_line)+')\n'
		s += '\nMETHODS/FUNCTIONS:\n'
		
		for x in range(0,len(self.methods)):
			if (self.methods[x].class_name == ''):
				s += self.methods[x].name+'('+str(self.methods[x].initial_line)+'~'+str(self.methods[x].final_line)+') - function or procedure\n'
			else:
				s += self.methods[x].name+'('+str(self.methods[x].initial_line)+'~'+str(self.methods[x].final_line)+') - Class: '+self.methods[x].class_name+'\n'
		return s
