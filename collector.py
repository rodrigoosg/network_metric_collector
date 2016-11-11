#!/usr/bin/python

from nmc.procnetdev import ProcNetDev
from nmc.config import Config
from time import gmtime, strftime
import time
import socket
import sys
import pydocumentdb.document_client as document_client
import uuid

def save(datetime, bytes_transmitted):
	# Get DB config
	config = Config()

	# """Renders the contact page."""
	client = document_client.DocumentClient(config.DOCUMENTDB_HOST, {'masterKey': config.DOCUMENTDB_KEY})

	# Read databases and take first since id should not be duplicated.
	db = next((data for data in client.ReadDatabases() if data['id'] == config.DOCUMENTDB_DATABASE))

	# Read collections and take first since id should not be duplicated.
	collection = next((collection for collection in client.ReadCollections(db['_self']) if collection['id'] == config.DOCUMENTDB_COLLECTION))

	# Create document
	document = client.CreateDocument(collection['_self'],
		{'id': str(uuid.uuid1()),
		 'timestamp': time.time(),
		 'datetime': datetime,
		 'bytes_transmitted': bytes_transmitted,
		 'hostname': socket.gethostname(),
		 'sacleset': config.VMSS,
		 'name': config.DOCUMENTDB_DOCUMENT 
		})

def collect():
	pnd = ProcNetDev()
	bytes_transmitted = pnd['eth0']['transmit']['bytes']
	now = strftime("%Y/%m/%dT%H:%M:%S", gmtime())
	print "Time: %s | Bytes Transmitted: %s Bytes" % (now, int(bytes_transmitted))
	sys.stdout.flush()
	save(now, bytes_transmitted)
	print "Saved to database!"

if __name__ == "__main__":
	collect()
