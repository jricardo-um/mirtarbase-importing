#!/bin/env -S python3 -i
import pymongo
import pymongo.errors
import itertools
import json
import os
import pandas
import pathlib
import sys
from typing import Literal


#↘ itera sobre los archivos de una carpeta
def fileiter( folder, filename ):
	cwd = pathlib.Path( folder ).resolve()
	for file in cwd.glob( filename ):
		yield file


def main( rdir, murl, mname ):
	myclient = pymongo.MongoClient( murl )
	mydb = myclient[ mname ]
	mycol = mydb[ 'mirtarbase' ]
	#↘ itera sobre todos los archivos deseados
	for filepath in fileiter( rdir, '*.json' ):
		filename = pathlib.Path( filepath ).resolve()
		print( 'Reading file', filename )
		print( 'This can take a while...' )
		#↓ lee la base de datos
		with open( filename ) as filebuffer:
			fileread: dict = json.load( filebuffer )
		#↘ itera sobre cada entrada
		for row in fileread.values():
			row[ '_id' ] = row[ 'mirtarbase_id' ]
			del row[ 'mirtarbase_id' ]
			try:
				ires = mycol.insert_one( row )
				print( 'Saved:', ires.inserted_id, end='   \r' )
			except pymongo.errors.DuplicateKeyError:
				print( 'Already in database:', row[ '_id' ], end='   \r' )
	print( '\n' )
	print( 'You can export the database with the following command:' )
	print( 'mongoexport \'mongodb://localhost:27017/\' --db=tfm00 --collection=mirtarbase --out=<file>' )


if __name__ == '__main__':
	if '--help' in sys.argv:
		print(
			'''\
Reads .json files from ../2_convert and uploads them to a MongoDB database

Directory options:
   --no-chdir             no not change the base directory to the one of the script
   --rdir=<directory>     read .json files to <directory>
   --mongo-url=<url>      connect to mongodb in <url>
   --mongo-db=<name>      use <name> database from mongodb
'''
		)
		from os import _exit as q
		q( 0 )
	#↘ usa el directorio con el cual se está trabajando
	elif '--no-chdir' in sys.argv:
		print( 'Using', os.path.abspath( os.getcwd() ), 'as cwd' )
	#↘ usa el directorio del script
	else:
		newpath = os.path.dirname( sys.argv[ 0 ] )
		if not os.path.isabs( newpath ):
			newpath = os.path.join(
				os.path.abspath( os.getcwd() ),
				newpath,
			)
		os.chdir( newpath )
		print( 'Using', os.path.abspath( os.getcwd() ), 'as cwd' )
	rdir = '../2_convert'
	murl = 'mongodb://localhost:27017/'
	mname = 'tfm00'
	for arg in sys.argv:
		if arg.startswith( '--rdir=' ):
			rdir = arg.replace( '--rdir=', 1 )
		elif arg.startswith( '--mongo-url=' ):
			murl = arg.replace( '--mongo-url=', 1 )
		elif arg.startswith( '--mongo-db=<name>' ):
			mname = arg.replace( '--mongo-db=<name>', 1 )
	main( rdir, murl, mname )

# CATÁLOGO DE FLECHAS
#  ↰↱↲↳
# ←↑→↓↔↕↖↗↘↙
# ⇐⇑⇒⇓⇔⇕⇖⇗⇘⇙
# ⇦⇧⇨⇩ ⇪⇫⇬⇭
# ⇇⇈⇉⇊⇄⇅⇆ ⇤⇥
