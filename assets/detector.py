import sys
from components import SourceCode, Method, Classe, Data

####################################################################

class TestSmellOccurrence:

	def __init__(self, test_smell_type, method_name, lines):
		self.test_smell_type = test_smell_type
		self.method_name = method_name
		self.lines = []
		for x in lines:
			self.lines.append( x )
	
	def __str__(self):
		r = self.test_smell_type + '\nMethod: ' + self.method_name + '\nLines: ' + str(self.lines) + '\n'
		return r

####################################################################

class Detector:

	def __init__(self):
		self.occurrences = []

	def add_test_smell_occurence(self, test_smell_type, method_name, lines):
		ts = TestSmellOccurrence(test_smell_type, method_name, lines)
		self.occurrences.append( ts )

	def how_many_assertions(self, source, method):	
		occ = []
		for i in range( method.initial_line, method.final_line ):
			if((not source.empty[i]) and
				(
					source.content[i].lstrip().find("assert ") == 0 or
					source.content[i].lstrip().find("assert_") == 0 or
					source.content[i].lstrip().find(".assert") > -1 or
					source.content[i].lstrip().find("self.assert") == 0)
				):
				occ.append(i+1)
		return occ

	def prefixed_with_test(self, method):
		if (len(method.name)>3 and method.name[0]=='t' and method.name[1]=='e' and method.name[2]=='s' and method.name[3]=='t'):
			return True
		else:
			return False

	def prefixed_with_assert(self, method):
		if (len(method.name)>6 and method.name[0]=='a' and method.name[1]=='s' and method.name[2]=='s' and method.name[3]=='e' and method.name[4]=='r' and method.name[5]=='t'):
			return True
		else:
			return False

	def looking_for_test_smells(self, source, methods):
		#self.assertion_roulette(source, methods)
		self.conditional_logic_test(source, methods)
		self.exception_handling(source, methods)
		self.redundant_print(source, methods)
		self.sleepy_test(source, methods)
		self.unknown_test(source, methods)
		self.verbose_test(source, methods)

		self.paradigms_blend(source)
		self.verifying_in_setup_method(source, methods)
		self.non_functional_statement(source, methods)
		self.undefined_test(source, methods)
		
		# print("\n*********************************\n")
		# print(str(len(self.occurrences)) + " test smells detected.")
		# print("\n*********************************\n")
		#for occurence in self.occurrences:
		#	print( occurence )

		return self.occurrences


	# def assertion_roulette(self, source, methods):
	# 	for method in methods:
	# 		if (not (method.name=='setUp')):
	# 			occ = self.how_many_assertions( source, method )
	# 			if ( len(occ) > 1 ):
	# 				self.add_test_smell_occurence( "Assertion Roulette", method.name, occ)


	def exception_handling(self, source, methods):
		lista,occ = [],[]
		for method in methods:
			if (method.name!='setUp' and method.name!='tearDown' and not self.prefixed_with_assert(method) and (len(self.how_many_assertions(source, method)) > 0 or self.prefixed_with_test(method))):
				for i in range( method.initial_line, method.final_line ):
					if(not source.empty[i] and source.content[i].find("try:") != -1):
						occ.append(i+1)
				
				if (len(occ) > 0):
					for x in range(len(occ)):
						lista.append(occ[x])
						self.add_test_smell_occurence( "Exception Handling", method.name, lista)
						lista.clear()
					occ.clear()


	def conditional_logic_test(self, source, methods):
		lista,occ = [],[]
		for method in methods:
			if (method.name!='setUp' and method.name!='tearDown' and not self.prefixed_with_assert(method)):
				for i in range( method.initial_line, method.final_line ):
					#if(not source.empty[i] and (source.content[i].find("if(") != -1 or source.content[i].find("if ") != -1 or source.content[i].find("for ") != -1 or source.content[i].find("while ") != -1 or source.content[i].find("while ") != -1) and source.content[i][len(source.content[i])-2] == ':'):
					if(not source.empty[i] and (
						source.content[i].lstrip().find("if(") == 0 or source.content[i].lstrip().find("if ") == 0 or
						source.content[i].lstrip().find("while(") == 0 or source.content[i].lstrip().find("while ") == 0 or
						source.content[i].lstrip().find("for ") == 0 )):

						if (len(self.how_many_assertions(source, method)) > 0 or self.prefixed_with_test(method)):
							occ.append(i+1)
				
				if (len(occ) > 0):
					for x in range(len(occ)):
						lista.append(occ[x])
						self.add_test_smell_occurence( "Conditional Test Logic", method.name, lista)
						lista.clear()
					occ.clear()


	def redundant_print(self, source, methods):
		lista,occ = [],[]
		for method in methods:
			for i in range( method.initial_line, method.final_line ):
				if(not source.empty[i] and (source.content[i].lstrip().find("print(") == 0 or source.content[i].lstrip().find("print ") == 0)):
					if (len(self.how_many_assertions(source, method)) > 0 or self.prefixed_with_test(method) and not self.prefixed_with_assert(method)):
						occ.append(i+1)
			
			if (len(occ) > 0):
				for x in range(len(occ)):
					lista.append(occ[x])
					self.add_test_smell_occurence( "Redundant Print", method.name, lista )
					lista.clear()
				occ.clear()


	def sleepy_test(self, source, methods):
		lista,occ = [],[]
		#for method in methods:
			#print (method)
		for method in methods:
			for i in range( method.initial_line, method.final_line ):
				if(not source.empty[i] and (source.content[i].find("time.sleep") != -1 or source.content[i].find("event.wait") != -1)):
					if (len(self.how_many_assertions(source, method)) > 0 or self.prefixed_with_test(method) and not self.prefixed_with_assert(method)):
						occ.append(i+1)
				#if(not source.empty[i] and source.content[i].lstrip().find("def ") == 0):
				#	break
			
			if (len(occ) > 0):
				for x in range(len(occ)):
					lista.append(occ[x])
					self.add_test_smell_occurence( "Sleepy Test", method.name, lista)
					lista.clear()
				occ.clear()


	def unknown_test(self, source, methods):
		for method in methods:
			if (self.prefixed_with_test(method) and not self.prefixed_with_assert(method)):
				occ = self.how_many_assertions( source, method )
				if ( len(occ) == 0 ):
					occ.append(method.initial_line)
					self.add_test_smell_occurence( "Unknown Test", method.name, occ)
				occ.clear()


	def verbose_test(self, source, methods):
		occ = []
		for method in methods:
			if (method.name!='setUp' and method.name!='tearDown' and not self.prefixed_with_assert(method)):
				if (method.final_line - method.initial_line >= 45):
					occ.append(method.initial_line)
					occ.append(method.final_line)
					self.add_test_smell_occurence( "Verbose Test", method.name, occ)
					occ.clear()


	def paradigms_blend(self, source):
		procedural, oo, occ = False, False, []

		for x in range(source.number_of_lines):
			if (source.empty[x]):
				pass
			elif (source.content[x].find("from ") == 0 or source.content[x].find("import ") == 0):
				pass
			elif (source.content[x].find("class ") == 0): # maybe verify indentation == 0
				oo = True
				occ.append(x+1)
				break
			elif ( x > 0 and source.content[x-1][len(source.content[x-1])-2] == ',' or source.content[x-1][len(source.content[x-1])-2] == '('):
				pass
			elif ( source.content[x][0] == ')'):
				pass
			else:
				if (procedural == False):
					occ.append(x+1)
				procedural = True

		if (procedural and oo):
			self.add_test_smell_occurence( "Programming Paradigms Blend", "", occ)


	def verifying_in_setup_method(self, source, methods):
		occ,lista = [],[]
		for method in methods:
			if (method.name=='setUp' or method.name=='tearDown'):
				occ = self.how_many_assertions( source, method )
				if (len(occ) > 0):
					for x in range(len(occ)):
						lista.append(occ[x])
						self.add_test_smell_occurence( "Verifying in Setup Method", method.name, lista)
						lista.clear()
					occ.clear()


	def non_functional_statement(self, source, methods):
		occ,lista = [],[]
		for method in methods:
			for i in range( method.initial_line, method.final_line ):
				if(source.content[i].find("pass\n") != -1 and i > 0 and source.content[i-1].find("def ") == -1):
					occ.append(i+1)

			if (len(occ) > 0):
				for x in range(len(occ)):
					lista.append(occ[x])
					self.add_test_smell_occurence( "Non-Functional Statement", method.name, lista)
					lista.clear()
				occ.clear()



	def undefined_test(self, source, methods):
		occ = []
		for method in methods:
			if ((not (method.name=='setUp')) and not (method.name=='tearDown') and not self.prefixed_with_assert(method)): 
				#if ( len(self.how_many_assertions( source, method )) > 0 and not self.prefixed_with_test(method) and source.indentation[method.initial_line] < 2 ):
				if ( len(self.how_many_assertions( source, method )) > 0 and not self.prefixed_with_test(method)):
					occ.append( method.initial_line )
					self.add_test_smell_occurence( "Undefined Test", method.name, occ)
					occ.clear()
