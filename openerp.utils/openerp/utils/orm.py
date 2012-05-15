#encoding=utf-8

class OsvMixin(object):
    """
    A mixin class for osv.osv objects to add util methods to openobject models
    """
    def query(self, cr, uid, search_query, context=None):
        """A shortcut for orm "search and browse" methods:
            given a model as pool_obj and a search query as search_query
            returns a list of objects as poll.obj.browse() would do

            to be used instead of:
                obj = self.pool.get('model_name')
                ids = obj.search(cr, uid, search_query)
                objects_list = obj.browse(cr, uid, ids)
            this way:
                obj = self.pool.get('model_name')
                objects_list = utils.query(obj, cr, uid, search_query)
        """
        ids = self.search(cr, uid, search_query, context)
        return self.browse(cr, uid, ids, context)
    
    def all(self, cr, uid, context=None):
        """Returns the list of all objects """
        return self.query(cr, uid, [], context)
    

