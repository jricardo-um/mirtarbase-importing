#!/bin/env -S python3 -i
# 0_scripts/3_upload.py --efile=3_database/export.json 2> 0_scripts/3_errors.log
import pymongo
import pymongo.errors
import json
import os
import pathlib
import sys
from typing import Literal


#↘ itera sobre los archivos de una carpeta
def fileiter( folder, filepattern ):
	cwd = pathlib.Path( folder ).resolve()
	for file in cwd.glob( filepattern ):
		yield file


def main():
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
		for key, row in fileread.items():
			row[ '_id' ] = key
			try:
				ires = mycol.insert_one( row )
				print( 'Saved:', ires.inserted_id, end='   \r' )
			except pymongo.errors.DuplicateKeyError:
				print( 'Already in database:', key, file=sys.stderr )
	print( '\n' )


if __name__ == '__main__':
	if '--help' in sys.argv:
		print(
		 *[
		  'Reads .json files and uploads them to a MongoDB database.',
		  '',
		  'Directory options:',
		  '   --no-chdir             no not change the base directory to the one of the script',
		  '   --rdir=<directory>     read .json files from <directory> (default ../2_convert)',
		  '   --mongo-url=<url>      connect to mongodb in <url> (default localhost:27017)',
		  '   --mongo-db=<name>      use <name> collection from mongodb (default tfm)',
		  '   --efile=<file>         export created database to <efile>',
		 ]
		)
		from os import _exit as q
		q( 0 )
	#↘ usa el directorio con el cual se está trabajando
	elif '--no-chdir' in sys.argv:
		print( 'Using', os.path.abspath( os.getcwd() ), 'as cwd' )
	#↘ o por defecto usa el directorio del script
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
	murl = 'localhost:27017'
	mname = 'tfm'
	efile = ''
	#↘ opciones de linea de comandos
	for arg in sys.argv:
		if arg.startswith( '--rdir=' ):
			rdir = arg.replace( '--rdir=', '', 1 )
			print( 'Using', rdir, 'as reading dir' )
		elif arg.startswith( '--mongo-url=' ):
			murl = arg.replace( '--mongo-url=', '', 1 )
			print( 'Using', murl, 'as url' )
		elif arg.startswith( '--mongo-db=' ):
			mname = arg.replace( '--mongo-db=', '', 1 )
			print( 'Using', mname, 'as database name' )
		elif arg.startswith( '--efile=' ):
			efile = arg.replace( '--efile=', '', 1 )
	murl = f'mongodb://{murl}/'
	main()
	ecmd = 'mongoexport {} --db={} --collection=mirtarbase --out={}'
	if efile:
		os.system( ecmd.format( murl, mname, efile ) )
	else:
		print( 'You can export the database with the following command:',
		ecmd.format( murl, mname, '<file>' ), sep='\n' )  # yapf: disable

# CATÁLOGO DE FLECHAS
#  ↰↱↲↳
# ←↑→↓↔↕↖↗↘↙
# ⇐⇑⇒⇓⇔⇕⇖⇗⇘⇙
# ⇦⇧⇨⇩ ⇪⇫⇬⇭
# ⇇⇈⇉⇊⇄⇅⇆ ⇤⇥
