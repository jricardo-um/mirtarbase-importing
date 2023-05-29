#!/bin/env -S python3 -i

import json
from flask import Flask, request, jsonify
from flask_mongoengine import MongoEngine

xxyzx = None
app = Flask( __name__ )
app.config[ 'MONGODB_SETTINGS' ] = { 'db': 'tfm00', 'host': 'localhost', 'port': 27017 }
db = MongoEngine()
db.init_app( app )


class User( db.Document ):
	_id = db.StringField()
	gene_symbol = db.StringField()
	
	def to_json( self ):
		return { "_id": self._id, "email": self.gene_symbol }


@app.route( '/', methods=[ 'GET' ] )
def mainmenu():
	return jsonify( {
		'help': 'please use one of the shown formats',
		'fmts': {
		'/genes?mirna=<id>': 'get genes regulted by mirna',
		'/mirnas?gene=<id>': 'get mirnas regulting a gene',
		}
	} )


### 1. Qué genes están regulados por un determinado mirna.
@app.route( '/genes', methods=[ 'GET' ] )
def genes():
	name = request.args.get( 'mirna' )
	user = User.objects( _id=name )
	if not user:
		return jsonify( { 'error': 'data not found', 'mirna': name } )
	else:
		return jsonify( user.to_json() )


### 2. Qué mirnas regulan determinados genes.
@app.route( '/mirnas', methods=[ 'GET' ] )
def mirnas():
	name = request.args.get( 'gen' )
	print( name )
	return jsonify( { 'name': name } )


if __name__ == "__main__":
	app.run( debug=True )
	print( 'name', xxyzx, type( xxyzx ) )
