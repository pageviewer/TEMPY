import sys,re,pathlib,os,git,shutil,subprocess

sys.path.append('./assets')
from components import SourceCode, Method, Classe, Data
from python_parser import *
from detector import *
from report_generator import *

import tkinter as tk
from tkinter import ttk
import tkinter.filedialog
from tkinter import messagebox

def get_selected_test_file(lista):
	if not lista.curselection():
		tkinter.messagebox.showwarning(title=None, message="Please select a test file from the list for analysis.")
	else:
		all_logs, projects = [], []
		for x in lista.curselection():
			p = PythonParser(lista.get(x))
			if (p.ast_parser):
				#print(x)
				all_logs.append(p.start())
			else:
				#print(x)
				all_logs.append(p.start2())

			projects.append( lista.get(x) )
		
		prev, cont_proj, cont_total, ts_qtd  = None, 0, 0, []
		for index in range(len(all_logs)):
			for log in all_logs[index]:
				if (log.lines == prev):
					pass
				else:
					cont_proj += 1
					cont_total += 1
				prev = log.lines
			ts_qtd.append( cont_proj )
			cont_proj = 0

		report = ReportGenerator()
		report.add_header( cont_total, len(all_logs) , projects, ts_qtd)
		prev = None
		for index in range(len(all_logs)):		
			report.add_table_header( projects[index], ts_qtd[index] )
			for log in all_logs[index]:
				if (log.lines == prev):
					pass
				else:
					report.add_table_body( log.test_smell_type, log.method_name, log.lines )
				prev = log.lines
			report.add_table_close(ts_qtd[index])
		report.add_footer()
		report.build()

		url = os.path.abspath("./report/log.html")
		webbrowser.open(url,new=1)
		# sys.exit(0)

def get_all_test_file(lista):
	if (tkinter.messagebox.askokcancel(title=None, message=str( lista.size() )+" test file(s) selected. Do you wish to continue?")):

		all_logs, projects = [], []
		for x in range(lista.size()):
			p = PythonParser(lista.get(x))
			if (p.ast_parser):
				all_logs.append(p.start())
			else:
				all_logs.append(p.start2())
			
			projects.append( lista.get(x) )

		prev, cont_proj, cont_total, ts_qtd  = None, 0, 0, []
		for index in range(len(all_logs)):
			for log in all_logs[index]:
				if (log.lines == prev):
					pass
				else:
					cont_proj += 1
					cont_total += 1
				prev = log.lines
			ts_qtd.append( cont_proj )
			cont_proj = 0

		report = ReportGenerator()
		report.add_header( cont_total, len(all_logs) , projects, ts_qtd)
		prev = None
		for index in range(len(all_logs)):		
			report.add_table_header( projects[index], ts_qtd[index] )
			for log in all_logs[index]:
				if (log.lines == prev):
					pass
				else:
					report.add_table_body( log.test_smell_type, log.method_name, log.lines )
				prev = log.lines
			report.add_table_close(ts_qtd[index])
		report.add_footer()
		report.build()

		url = os.path.abspath("./report/log.html")
		webbrowser.open(url,new=1)
		# sys.exit(0)
		

def close_window(window):
	window.destroy()
	root.deiconify()

def close_window_confirmation(newWindow):
    if (tkinter.messagebox.askokcancel(title=None, message="Do you really want to close this window?")):
    	close_window(newWindow)

def test_file_selection_window(nomes,paths):
	newWindow = tk.Tk()
	newWindow.protocol('WM_DELETE_WINDOW', lambda: close_window_confirmation(newWindow))
	newWindow.wm_title("Select a Python test file")
	newWindow.minsize(350, 200)

	xscrollbar = tk.Scrollbar(newWindow, orient=tk.HORIZONTAL)#, selectmode = "multiple")
	xscrollbar.pack(side=tk.BOTTOM, fill=tk.X)

	yscrollbar = tk.Scrollbar(newWindow, orient=tk.VERTICAL)
	yscrollbar.pack(side=tk.RIGHT, fill=tk.Y)

	lista = tk.Listbox(newWindow, width = 80, xscrollcommand=xscrollbar.set, yscrollcommand=yscrollbar.set, selectmode = "multiple")
	lista.pack()

	xscrollbar.config(command=lista.xview)
	yscrollbar.config(command=lista.yview)

	for x in range(0,len(nomes)):
		lista.insert(x, paths[x]+'/'+nomes[x])

	btn1 = tk.Button(newWindow, text='Select', command=lambda: get_selected_test_file(lista)).pack(fill=tk.X)
	btn2 = tk.Button(newWindow, text='Select All', command=lambda: get_all_test_file(lista)).pack(fill=tk.X)
	btn3 = tk.Button(newWindow, text='Cancel', command=lambda: close_window(newWindow)).pack(fill=tk.X)

def generate_test_file_list_log(files,nomes,paths):
	if (files > 1):
		tkinter.messagebox.showinfo(title=None, message=str(files) + ' Python test files found.')
		root.withdraw() # hide home screen
		test_file_selection_window(nomes,paths)

	elif (files == 1):
		tkinter.messagebox.showinfo(title=None, message='1 Python test file found.')
		root.withdraw() # hide home screen
		test_file_selection_window(nomes,paths)
	else:
		tkinter.messagebox.showinfo(title=None, message='No Python test file found.')


def is_hidden_directory(dirName):
	if( dirName.find( '/.' )!=-1 ):
		return True
	else:
		return False

def is_test_file(filename,path='0'):
	if (path=='0'):
		f = open(filename, 'r', encoding="utf8", errors='ignore')
	else:
		f = open(path + '/' + filename, 'r', encoding="utf8", errors='ignore')
	for line in f:
		if (line.find('assert') == 0):
			f.close()
			return True
		if (line.find('import unittest') != -1 or line.find('import pytest') != -1 or line.find('from unittest') != -1 or line.find('from pytest') != -1):
			f.close()
			return True
	f.close()
	return False

def search_test_file(tempdir):
	number_of_files, paths, nomes = 0,[],[]
	for dirName, subdirList, fileList in os.walk(tempdir):
		if( not is_hidden_directory(dirName) ):
			for x in fileList:
				if ( x.find( '.py' )!=-1 and x.find( 'main.py' )==-1):
					if (is_test_file(x,dirName)):
						number_of_files += 1
						nomes.append(x)
						paths.append(dirName)

	generate_test_file_list_log(number_of_files,nomes,paths)

def select_file():
	fname = tk.filedialog.askopenfilename(filetypes=[("Python files", ".py")],title='Choose a test file')
	if len(fname) > 0:
		
		all_logs, projects, ts_qtd, i, cont = [], [], [], 0, 0
		p = PythonParser(fname)
		if (p.ast_parser):
			all_logs.append(p.start())
		else:
			all_logs.append(p.start2())
		
		projects.append( fname )
		
		ts_qtd.append( len(all_logs[i]) )
		
		for log in all_logs:
			ts_qtd.append( len(log) )
			for x in log:
				cont += 1

		report = ReportGenerator()
		report.add_header( cont, len(all_logs) , projects, ts_qtd)
		prev = None
		for index in range(len(all_logs)):			
			report.add_table_header( projects[index], ts_qtd[index] )
			for log in all_logs[index]:
				if (log.lines == prev):
					pass
				else:
					report.add_table_body( log.test_smell_type, log.method_name, log.lines )
				prev = log.lines
			report.add_table_close(ts_qtd[index])
		report.add_footer()
		report.build()

		url = os.path.abspath("./report/log.html")
		webbrowser.open(url,new=1)
		# sys.exit(0)

		if( not is_test_file(fname) ):
			tkinter.messagebox.showwarning(title=None, message="The selected file is not a test file.")

def select_directory():
	currdir = os.getcwd()
	tempdir = tk.filedialog.askdirectory(parent=root, initialdir=currdir, title='Select a directory')
	if (len(tempdir) > 0):
		search_test_file(tempdir)

def set_github_url():
	url_valid = False
	try:
	    shutil.rmtree("./project_downloaded")
	except OSError as e:
	    pass

	while (not url_valid):
		git_url = tk.simpledialog.askstring("Analyze project from GitHub", "Enter GitHub URL:", initialvalue="https://github.com/")

		if (git_url is None):
			url_valid = True
		elif (git_url.find( 'github.com/' ) == -1):
			tkinter.messagebox.showinfo(title=None, message='Please enter a valid GitHub url.\n\nTry:\nhttps://github.com/ + \n{user_name}/{project_name}')
		else:
			#subprocess.Popen(['python3', "./assets/progress_bar.py"])
			try:
				git.Repo.clone_from(git_url, "project_downloaded")
				url_valid = True
				search_test_file("project_downloaded")
			
			except Exception as e:
				tkinter.messagebox.showinfo(title=None, message='Project not found. Please check GitHub URL and try again.')

		
root = tk.Tk()
root.resizable(width=False, height=False)
root.wm_title("TS Automatic Detector for Python")

b1 = tk.Button(master = root, text = 'Choose a test file', width = 50, command=select_file)
b1.pack(side=tk.TOP, padx = 2, pady=2)

b2 = tk.Button(master = root, text = 'Search for test classes in a local project', width = 50, command=select_directory)
b2.pack(side=tk.BOTTOM, padx = 2, pady=2)

b3 = tk.Button(master = root, text = 'Analyze project from GitHub', width = 50, command=set_github_url)
b3.pack(side=tk.BOTTOM, padx = 2, pady=2)

tk.mainloop()
# print(str(cont_total) + " com arquivos de test smells encontrados em " + str(len(projects)) + " arquivos de teste.")