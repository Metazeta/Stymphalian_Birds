#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
__project__ = littlebirdie
__author__ = "Emmanuel Ruaud"
__email__ = "eruaud@student.le-101.fr"
"""

import os
import sys
import jinja2 as jj
from colorama import Fore, Back, Style
from distutils.dir_util import copy_tree
import readline
import glob
from shutil import copy2


LIBFT_PATH = 'Documents/vogsphere/libft'


def print_header():
	f = open('resources/header', 'r')
	print(Fore.BLUE + f.read())


def gen_makefile(directory, dict_options):
	f = open(directory + '/Makefile', 'w')
	current = os.path.dirname(os.path.abspath(__file__))
	print('Creating C project...')
	env = jj.Environment(loader=jj.FileSystemLoader(current),
						 trim_blocks=True)
	template = env.get_template('resources/mk_template')
	f.write(template.render(dict=dict_options))
	f.close()
	copy2(os.path.join(current, 'resources/gitignore'),
		os.path.join(directory + '/.gitignore'))

def gen_pythonfile(directory, dict_options):
	f3 = open(os.path.join(directory, 'script', dict_options['name'] + '.py'), 'w')
	current = os.path.dirname(os.path.abspath(__file__))
	env = jj.Environment(loader=jj.FileSystemLoader(current),
						 trim_blocks=True)
	template = env.get_template('resources/python_template.py')
	f3.write(template.render(dict=dict_options))
	f3.close()
	f2 = open(directory + '/.gitignore', 'w')
	f2.close()

def handle_c(name, directory):
	try :
		os.makedirs(os.path.join(directory, 'includes'))
		os.makedirs(os.path.join(directory, 'build'))
		os.makedirs(os.path.join(directory, 'src'))
		os.makedirs(os.path.join(directory, 'lib'))
	except:
		print('Shit happened.')
	print(Fore.YELLOW, end='')
	lib = input('Do you want to include your libft ? (y/n) ')
	if lib == 'y':
		copy_tree(os.path.join(os.path.expanduser("~"), LIBFT_PATH),
				  os.path.join(os.path.expanduser("~"), directory, 'lib/libft/'))
		gen_makefile(directory,
					 {'name':name, 'lib_includes':'-I lib/libft/includes/',
					  'libs_lib':'-lft', 'flags_lib':'-L lib/libft/',
					  'make_lib':'@make -C lib/libft/'})
	else:
		gen_makefile(directory, {'name':name})
	print(Fore.GREEN + 'Project was successfully generated')


def handle_py(name, directory):
	print('Creating Python project...')
	os.makedirs(os.path.join(directory, 'script'))
	gen_pythonfile(directory, {'name':name})
	print(Fore.GREEN + 'Project was successfully generated')


def create_folder(directory):
	if not os.path.exists(directory):
		os.makedirs(directory)
		print(Fore.GREEN + directory + ' folder was created.')
	else:
		print(Fore.GREEN + directory + ' already exists')
		sys.exit()

def path_completer(text,state):

	readline.get_line_buffer().split()
	text = os.path.join(os.path.expanduser("~") , text)
	return [ x for x in glob.glob(text + '*') ][state]


def get_input():
	print_header()
	print(Fore.YELLOW, end='')
	name = input('Project name: ')
	readline.set_completer_delims('\t')
	readline.parse_and_bind("tab: complete")
	readline.set_completer(path_completer)
	pro_folder = input('Project Folder: ')
	create_folder(os.path.join(os.path.expanduser("~"), pro_folder))
	print(Fore.YELLOW, end='')
	lng = input("Language: ")
	if lng == 'C':
		handle_c(name, pro_folder)
	elif lng == 'Python':
		handle_py(name, pro_folder)
	else:
		print('This language is not supported')


def main():
	get_input()


if __name__ == '__main__':
	main()
