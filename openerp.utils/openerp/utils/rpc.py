# encoding=utf-8

import xmlrpclib


class Dict(dict):
    """A class to extend python dict to access dictionary by object notation"""
    def __getattr__(self, attr):
        return self[attr]
    



class Connection(object):
    """A class to estabilish an xmlrpc lib connection to openerp server
        Provides methods to query data: search, read, write, unlink
    >>> conn = Connection('dbname', 'username', 'passwd', 
    ...     'http://localhost:8169/xmlrpc/common',
    ...     'http://localhost:8169/xmlrpc/object')
    >>> conn.search('res.partner') # doctest: +ELLIPSIS
    [...]
    """
    def __init__(self, dbname, username, pwd, common_url, object_url):
        self.dbname = dbname
        self.username = username
        self.pwd = pwd
        self.common_url = common_url
        self.uid = self.get_uid()
        self.sock = xmlrpclib.ServerProxy(object_url)
    
    def get_uid(self):
        sock_common = xmlrpclib.ServerProxy(self.common_url)
        uid = sock_common.login(self.dbname, self.username, self.pwd)
        return uid
    
    def search(self, model, query=[]):
        return self.sock.execute(self.dbname, self.uid, self.pwd, model , 'search', query)
    
    def read(self, model, ids, fields=[]):
        return self.sock.execute(self.dbname, self.uid, self.pwd, model , 'read', ids, fields)
    
    def browse(self, model, ids, fields=[]):
        res = self.read(model, ids, fields)
        if isinstance(res, list):
            return [Dict(d) for d in res]
        else:
            return Dict(res)
    
    def write(self, model, ids, values):
        return self.sock.execute(self.dbname, self.uid, self.pwd, model, 'write', ids, values)
    
    def unlink(self, model, ids):
        return self.sock.execute(self.dbname, self.uid, self.pwd, model, 'unlink', ids)
    
    def create(self, model, vals, context={}):
        return self.sock.execute(self.dbname, self.uid, self.pwd, model, 'create', vals, context)
    
    def call(self, model, method, *args, **kwargs):
        """calls a method on a model passing the given args """
        return self.sock.execute(self.dbname, self.uid, self.pwd, model, method, *args, **kwargs)

