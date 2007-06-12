"""
MuSQLdb command abstraction layer, mysql_autoconnection version
"""
#
# (C) 2006-2007 Merlijn 'valhallasw' van Deen,
#
# Distributed under the terms of the MIT license.
#
__version__ = '$Id$'

# Usage:
# ------
# import querier
# var = querier.querier(host="localhost", etc) #same as MySQLdb.connect attributes
# result = var.do("MySQL query")               #same as cursor.execute attributes
#
# all other functions are made purely for use on mediawiki tables.
#
# The result is a list of dictionaries: [{'colname': data1, 'colname2': data2},{'colname': data11, 'colname2': data22}]

import os
import MySQLdb, MySQLdb.cursors, mysql_autoconnection
import wikipedia

class querier:
    """Class for a database querier"""
    def __init__(self,*args,**kwargs):
        """Initializer function"""
        def _callback(conn_obj):
            wikipedia.output(u'Connection has been. Reconnecting in %i seconds (attempt %i/%i)' % (conn_obj, conn_obj.current_retry*conn_obj.retry_timeout, conn_obj.current_retry, conn_obj.max_retries))
        newkwargs = {
            'read_default_file': os.path.expanduser('~' + os.sep + '.my.cnf'),
            #read toolserver database information (please make sure the host is listed in the file)
            'cursorclass': MySQLdb.cursors.DictCursor,
            'retry_timeout': 5,
            'max_retries': 4,
            'callback': _callback,
        }

        newkwargs.update(kwargs)
        self.db = mysql_autoconnection.connect(*args, **newkwargs)

    def do(self, *args,**kwargs):
        """SQL Query function"""
        transpose = kwargs.pop('transpose', False)
        mediawiki = kwargs.pop('mediawiki', False)

        cursor = self.db.cursor()
        cursor.execute(*args,**kwargs)
        retval = tuple(cursor.fetchall())
        cursor.close()

        if mediawiki:
            convertutf8(retval)

        if transpose:
            if len(retval) > 0:
                return dict(zip(retval[0].keys(),zip(*map(dict.values,retval))))
                # 17:36 < dodek> valhalla1w, you're posting it on obfuscated python coding contest or sth? :)
                # 17:36 < valhalla1w> actually i'm trying to transpose a list of dicts to a dict of tuples
                # 17:42 < valhalla1w> s/list/tuple
            else:
                return {}
        return retval

    def commit(self):
        return self.db.commit()

def convertutf8(rows):
    for row in rows:
        for col in row:
            if type(row[col]) == str:
                row[col] = row[col].decode('utf-8')