from datetime import datetime

class Config():

	DOCUMENTDB_HOST = 'https://<documentdb>.documents.azure.com:443/'
	DOCUMENTDB_KEY = "MY_KEY_ENDING_IN_=="

	DOCUMENTDB_DATABASE = 'database name'
	DOCUMENTDB_COLLECTION = 'collection name'
	DOCUMENTDB_DOCUMENT = 'document name'
	VMSS = 'VM Sacle Set Name'