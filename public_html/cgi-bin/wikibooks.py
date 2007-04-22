#! /home/valhallasw/bin/python
# $Id$
#
# Script to output users who have edited a certain article, but who have not
# edited their user page with the edit comment {{dubbel}}
#
# Created for the move to GFDL/CC-BY-SA on nl.wikibooks
#
# (C) 2007 by Merlijn 'valhallasw' van Deen
# Licensed under the MIT license. (eg. you are free to copy and distribute, as
# long as you mention my name in both source and binary versions)

import cgi
import cgitb; cgitb.enable()
import re;
import sys, os, time
starttime = time.time()

sys.path.append('/home/valhallasw/libs/python') #viewable through http://tools.wikimedia.de/~valhallasw/libs/python
import querier, sqlfunctions, cgifunctions

form= cgi.FieldStorage(keep_blank_values=1)

if 'articles' not in form:
	articles = ''
else:
	articles = form['articles'].value

if 'source' in form:
	print "Content-type: text/plain;charset=utf-8\n\n"
	n = open(sys.argv[0])
	print n.read()
	sys.exit(0)
	
print "Content-type: text/html;charset=utf-8\n\n"
print "<html><head><title>nl.wikibooks Evil Non-Dual User Search</title></head><link rel='stylesheet' type='text/css' href='../main.css'><body><h1>Evil Non-Dual User Search Pro(TM)</h1>"
print """<form method=post action="wikibooks.py">
           Artikelen: (een per regel):<br/> <textarea name=articles cols=80 rows=5>%s</textarea><br/>
	   <input type=submit>
	   </form><hr>""" % articles
if 'articles' in form:
  Q = querier.querier();
  Q.do("use nlwikibooks_p")
  for article in articles.split('\n'):
  	article = article.strip().replace(" ","_")
	if len(article) == 0:
		continue
  	print "<h2><a href='http://nl.wikibooks.org/w/index.php?title=%s&redirect=no'>%s</a></h2>" % (article, article)
	res = Q.do(""" select replace(user_name, ' ', '_') as page_title, num
		 from revision
		 right join
		 	(SELECT page_id as user_page, rev_user_text AS user_name, count(rev_id) AS num
		        FROM revision
			LEFT JOIN page ON page_title = replace(rev_user_text, ' ', '_') 	AND page_namespace = 2
			WHERE rev_page=(select page_id
				from page
				where page_title=%s
				and page_namespace=0
			)
			AND rev_timestamp < '20070415000000'
			GROUP BY rev_user_text
		) as user
		on rev_page=user_page
			and rev_user_text=user_name
			and cast(rev_comment as char) = "{{dubbel}}"
		where rev_id IS NULL
		order by num desc; """, article )
	print "<table>"
	for row in res:
		print "<tr><td><a href='http://nl.wikibooks.org/wiki/Gebruiker:%s'>%s</a></td><td>%i</td></tr>" % (row['page_title'], row['page_title'], row['num'])
	if len(res) == 0:
		print "This page should be dual-licenced! <small>(or does not exist)</small>"
	print "</table>"
print "<p class='footer'>(C) 2007 by Merlijn 'valhallasw' van Deen. Licensed under the MIT license. <a href='?source'>View source</a> - <a href='/websvn/listing.php?repname=valhallasw&path=/public_html/cgi-bin/'>svn browser</a> - Render time: %.2fs<br><pre>$Id$</pre></p>" % (time.time() - starttime)
print "</body></html>"
