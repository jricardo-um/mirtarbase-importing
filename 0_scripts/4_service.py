#!/bin/env -S python3 -i
from flask import Flask, request, jsonify

# GPROFILER
from gprofiler import GProfiler


def enrichment( specie_mtb: str, genes: list ):
	gp = GProfiler( return_dataframe=False )
	res = gp.profile(
	 organism='hsapiens',  # TODO: https://biit.cs.ut.ee/gprofiler/page/organism-list
	 query=genes,
	)
	for r in res:
		yield r[ 'native' ]


# METHOD 1 (broken)
from flask_mongoengine import MongoEngine

app = Flask( __name__ )
app.config[ 'MONGODB_SETTINGS' ] = { 'db': 'tfm00', 'host': 'localhost', 'port': 27017 }
db = MongoEngine()
db.init_app( app )


class User( db.Document ):
	_id = db.StringField()
	gene_symbol = db.StringField()
	
	def to_json( self ):
		return { "_id": self._id, "gene_symbol": self.gene_symbol }


def retrieve_with_mongoengine( **kwds ):
	user = User.objects( **kwds )
	if user: return user.to_json()
	else: raise ValueError( "Can't make this work" )


# METHOD 2 (pymongo)
import pymongo

myclient = pymongo.MongoClient( 'mongodb://localhost:27017/' )
mydb = myclient[ 'tfm00' ]
mycol = mydb[ 'mirtarbase' ]


def retrieve_with_pymongo( conditions, fields ):
	myres = mycol.find( conditions, fields )
	yield from myres


# FLASK PORTAL


## 0. Página principal
## muestra info de uso
@app.route( '/', methods=[ 'GET' ] )
def mainmenu():
	return jsonify( {
	 'help': 'please use one of the shown formats',
	 'fmts': {
	  '/genes?mirna=<id>': 'get genes regulted by mirna',
	  '/mirnas?gene=<id>': 'get mirnas regulting a gene',
	 },
	} )


## 1. Qué genes están regulados por un determinado mirna.
## recibe un `_id` y devuelve un `gene_symbol`
@app.route( '/genes', methods=[ 'GET' ] )
def genes():
	name = request.args.get( 'mirna' )
	try:
		res = retrieve_with_mongoengine( _id=name )
		enr = None
	except:
		res = retrieve_with_pymongo( { '_id': name }, { '_id': 0, 'gene_symbol': 1, 'specie': 1 } )
		res = next( res, { 'gene_symbol': None, 'specie': None } )
		enr = enrichment( res[ 'specie' ], [ res[ 'gene_symbol' ] ] )
		res[ 'funcs' ] = list( enr )  # TODO: ver si es korrecto
	return jsonify( res )


## 2. Qué mirnas regulan determinados genes.
## recibe un `gene_symbol` y se devuelve uno o varios `_id`s
@app.route( '/mirnas', methods=[ 'GET' ] )
def mirnas():
	name = request.args.get( 'gen' )
	try:
		res = retrieve_with_mongoengine( gene_symbol=name )
	except:
		res = retrieve_with_pymongo( { 'gene_symbol': name }, { '_id': 1 } )
		res = list( i for i in res )
	return jsonify( res )


if __name__ == "__main__":
	app.run( debug=True )
	# para probar http://127.0.0.1:5000/genes?mirna=MIRT134276

# en la respuesta poner info de los codigos g_profiler
# cambiar el mirna=
# añadir evidence= strong|weak
# pasar toda la fila
