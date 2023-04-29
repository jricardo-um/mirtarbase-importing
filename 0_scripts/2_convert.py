#!/bin/env -S python3 -i
import json
import os
import pandas
import pathlib
import sys
from typing import Literal


class config:
	funcmap = dict()
	
	#↘ guarda el nombre de archivo de los ajustes
	def __init__( self, cfgfile ):
		self.cfgfile = cfgfile
	
	#↘ carga los ajustes al empezar
	def __enter__( self ):
		with open( self.cfgfile ) as f:
			self.params: dict[ str:dict ] = json.load( f )
		return self
	
	#↘ guarda los ajustes al acabar
	def __exit__( self, exc_type, exc_val, exc_tb ):
		with open( self.cfgfile, 'w' ) as f:
			json.dump( self.params, f, indent='\t' )
	
	#↘ devuelve la columna que actúa como índice
	def column_as_identifier( self ):
		key = "column_as_index"
		if key in self.params:
			return self.params[ key ]
		else:
			new = input( 'Please enter column name to use as ID: ' )
			self.params[ key ] = new
			print( ' Updated!' )
			return new
	
	#↘ devuelve si la columna tiene el atributo "custom"
	def column_is_custom( self, key2 ):
		key1 = "column_configs"
		key3 = "custom"
		if key2 not in self.params[ key1 ]:
			self.params[ key1 ].update( { key2: dict() } )
		try:
			return self.params[ key1 ][ key2 ][ key3 ]
		except KeyError:
			afirm = ( 'y', 'yes', 's', 'si', 'sí' )
			new = input( f'Set column `{key2}` as custom? ' )
			new = True if new in afirm else False
			self.params[ key1 ][ key2 ][ key3 ] = new
			print( ' Updated!' )
			return new
	
	#↘ convierte el título de la columna a los títulos del correo
	def colkey( self, key2 ):
		key1 = "column_configs"
		key3 = "savename"
		try:
			return self.params[ key1 ][ key2 ][ key3 ]
		except KeyError:
			new = input( f'Enter MongoDB name for `{key2}`: ' )
			self.params[ key1 ][ key2 ][ key3 ] = new
			print( ' Updated!' )
			return new
	
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
		return list( isthisajoke( val, separators.copy() ) )
		if False:
			# es mi implementación original
			# pero el excel está MUUUY mal hecho
			for separator in separators:
				if separator in val:
					return val.split( separator )
			return [val] # yapf: disable
	#↕ registra la función para usarla al procesar columnas
	funcmap.update( { "multisep": separe_multiple_separators } )
	
	#   evita nombres diferentes para la misma entrada
	#↘ (en nuestro caso, "5pRNA"="5'RNA"="5p-RNA"=etc…)
	def control_vocabulary( self, val: str, key2 ):
		if type( val ) is list:
			return list( self.control_vocabulary( v, key2 ) for v in val )
		key1 = "column_configs"
		key3 = "allowed_values"
		try:
			allowed = self.params[ key1 ][ key2 ][ key3 ]
			return allowed[ val ]
		except KeyError:
			new = input( f'Enter allowed value for `{val}` in column `{key2}`: ' )
			if new == '': new = val
			try:
				self.params[ key1 ][ key2 ][ key3 ][ val ] = new
			except KeyError:
				self.params[ key1 ][ key2 ][ key3 ] = { val: new }
			print( ' Updated!' )
			return new # yapf: disable
	#↕ registra la función para usarla al procesar columnas
	funcmap.update( { "vocabset": control_vocabulary } )
	
	#↘ convierte a `int`
	def asinteger( self, val, key2 ):
		return int(val) # yapf: disable
	#↕ registra la función para usarla al procesar columnas
	funcmap.update( { "integer": asinteger } )
	
	#↘ ignora el valor de esa columna
	def ignore( self, val, key2 ):
		return self.ignore # yapf: disable
	#↕ registra la función para usarla al procesar columnas
	funcmap.update( { "ignore": ignore } )
	
	#   devuelve las funciones adecuadas para cada columna
	#↘ (de entre las registradas antes)
	def custom_funcs( self, key2 ):
		key1 = "column_configs"
		key3 = "custom_functions"
		try:
			for val in self.params[ key1 ][ key2 ][ key3 ]:
				yield self.funcmap[ val ]
		except KeyError:
			self.params[ key1 ][ key2 ][ key3 ] = list()
			while True:
				new = input( f'Enter funcs for `{key2}`: ' )
				if new == '': break
				list.append( self.params[ key1 ][ key2 ][ key3 ], new )
				print( ' Updated!' )
			for val in self.params[ key1 ][ key2 ][ key3 ]:
				yield self.funcmap[ val ]


#↘ itera sobre los archivos de una carpeta
def fileiter( folder, filename ):
	cwd = pathlib.Path( folder ).resolve()
	for file in cwd.glob( filename ):
		yield file


#   modifica valores para diccionarios arbitrariamente anidados
#   underdict( dikt, 'key1:key2:key3', val, ':' )
#↘         `dikt['key1']['key2']['key3']=val`
def underdict( dikt: dict, remainingkeys: str, val: any, sep=':' ):
	"""Turns (dict,'key1:key2:key3',val) into dict['key1']['key2']['key3']=val

	Args:
		 dikt (dict): dictionary whose value is to be updated
		 remainingkeys (str): keys for the value to update
		 val (any): value to update
		 sep (str, optional): separator for `remainingkeys`. Defaults to ':'.
	"""
	key, sep, keys = remainingkeys.partition( sep )
	if sep == '':
		dikt[ key ] = val
	else:
		if key not in dikt: dikt.update( { key: dict() } )
		underdict( dikt[ key ], keys, val, sep )


def main():
	#↘ carga la configuración, incluye la lista de valores permitidos para las columnas
	with config( '2_convert_config_mirtarbase.json' ) as mycfg:
		#↘ itera sobre todos los archivos deseados
		for filepath in fileiter( '../1_download', '*.xlsx' ):
			#↓ diccionario para almacenar los datos importados
			mydatabase: dict[ dict ] = dict()
			filename = pathlib.Path( filepath ).name
			print( 'Reading file', filename )
			print( 'This can take a while...' )
			#↓ lee la base de datos con pandas
			fileread = pandas.read_excel( filepath )
			#↘ itera sobre (índice, fila) del dataframe
			for ind, row in fileread.iterrows():
				print( '\x1b[F\x1b[K', 'Processing row', ind )
				#↓ guarda la columna que hace de ID
				entryname = row[ mycfg.column_as_identifier() ]
				if entryname not in mydatabase:
					mydatabase.update( { entryname: dict() } )
				#↘ itera sobre (columna, valor) de la fila
				for col, val in row.items():
					#↘ modifica los valores si es necesario
					if mycfg.column_is_custom( col ):
						for func in mycfg.custom_funcs( col ):
							val = func( mycfg, val, col )
						if val == mycfg.ignore: continue
					#↘ evita que pandas lo guarde algún valor como `datetime`
					else:
						val = str( val )
					col = mycfg.colkey( col )
					#↓ pone el valor en mi "base de datos json"
					underdict( mydatabase[ entryname ], col, val )
			#↓ guarda la base de datos como json
			exportfilepath = '../2_convert/' + filename + '.json'
			pathlib.Path( exportfilepath ).parent.mkdir( parents=True, exist_ok=True )
			with open( exportfilepath, 'w' ) as file:
				json.dump( mydatabase, file, indent='\t' )


#↘ para fácil edición de los experimentos
def edit_experiments( method: Literal[ 'b', 'i', 'e' ] = 'b', tpath='./2_temp_edit.tsv' ):
	with config( '2_convert_config_mirtarbase.json' ) as mycfg:
		key1, key2, key3 = "column_configs", "Experiments", "allowed_values"
		table = mycfg.params[ key1 ][ key2 ][ key3 ].items()
		table = tuple( '\t'.join( pair ) for pair in table )
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
					key, val = line.strip().split( '\t' )
					table.update( { key: val } )
		mycfg.params[ key1 ][ key2 ][ key3 ] = table


#   separa por todos los separadores a la vez
#↘ "item1//item2;item3//item4//item5" -> ['item1','item2','item3','item4','item5']
def isthisajoke( text: str, separators: list[ str ] ):
	if not len( separators ):
		yield text
	else:
		separator = separators.pop()
		for value in text.split( separator ):
			yield from isthisajoke( value, separators.copy() )


if __name__ == '__main__':
	if '--help' in sys.argv:
		print(
			'''Command line options:
--no-chdir          	no not change the directory to the one of the script
--edit-experiments  	export and import experiments mapping
--export-experiments	export experiments mapping
--import-experiments	import experiments mapping'''
		)
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
	if '--edit-experiments' in sys.argv: edit_experiments( method='b' )
	elif '--export-experiments' in sys.argv: edit_experiments( method='e' )
	elif '--import-experiments' in sys.argv: edit_experiments( method='i' )
	else: main()

# CATÁLOGO DE FLECHAS
#  ↰↱↲↳
# ←↑→↓↔↕↖↗↘↙
# ⇐⇑⇒⇓⇔⇕⇖⇗⇘⇙
# ⇦⇧⇨⇩ ⇪⇫⇬⇭
# ⇇⇈⇉⇊⇄⇅⇆ ⇤⇥
