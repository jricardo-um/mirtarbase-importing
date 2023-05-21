#!/bin/env -S python3 -i
import os
import requests
import sys
import time
from multiprocessing import Manager, Process, Queue


def uname( url: str ) -> str:
	#> returns the file name from the url
	return url.rsplit( '/', 1 )[ -1 ]


def downloader( url_list: Queue, current: list, i ) -> requests.models.Response:
	#> downloads from the url
	while not url_list.empty():
		url = url_list.get()
		current.append( uname( url ) )
		req = requests.get( url, stream=True )
		with open( savefolder + uname( url ), 'wb' ) as file:
			for char in req.iter_content():
				file.write( char )
		current.remove( uname( url ) )


def main():
	#> folder to save the files
	global savefolder
	savefolder = '../1_download/'
	os.makedirs( savefolder, exist_ok=True )
	with Manager() as mgr:
		#> list of files to download
		url_list = mgr.Queue()
		with open( './1_download_list.txt' ) as url_list_file:
			for line in url_list_file.readlines():
				url_list.put( line.strip() )
		current = mgr.list()
		#> multiprecoessing
		procs: list[ Process ] = list()
		for i in range( 3 ):
			p = Process( target=downloader, args=( url_list, current, i ) )
			p.start()
			procs.append( p )
		print( 'Downloading:' )
		#> to watch the queue
		for job in procs:
			while job.is_alive():
				jn = '  [' + '] ['.join( current ) + '] '
				rm = url_list.qsize()
				if rm: jn += '{+' + str( rm ) + '}'
				print( jn, end='\r' )
				time.sleep( 1 )
				print( ' ' * len( jn ), end='\r' )
			job.join()
		print()


if __name__ == '__main__':
	if '--help' in sys.argv:
		print( '''Command line options:
--no-chdir             no not change the directory to the one of the script''' )
		exit( 0 )
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
	main()
