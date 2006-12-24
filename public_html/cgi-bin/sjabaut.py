#! /home/valhallasw/bin/python
# $Id$
import cgi
import cgitb; cgitb.enable()

import sys, os
sys.path.append('/home/valhallasw/libs/python') #viewable through http://tools.wikimedia.de/~valhallasw/libs/python
import querier, sqlfunctions, cgifunctions

counter = 0
Q = querier.querier()
pagesOK = Q.do("select pl_title page_title from nlwiki_p.pagelinks join nlwiki_p.page on page_id=pl_from where page_title=\"Te_verwijderen_pagina's\" and page_namespace=4 and pl_namespace=0")

pages = Q.do("select page_title from nlwiki_p.page join nlwiki_p.categorylinks on page_id =cl_from where cl_to='Wikipedia:Auteur' and page_namespace=0")

print "Content-type: text/html; charset=UTF-8\n\n<html><body>";
print "<pre>$Id$</pre>"
print "%i te verwijderen, %i verwijdersjabloon <p><ul>" % (len(pagesOK),len(pages))
for page in pages:
   if page not in pagesOK:
       counter = counter + 1
       print "<li><a href='http://nl.wikipedia.org/wiki/%s'>%s</a></li>" % (page['page_title'], page['page_title'])

print "</ul><br>%s not OK</body></html>" % counter
