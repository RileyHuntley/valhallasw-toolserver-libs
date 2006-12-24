# $Id$
import os, sys
os.environ['TZ'] = 'Europe/Amsterdam'
sys.path.append('..')

import time, datetime
import querier, wikipedia
from useful import iter_islast

wikipedia.setAction(u'Orphan-Overlegupdater van [[Gebruiker:Valhallasw]] ([[Gebruiker:Valhallasw/toolserver/bot|changelog]])')

now = datetime.datetime(*time.localtime()[0:5])

P = wikipedia.Page(wikipedia.getSite(u'nl'), "Wikipedia:OrphanOverleg")
Q = querier.querier()
statistiek = {}

output = unicode(now.strftime("=Orphan-overlegpagina's (%Y%m%d, %H%M)=\n"))

print "Ophalen orphanpagina's..."
results = Q.do("select p2.page_title, p2.page_id, p2.page_len from nlwiki_p.page as p1 right join nlwiki_p.page as p2 on p1.page_title = p2.page_title and p1.page_namespace=0 where p2.page_namespace=1 and p1.page_title IS NULL;")
print str(len(results)) + ' items;'
output += str(len(results)) + 'items;'

workwith = list(results)

metslash = ""

for page in workwith:
  if (page['page_title'].rfind('/') > -1):
    if (len(metslash) != 0):
      metslash += " or cl_from="
    metslash += str(page['page_id'])

heeftcat = Q.do("select cl_from from nlwiki_p.categorylinks where cl_from=" + metslash + " and cl_to='Wikipedia:Archief';", transpose=True)

for page in workwith:
  if page['page_id'] in heeftcat['cl_from']:
    workwith.remove(page)

geendeletes = [];

print str(len(workwith)) + " pagina's om te verwerken"
output += str(len(workwith)) + u" pagina's om te verwerken; "
output += str(len(results)-len(workwith)) + u" pagina's genegeerd.\n"
output += u'{| class = "prettytable"\n'
output += u'|-\n'
output += u'! rowspan=2 | Pagina\n'
output += u'! colspan=4 | Hoofdpagina\n'
output += u'|-\n'
output += u'! Datum || Actie || Gebruiker || Reden\n'
output += u'|-\n'


for page in workwith:
  #retrieve deletion history
  delhist = Q.do("select log_timestamp, log_action, user_name, log_comment from nlwiki_p.logging inner join nlwiki_p.user_ids on log_user=user_id where log_namespace=0 and log_title=%s and log_type='delete' order by log_timestamp desc limit 1",page['page_title'], mediawiki=True);
  
  print page['page_title'] + " ("+str(len(delhist))+" deletes)"
  page = Q.doutf8(page)
  if len(delhist) == 0:
    geendeletes.append(page)
    continue
 
  output += u'| rowspan=' + str(len(delhist)) + u' | [[Overleg:' + page['page_title'].replace('_',' ') + u']]</br>(' + str(page['page_len']) + u' bytes)\n'
  
  for histitem in delhist:
    tstamp = time.strftime("%d %b %y, %H:%m", time.strptime(histitem['log_timestamp'],"%Y%m%d%H%M%S"))
    output += u'| ' + tstamp + u' || ' + histitem['log_action'] + u' || [[User:' + histitem['user_name'] + u'|]] || <nowiki>' + histitem['log_comment'] + u'</nowiki>\n|-\n'
    if histitem['user_name'] in statistiek:
      statistiek.update({histitem['user_name']: statistiek[histitem['user_name']]+1})
    else:
      statistiek.update({histitem['user_name']: 1})

output += u'|}\n\n'
output += u"== Pagina's zonder deletion history ==\n"

for page in geendeletes:
  output += u'* [[Talk:' + page['page_title'] + u']]\n'

totaalover = len(workwith) - len(geendeletes)

output += u'\n\n==Statistiek==\n'
for pair in sorted(statistiek.iteritems(), key=lambda x: x[1], reverse=True):
  output += u'* [[User:'+pair[0]+u']] ('+str(pair[1])+u' pages (' + str(round((0.0+pair[1])*100/totaalover,1)) + u'%))\n';

P.put(output)
