#!/bin/env -S python3 -i
# 0_scripts/2_convert.py --ignore-prompts 2> 0_scripts/2_errors.log
# 0_scripts/2_convert.py --export-experiments
import itertools
import json
import os
import pandas
import pathlib
import sys
from datetime import datetime
from typing import Literal


def unique( l ):
	return list( set( l ) )


class config:
	funcmap = dict()
	
	#↘ guarda el nombre de archivo de los ajustes
	def __init__( self, cfgfile, pign ):
		self.cfgfile = cfgfile
		self.pign = pign
	
	#↘ carga los ajustes al empezar
	def __enter__( self ):
		with open( self.cfgfile ) as f:
			self.params: dict[ str:dict ] = json.load( f )
		return self
	
	#↘ guarda los ajustes al acabar
	def __exit__( self, exc_type, exc_val, exc_tb ):
		with open( self.cfgfile, 'w' ) as f:
			json.dump( self.params, f, indent='\t' )
	
	#   separa por todos los separadores a la vez p.ej.
	#   "item1//item2;item3//item4//item5" pasa a ser
	#↘ ['item1','item2','item3','item4','item5']
	def _isthisajoke( self, text: str, separators: list[ str ] ):
		if not len( separators ):
			yield text
		else:
			separator = separators.pop()
			for value in text.split( separator ):
				yield from self._isthisajoke( value, separators.copy() )
	
	#   encuentra el separador adecuado y separa
	#↘ (en nuestro caso "//" o ";")
	def separe_multiple_separators( self, val: str, key2 ):
		key1 = "column_configs"
		key3 = "known_separators"
		try:
			separators: list = self.params[ key1 ][ key2 ][ key3 ]
		except KeyError:
			separators = list()
			while True:
				new = input( f'Enter value separators for `{key2}`: ' )
				if new == '': break
				separators.append( new )
			self.params[ key1 ][ key2 ][ key3 ] = separators
			print( ' Updated!' )
		return list( self._isthisajoke( val, separators.copy() ) )
	
	#   evita nombres diferentes para la misma entrada
	#↘ (en nuestro caso, "5pRNA"="5'RNA"="5p-RNA"=etc…)
	def control_vocabulary( self, val: str, key2 ):
		if type( val ) == list:
			return unique( itertools.chain( *[
			 self.control_vocabulary( v, key2 ) for v in val
			], ) )  # yapf: disable
		key1 = "column_configs"
		key3 = "allowed_values"
		try:
			allowed = self.params[ key1 ][ key2 ][ key3 ]
			if type( val ) == list: allowed[ val ]
			else: return allowed[ val ]
		except KeyError:
			if self.pign: new = ''
			else: new = input( f'Enter allowed value for `{val}` in column `{key2}`: ' )
			if new == '': new = val
			try:
				self.params[ key1 ][ key2 ][ key3 ][ val ] = [ new ]
			except KeyError:
				self.params[ key1 ][ key2 ][ key3 ] = { val: [ new ] }
			if not self.pign: print( ' Updated!' )
			return new


#↘ itera sobre los archivos de una carpeta
def fileiter( folder, filename ):
	cwd = pathlib.Path( folder ).resolve()
	for file in cwd.glob( filename ):
		yield file


def supindex( v ):
	v = str( v )
	for w, i in (
	 ( 'nan', 0 ),
	 ( 'Non-Functional MTI (Weak)', 1 ),
	 ( 'Non-Functional MTI', 2 ),
	 ( 'Functional MTI (Weak)', 3 ),
	 ( 'Functional MTI', 4 ),
	):
		if v == w: return i
	raise ValueError( f'Index {v} {type(v)} not supported' )


def col2key( c ):
	for d, k in (
	 ( 'miRTarBase ID', 'mirtarbase_id' ),
	 ( 'miRNA', 'mirna_symbol' ),
	 ( 'Species (miRNA)', 'mirna_specie' ),
	 ( 'Target Gene', 'gene_symbol' ),
	 ( 'Target Gene (Entrez ID)', 'gene_entrez' ),
	 ( 'Species (Target Gene)', 'gene_specie' ),
	 ( 'Experiments', 'experiments' ),
	 ( 'Support Type', 'support_type' ),
	 ( 'References (PMID)', 'pubmed_ids' ),
	):
		if c == d: return k
	raise ValueError( f'Column {c} not indexed' )


def main():
	#↘ carga la configuración, incluye la lista de valores permitidos para las columnas
	with config( cfgpath, pign ) as mycfg:
		#↘ itera sobre todos los archivos deseados
		for filepath in fileiter( rdir, '*.xlsx' ):
			#↓ diccionario para almacenar los datos importados
			mydatabase: dict[ dict ] = dict()
			filename = pathlib.Path( filepath ).name
			print( 'Reading file', filename )
			print( 'This can take a while...' )
			#↓ lee la base de datos con pandas
			fileread = pandas.read_excel( filepath )  #, dtype=str )
			corruptentries = list()
			#↘ itera sobre (índice, fila) del dataframe
			for ind, row in fileread.iterrows():
				if ind < 700 or not ind % 700: print( '\x1b[F\x1b[K', 'Processing row', ind )
				if type( row[ 'Target Gene' ] ) == datetime:
					i = row[ 'miRTarBase ID' ]
					print(
					 '[Value]',
					 f'Discarded entry with ID {i},',
					 f'Target Gene is datetime: {val}',
					 file=sys.stderr,
					)
					continue
				#↓ no se puede usar `miRTarBase ID` porque está repetido
				entryname = row[ 'miRNA' ] + '_' + row[ 'Target Gene' ]
				entry = mydatabase.get( entryname, dict() )
				#↘ itera sobre (columna, valor) de la fila
				for col, val in row.items():
					key = col2key( col )
					if col in (
					  'miRTarBase ID',
					  'miRNA',
					  'Species (miRNA)',
					  'Target Gene',
					  'Target Gene (Entrez ID)',
					  'Species (Target Gene)',
					):
						#↓ estos valores no deberian cambiar
						if entry.get( key, val ) != val:
							print(
							 '[Match]',
							 f'Discarded entry {entryname},',
							 f'column {col} does not match:',
							 f'{entry[ key ]} != {val}',
							 file=sys.stderr,
							)
							corruptentries.append( entryname )
						else:
							entry[ key ] = val
					#↓ modifica los valores necesarios
					elif col in ( 'Experiments', ):
						val = mycfg.separe_multiple_separators( val, col )
						if key in entry: val += entry[ key ]
						val = mycfg.control_vocabulary( val, col )
					elif col in ( 'Support Type', ):
						val = supindex( val )
						val = max( val, entry.get( key, -1 ) )
					elif col in ( 'References (PMID)', ):
						val = unique( entry.get( key, [] ) + [ val ] )
					else:
						raise ValueError( f'Column {col} not expected' )
					#↓ pone el valor en mi fila
					entry[ key ] = val
				#↓ pone la fila en mi base de datos
				mydatabase[ entryname ] = entry
			#↓ elimina las filas inconsistentes
			for entryname in unique( corruptentries ):
				del mydatabase[ entryname ]
			#↓ guarda la base de datos como json
			exportfilepath = wdir + filename + '.json'
			pathlib.Path( exportfilepath ).parent.mkdir( parents=True, exist_ok=True )
			with open( exportfilepath, 'w' ) as file:
				json.dump( mydatabase, file, indent='\t' )


#↘ para fácil edición de los experimentos
def edit_experiments( method: Literal[ 'b', 'i', 'e' ] = 'b', tpath='./2_temp_edit.tsv' ):
	with config( cfgpath, pign ) as mycfg:
		key1, key2, key3 = "column_configs", "Experiments", "allowed_values"
		paramz = mycfg.params[ key1 ][ key2 ][ key3 ].items()
		table = tuple( '\t'.join( ( k, '\t'.join( v ) ) ) for k, v in paramz )
		if method in list( 'be' ):
			with open( tpath, 'w' ) as tfile:
				tfile.write( '\n'.join( table ) )
		if method in list( 'b' ):
			if sys.platform == 'linux':
				os.system( f'xdg-open {tpath}' )
			input( f'Edit {tpath} then press enter...' )
		table = dict()
		if method in list( 'bi' ):
			with open( tpath ) as tfile:
				for line in tfile.readlines():
					key, *val = line.rstrip().split( '\t' )
					table.update( { key: val } )
			table.update( { " ": [] } )
			mycfg.params[ key1 ][ key2 ][ key3 ] = table


if __name__ == '__main__':
	if '--help' in sys.argv:
		print(
		 *[
		  'Reads .xlsx files from ../1_download and saves them as .json with a defined structure to ../2_convert',
		  'Use `2> errors.log` to save the error messages.',
		  '',
		  'Directory options:',
		  '   --no-chdir             no not change the base directory to the one of the script',
		  '   --rdir=<directory>     read .xlsx files from <directory>',
		  '   --wdir=<directory>     write .json files to <directory>',
		  '',
		  'Config options:',
		  '   --edit-experiments     export and import experiments mapping',
		  '   --export-experiments   export experiments mapping',
		  '   --import-experiments   import experiments mapping',
		  '   --ignore-prompts       skip new experiment prompts',
		 ],
		 sep='\n'
		)
		from os import _exit as q
		q( 0 )
	cfgpath = '2_mirtarbase_config.json'
	pign = '--ignore-prompts' in sys.argv
	#↘ usa el directorio con el cual se está trabajando
	if '--no-chdir' in sys.argv:
		print( 'Using', os.path.abspath( os.getcwd() ), 'as cwd' )
	#↘ o por defecto usa el directorio de este script
	else:
		newpath = os.path.dirname( sys.argv[ 0 ] )
		if not os.path.isabs( newpath ):
			newpath = os.path.join(
			 os.path.abspath( os.getcwd() ),
			 newpath,
			)
		os.chdir( newpath )
		print( 'Using', os.path.abspath( os.getcwd() ), 'as cwd' )
	rdir = '../1_download/'
	wdir = '../2_convert/'
	#↘ modifica las rutas de los directorios
	for arg in sys.argv:
		if arg.startswith( '--rdir' ):
			rdir = arg.replace( '--rdir=', '', 1 )
			print( 'Using', rdir, 'as reading dir' )
		if arg.startswith( '--wdir' ):
			wdir = arg.replace( '--wdir=', '', 1 )
			print( 'Using', rdir, 'as writing dir' )
	#↘ opciones para editar el campo `experiments`
	if '--edit-experiments' in sys.argv: edit_experiments( method='b' )
	elif '--export-experiments' in sys.argv: edit_experiments( method='e' )
	elif '--import-experiments' in sys.argv: edit_experiments( method='i' )
	else: main()
