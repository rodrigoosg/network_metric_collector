#!/usr/bin/python

from nmc.procnetdev import ProcNetDev
from nmc.config import Config
from time import gmtime, strftime
import time
import socket
import sys
import schedule
import pydocumentdb.document_client as document_client
import uuid

def create(datetime, metric, recreate):
	# Get DB config
	config = Config()

	# """Renders the contact page."""
	client = document_client.DocumentClient(config.DOCUMENTDB_HOST, {'masterKey': config.DOCUMENTDB_KEY})

	# Read databases and take first since id should not be duplicated.
	db = next((data for data in client.ReadDatabases() if data['id'] == config.DOCUMENTDB_DATABASE))

	if (recreate == True):
		# Attempt to delete the database.  This allows this to be used to recreate as well as create
		try:
			db = next((data for data in client.ReadDatabases() if data['id'] == config.DOCUMENTDB_DATABASE))
			client.DeleteDatabase(db['_self'])
			db = None
		except:
			pass

	if (not db):
		# Create database
		db = client.CreateDatabase({ 'id': config.DOCUMENTDB_DATABASE })

	# Read collections and take first since id should not be duplicated.
	collection = next((collection for collection in client.ReadCollections(db['_self']) if collection['id'] == config.DOCUMENTDB_COLLECTION))

	if (not collection):
		# Create collection
		collection = client.CreateCollection(db['_self'],{ 'id': config.DOCUMENTDB_COLLECTION })

	# Create document
	document = client.CreateDocument(collection['_self'],
		{'id': str(uuid.uuid1()),
		 'timestamp': time.time(),
		 'datetime': datetime,
		 'value': metric,
		 'hostname': socket.gethostname(),
		 'sacleset': config.VMSS,
		 'name': config.DOCUMENTDB_DOCUMENT 
		})

last_bytes = 0

def job():
	global last_bytes
	pnd = ProcNetDev()
	tmp_bytes = last_bytes
	last_bytes = pnd['eth0']['transmit']['bytes']
	delta_bytes = last_bytes - tmp_bytes 
	now = strftime("%Y/%m/%dT%H:%M:%S", gmtime())
	print "Time: %s | Bytes Transmitted: %s B/s" % (now, int(delta_bytes))
	sys.stdout.flush()
	create(now, delta_bytes, False)
	print "Saved to database!"

if __name__ == "__main__":
	schedule.every(5).seconds.do(job)
	while True:
		schedule.run_pending()
		time.sleep(0.5)
