# $Id$

# exceptions
class NoSuchPage(Exception):
        def __init__(self, value):
            self.value = value
        def __str__(self):
            return repr(self.value)

class NoSuchDatabase(Exception):
        def __init__(self, value):
            self.value = value
        def __str__(self):
            return repr(self.value)
            
# defs
def getpid(querier,db,title,namespace):
  page = title.replace(' ','_')
  page = page[:1].upper() + page[1:]
  column = querier.do("SELECT page_id from %s.page where page_title=%r and page_namespace=%i" % (db, page, namespace))
  if column:
    return column[0]['page_id']
  else:
    raise NoSuchPage(page)
  
def getdb(querier, lang):
  column = querier.do("SELECT dbname FROM toolserver.wiki WHERE domain=%r" % (lang + '.wikipedia.org'))
  
  if column:
    return column[0]['dbname']
  else:
    raise NoSuchDatabase(lang)
  
  #import re
  #return re.sub('-','_',lang)+'wiki_p'
  