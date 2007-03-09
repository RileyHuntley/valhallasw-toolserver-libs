# $Id$
import os
os.environ['TZ'] = 'Europe/Amsterdam'

def month(val):
  return ['januari', 'februari', 'maart', 'april', 'mei', 'juni', 'juli',
          'augustus', 'september', 'oktober', 'november', 'december'][int(val)-1]
										
import time, datetime
if time.localtime()[3] == 0:
  import wikipedia
  
  wikipedia.setAction(u'Wikinewsupdater van [[w:Gebruiker:Valhallasw]] ([[w:Gebruiker:Valhallasw/toolserver/bot|changelog]])')
  
  now = datetime.datetime(*time.localtime()[0:5])
    
  pagename = "Wikinews:" + time.strftime("%Y")+"/"+month(time.strftime("%m"))+"/"+time.strftime("%d").strip('0')
  inhoud = '<DynamicPageList>\ncategory='+time.strftime("%d").strip('0')+' '+month(time.strftime("%m"))+' '+ time.strftime("%Y")+'\ncategory=Gepubliceerd\nnotcategory=Dispuut\nnotcategory=Lokaal belang\nsuppresserrors=true\n</DynamicPageList>'
    
  P = wikipedia.Page(wikipedia.getSite(u'nl',u'wikinews'), pagename)
  if not P.exists():          # als 'ie bestaat doe ik lekker niks ;)
    P.put(inhoud)
    
  #nu nog de pagina voor over een week toevoegen
  dan = now + datetime.timedelta(days=7)

  pagename = "Wikinews:" + dan.strftime("%Y")+"/"+month(dan.strftime("%m"))+"/"+dan.strftime("%d").strip('0')
  inhoud = "<DynamicPageList>\ncategory="+dan.strftime("%d").strip('0')+' '+month(dan.strftime("%m"))+' '+ dan.strftime("%Y")+'\ncategory=Gepubliceerd\nnotcategory=Dispuut\nnotcategory=Lokaal belang\nsuppresserrors=true\n</DynamicPageList>'
 
  P = wikipedia.Page(wikipedia.getSite(u'nl',u'wikinews'), pagename)
  if not P.exists():          # als 'ie bestaat doe ik lekker niks ;)
    P.put(inhoud)
  
#else:
  #print time.strftime("--not 00:00 yet. current time: %H:%M:%S") 
