import os, sys, webbrowser, ast
#sys.path.append('./assets')
from components import SourceCode, Method, Classe, Data
from detector import *
from report_generator import *


class PythonParser:

	def __init__(self, path_testfile):
		try:
			self.ast_parser = True
			self.file = open(path_testfile, 'r')
			self.data = Data()
			self.path_testfile = path_testfile
			self.source = SourceCode()
			class_methods = []

			with open(path_testfile) as file:
			    node = ast.parse(file.read())
			global_methods = [n for n in node.body if isinstance(n, ast.FunctionDef)]
			classes = [n for n in node.body if isinstance(n, ast.ClassDef)]

			for classe in classes:
				self.data.add_class( Classe( classe.name, classe.lineno, classe.end_lineno ) )
			for class_ in classes:
				class_methods = [n for n in class_.body if isinstance(n, ast.FunctionDef)]
				methods = [n for n in class_.body if isinstance(n, ast.FunctionDef)]
				for method in methods:
					self.data.add_method( Method( method.name, method.lineno, method.end_lineno ) )

			for method in global_methods:
				self.data.add_method( Method( method.name, method.lineno, method.end_lineno ) )

			print(path_testfile + " [AST PACKAGE]")
		
		except Exception as e:
			print(e)
			try:
				self.ast_parser = False
				self.file = open(path_testfile, 'r')
				self.path_testfile = path_testfile
				self.data = Data()
				self.source = SourceCode()
				print(path_testfile + " [MY AST]")

			except Exception as e:
				print(e)


	def is_empty_line(self, line):
		if(line.replace(" ", "").replace("\t", "").replace("\n", "") == ''):
			return True
		else:
			return False

	def count_indentations(self, s):
		return len(s) - len(s.lstrip())

	def get_class_name_from_line(self, position,s):
		for x in range(position+6,len(s)):
			if (s[x]=='(' or s[x]==':'):
				return s[position+6:x]
		return s[position+6:-1]

	def get_method_name_from_line(self, position,s):
	    for x in range(position+4,len(s)):
	        if (s[x]=='('):
	            return s[position+4:x]
	    return s[position+4:-1]

	################ Test Smells detection proccess starts here ################

	def start(self):
		number_of_line, start_scope, end_scope, comentario = 0, [], [], False

		for line in self.file:
			number_of_line += 1

			# verify . Type of comment: ''' [...] ''' OPEN & CLOSE
			if (line.count("\'\'\'") > 1 or line.count("\"\"\"") > 1):
				self.source.add_line(line,True, 0)

			# verify CLOSE comment. Type of comment: ''' [...] '''
			elif (comentario and (line.find("\'\'\'") != -1 or line.find('\"\"\"') != -1)):
				comentario = False
				self.source.add_line(line,True, 0)
			
			# verify OPEN comment. type of comment: ''' [...] ''' or """ [...] """
			elif (line.find("\'\'\'") != -1 or line.find('\"\"\"') != -1):
				comentario = True
				self.source.add_line(line,True, 0)

			# type of comment: #
			elif (len(line.lstrip()) > 1 and line.lstrip()[0]=='#'):
				self.source.add_line(line,True, 0)

			else:
				if (not comentario):
					self.source.add_line(line, self.is_empty_line(line), self.count_indentations(line))
				else:
					self.source.add_line(line,True, 0)

		print(self.data)
		detection = Detector()
		return detection.looking_for_test_smells(self.source, self.data.methods)

	def start2(self):
		number_of_line, start_scope, end_scope, comentario = 0, [], [], False

		for line in self.file:
			number_of_line += 1

			# verify . Type of comment: ''' [...] ''' OPEN & CLOSE
			if (line.count("\'\'\'") > 1 or line.count("\"\"\"") > 1):
				self.source.add_line(line,True, 0)

			# verify CLOSE comment. Type of comment: ''' [...] '''
			elif (comentario and (line.find("\'\'\'") != -1 or line.find('\"\"\"') != -1)):
				comentario = False
				self.source.add_line(line,True, 0)
			
			# verify OPEN comment. type of comment: ''' [...] ''' or """ [...] """
			elif (line.find("\'\'\'") != -1 or line.find('\"\"\"') != -1):
				comentario = True
				self.source.add_line(line,True, 0)

			# type of comment: #
			elif (len(line.lstrip()) > 1 and line.lstrip()[0]=='#'):
				self.source.add_line(line,True, 0)

			else:

				if (not comentario):
					self.source.add_line(line, self.is_empty_line(line), self.count_indentations(line))
							
					if (len(line) > 6 and line.lstrip()[0]=='c' and line.lstrip()[1]=='l' and line.lstrip()[2]=='a' and line.lstrip()[3]=='s' and line.lstrip()[4]=='s' and line.lstrip()[5]==' '):
						self.data.add_class( Classe( self.get_class_name_from_line(line.find("class "), line), number_of_line ) )
						start_scope.append(number_of_line)

					elif (line.lstrip().find("def ") == 0 or line.lstrip().find("def ") == 6):
						self.data.add_method( Method( self.get_method_name_from_line(line.find("def "), line), number_of_line ) )
						start_scope.append(number_of_line)
				else:
					self.source.add_line(line,True, 0)

		# print("\n------------------------------\n")
		# print("Iniciando análise do arquivo: " + self.path_testfile + "\n")

		# contagem de indentações em cada linha
		indentations,lines = [],[]
		for x in range(0,self.source.number_of_lines):
			if (not self.source.empty[x]):
				#print("Linha " + str(x+1) + " - " + str(self.source.indentation[x]) + " indentações.")
				indentations.append(self.source.indentation[x])
				lines.append(x+1)

		# armazena linhas onde escopos terminam através das indentações
		for x in range(0,len(start_scope)):
			for y in range(x,len(lines)):
				if (start_scope[x] == lines[y]):
					indent = indentations[y]
					pos = y
					break
			for y in range(pos+1,len(lines)):
				if (indentations[y] <= indent):
					end_scope.append(lines[y-1])
					break
		while (len(start_scope) > len(end_scope)):
			end_scope.append(lines[len(lines)-1])

		# print(len(start_scope))
		# print()
		# print(start_scope)
		# print("\n")
		# print(len(end_scope))
		# print(end_scope)
		# print()

		# armazena finais os escopos nos dados das CLASSES
		for x in range(0,len(self.data.classes)):
			for y in range(0,len(start_scope)):
				if (self.data.classes[x].initial_line == start_scope[y]):
					self.data.classes[x].set_final_line(end_scope[y])

		# armazena finais os escopos nos dados dos MÉTODOS
		for x in range(0,len(self.data.methods)):
			for y in range(0,len(start_scope)):
				if (self.data.methods[x].initial_line == start_scope[y]):
					self.data.methods[x].set_final_line(end_scope[y])


		# associa métodos com as respectivas classes e vice-versa
		for i in range(len(self.data.classes)):
			for j in range(len(self.data.methods)):
				if (self.data.methods[j].initial_line > self.data.classes[i].initial_line and self.data.methods[j].initial_line <= self.data.classes[i].final_line):
					self.data.methods[j].set_class_name(self.data.classes[i].name)
					self.data.classes[i].add_method(self.data.methods[j].name)


		# verifica sobreposição de métodos, corrigindo atraves de "def" quando houver
		for x in range(len(self.data.methods)):
			for y in range(self.data.methods[x].initial_line+1, self.data.methods[x].final_line):
				if (self.source.content[y].find("def ") > -1 and self.source.indentation[y] <= 4):
					self.data.methods[x].set_final_line(y-1)
					break

		#print(self.data)
		detection = Detector()
		return detection.looking_for_test_smells(self.source, self.data.methods)


	def print_data(self):
		for x in range(self.source.number_of_lines):
			if (self.source.empty[x]):
				print(str(x+1) + ' / indentacoes: ' + str(source.indentation[x]))