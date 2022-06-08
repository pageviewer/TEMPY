import sys
from components import SourceCode, Method, Classe, Data

class ReportGenerator:

	def __init__(self):
		self.file = open("./report/log.html", 'w')
		self.content = ''
		self.number_of_test_smells = 1


	def add_header(self, total_ts, qtd_ts_in_projects, projects, ts_qtd): # step 1
		self.content += '''<!DOCTYPE html>
<html>
<head>

<title>Test Smells Analysis</title>
<style>
	table, td, th {
		border: 1px solid black;
	}
	table {
		border-collapse: collapse;
		width: 100%;
	}
	td {
		text-align: center;
	}
</style>
</head>
<body>
		
<h1>Test Smells Analysis</h1>

<h3>Total analysis: ''' 

		if (total_ts > 1 and qtd_ts_in_projects > 1):
			self.content += str(total_ts) + " test smells found in " + str(qtd_ts_in_projects) + " python test files<h3>"
		elif(total_ts < 2 and qtd_ts_in_projects < 2):
			self.content += str(total_ts) + " test smell found in " + str(qtd_ts_in_projects) + " python test file<h3>"
		elif(total_ts > 1 and qtd_ts_in_projects < 2):
			self.content += str(total_ts) + " test smells found in " + str(qtd_ts_in_projects) + " python test file<h3>"
		else:
			self.content += str(total_ts) + " test smell found in " + str(qtd_ts_in_projects) + " python test files<h3>"

		self.content += '''<ul>\n'''
		for x in range(len(projects)):
			self.content += "\t<li>" + self.get_testfile_name( projects[x] ) + " - " + str(ts_qtd[x]) + " test smells found</li>"
		self.content += "\n</ul><hr/><hr/>"

	def add_table_header(self, path, qtd_ts):  # step 2
		self.content += '<h4>Python Test file: ' + self.get_testfile_name(path) + '<br>Path: ' + self.get_path(path) + '</h4>'

		if (qtd_ts > 0):
			self.content +='''\n<table>
	<thead>
		<th style="width: 3%">#</th>
		<th style="width: 19%">Test Smell</th>
		<th style="width: 58%">Method</th>
		<th style="width: 20%">Lines</th>
	</thead>\n'''

		else:
			self.content += "<h4>No test smell found.</h4>"
		self.number_of_test_smells = 1

	def add_table_body(self, ts, method, lines):  # step 4
		self.content += '''\t<tbody>
		<td>''' + str(self.number_of_test_smells) + '''</td>
		<td>''' + ts + '''</td>
		<td>''' + method + '''</td>
		<td>''' + str(lines)[1:-1] + '''</td>
	</tbody>\n'''
		self.number_of_test_smells += 1


	def add_table_close(self, qtd_ts):  # step 5
		if (qtd_ts > 0):
			self.content += '''\n</table><br><hr/>'''
		else:
			self.content += '<hr/>'

	def add_footer(self): # step 6
		self.content += "\n</body>\n</html>\n"


	def build(self): # final step (step 7)
		self.file.write( self.content )
		self.file.close()

	def get_testfile_name(self, path):
		for x in range(len(path)-1, -1, -1):
			if (path[x] == '/'):
				return path[x+1:]

	def get_path(self, path):
		for x in range(len(path)-1, -1, -1):
			if (path[x] == '/'):
				return path[0:x+1]