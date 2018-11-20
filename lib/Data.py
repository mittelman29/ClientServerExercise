import bmemcached
import sqlite3

class Data:
    def __init__(self, dbName, debug=False):
        self.client = bmemcached.Client(('localhost:11311', ))
        self.databaseName = dbName
        self.debug = debug
        self.tableName = 'datastore'
        self.dbconn = ''
        self.keys = []

        self.connectToDatabase()
        self.createTable()
        self.populateCache()


    def _db(self, sql, commit=False):
        c = self.dbconn.cursor()
        c.execute(sql)
        if commit:
            self.dbconn.commit()

        return c.fetchall()

    def set(self, key, value):
        ''' 
        1. Set the key/value pair in the db
        2. Add key to self.keys
        3. Set the key/value pair in cache
        '''
        self._db("INSERT INTO %s VALUES('%s', '%s') ON CONFLICT(key) DO UPDATE SET value='%s'" % (self.tableName,key,value,value), True)

        if( not key in self.keys ):
            self.keys.append(key)

        return self.client.set(key,value)

    def get(self, key):
        ''' Get key/value pair from cache '''
        return self.client.get(key)

    def getAll(self):
        ''' Get all the key/value pairs from cache '''
        kv = {}
        for key in self.keys:
            kv[key] = self.get(key)

        return kv

    def delete(self, key):
        ''' 
        1. Delete key/value pair from db
        2. Remove key/value from self.keys
        3. Delete key/value from cache
        '''
        self._db("DELETE FROM %s where key='%s'" % (self.tableName,key), True)

        self.keys.remove(key)

        return self.client.delete(key)

    def connectToDatabase(self):
        if self.debug: print "Connecting to %s..." % self.databaseName
        self.dbconn = sqlite3.connect('./data/%s' % self.databaseName)
        if self.debug: print "Connected to sqlite version: %s" % self._db('SELECT SQLITE_VERSION()')

    def createTable(self):
        if self.debug: print "Creating table %s..." % self.tableName
        self._db("create table if not exists %s (key TEXT PRIMARY KEY, value TEXT)" % self.tableName)

    def populateCache(self):
        kvs = self._db("SELECT * FROM %s" % self.tableName)
        for row in kvs:
            self.keys.append(row[0])
            self.client.set(row[0],row[1])
            
    def __del__(self):
        if self.debug: print "Closing connection to %s" % self.databaseName
        self.dbconn.close()

        
         
        
