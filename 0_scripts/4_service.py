#!/bin/env -S python3 -i
import os
import pymongo
import sys
from flask import Flask, request, jsonify

# MISC
dbfields_int = ( 'gene_entrez', 'support_type', 'pubmed_ids' )
dbfields = ( '_id', 'mirtarbase_id', 'mirna_symbol', 'mirna_specie',
  'gene_symbol', 'gene_entrez', 'gene_specie',
  'experiments', 'support_type', 'pubmed_ids' )  # yapf: disable

def transform( key, arg ):
	if key in dbfields_int: return int( arg )
	return arg


# ENRICHMENT

from gprofiler import GProfiler

skeys = (
 'name',
 'native',
 'description',
)

oids = {
 'Arabidopsis thaliana': None,
 'Bombyx mori': None,
 'Bos taurus': 'btaurus',
 'Caenorhabditis elegans': 'celegans',
 'Canis familiaris': 'clfamiliaris',
 'Capra hircus': 'chircus',
 'Cricetulus griseus': 'cgchok1gshd',
 'Danio rerio': 'drerio',
 'Drosophila melanogaster': 'dmelanogaster',
 'Epstein Barr virus': None,
 'Gallus gallus': 'ggallus',
 'Glycine max': None,
 'Homo sapiens': 'hsapiens',
 'Human cytomegalovirus': None,
 'Kaposi sarcoma-associated herpesvirus': None,
 'Macaca nemestrina': 'mnemestrina',
 'Mus musculus': 'mmusculus',
 'Oryza sativa': None,
 'Oryzias latipes': 'olatipes',
 'Ovis aries': 'oaries',  # also 'oarambouillet'
 'Rattus norvegicus': 'rnorvegicus',
 'Solanum lycopersicum': None,
 'Sus scrofa': 'sscrofa',  # also 12 different variants
 'Taeniopygia guttata': 'tguttata',
 'Xenopus laevis': None,
 'Xenopus tropicalis': 'xtropicalis',
}


def enrichment( specie_mtb: str, genes: list ):
	print( 'Enriching', genes )  # debug
	gp = GProfiler( return_dataframe=False )
	specie = oids[ specie_mtb ]
	if not specie: return None
	res = gp.profile(
	 organism=specie,  # TODO: https://biit.cs.ut.ee/gprofiler/page/organism-list
	 query=genes,
	)
	for r in res:
		try:
			s = { key: r[ key ] for key in skeys }
			if 'GO:' in r[ 'native' ]: yield s
			if 'HP:' in r[ 'native' ]: yield s
		except:
			None


# FLASK PORTAL

## 0. Configuración y página principal
## muestra info sobre como usar la API
app = Flask( __name__ )


@app.route( '/', methods=[ 'GET' ] )
def mainmenu():  # TODO: update
	return jsonify( {
	 'help': 'please use one of the shown formats',
	 'routes': {
	  '/genes?<field>=<value>': {
	   'description': 'get genes regulted by mirna',
	   'allowedtags': {
	    '<field>': dbfields,
	    '<value>': '*any',
	   }
	  },
	  '/mirnas?gene=<id>': 'get mirnas regulting a gene',
	 },
	} )


## 1. Consulta de miRTarBase
## recibe uno o varios campos y devuelve sus MTI
@app.route( '/search', methods=[ 'GET' ] )
def mtbase():
	print( 'Received GET in /search' )
	rargs = { key: transform(key,arg)
	  for key, arg in request.args.items()
	  if key in dbfields }  # yapf: disable
	res = list( mycol.find( rargs ) )
	# TODO: check https://stackoverflow.com/a/12437945
	return jsonify( res )


## 1. Qué genes están regulados por un determinado mirna.
## recibe un `mirna_symbol` y devuelve su caracterización funcional
@app.route( '/detail', methods=[ 'GET' ] )
def detail():
	print( 'Received GET in /detail' )
	# recibe los genes de la base de datos
	tar = { '_id': 0, 'gene_symbol': 1, 'gene_specie': 1 }
	key = 'mirna_symbol'
	arg = request.args.get( key )
	res = list( mycol.find( { key: arg }, tar ) )
	# separa los genes por especie
	con = dict()
	for r in res:
		try:
			con[ r[ 'gene_specie' ] ].append( r[ 'gene_symbol' ] )
		except:
			con[ r[ 'gene_specie' ] ] = [ r[ 'gene_symbol' ] ]
	# return jsonify( con )
	# enriquece con funciones
	res = { specie: list(enrichment( specie, genes ))
	 for specie, genes in con.items() }  # yapf: disable
	return jsonify( res )


if __name__ == "__main__":
	if '--help' in sys.argv:
		print(
		 *[
		  'Starts a local service to access the database.',
		  '',
		  'Options:',
		  '   --mongo-url=<url>      connect to mongodb in <url> (default localhost:27017)',
		  '   --mongo-db=<name>      use <name> collection from mongodb (default tfm)',
		 ]
		)
		from os import _exit as q
		q( 0 )
	murl = 'localhost:27017'
	mname = 'tfm'
	#↘ opciones de linea de comandos
	for arg in sys.argv:
		if arg.startswith( '--mongo-url=' ):
			murl = arg.replace( '--mongo-url=', '', 1 )
			print( 'Using', murl, 'as url' )
		elif arg.startswith( '--mongo-db=' ):
			mname = arg.replace( '--mongo-db=', '', 1 )
			print( 'Using', mname, 'as database name' )
	myclient = pymongo.MongoClient( f'mongodb://{murl}/' )
	mydb = myclient[ mname ]
	mycol = mydb[ 'mirtarbase' ]
	app.run( debug=True )
""" para probar
http://127.0.0.1:5000/search?gene_symbol=RAN
http://127.0.0.1:5000/search?mirna_symbol=hsa-miR-5088-3p
http://127.0.0.1:5000/detail?mirna_symbol=hsa-miR-5088-3p
"""
