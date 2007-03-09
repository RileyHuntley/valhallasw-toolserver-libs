# $Id$
import os
os.environ['TZ'] = 'Europe/Amsterdam'

import time, datetime

if time.localtime()[3] == 0:
  import wikipedia
  
  wikipedia.setAction(u'Verwijderlijstupdater van [[Gebruiker:Valhallasw]] ([[Gebruiker:Valhallasw/toolserver/bot|changelog]])')
  
  now = datetime.datetime(*time.localtime()[0:5])
  intwoweeks = now + datetime.timedelta(weeks=2)
  
  pagename = now.strftime("Wikipedia:Te verwijderen afbeeldingen/Toegevoegd %Y%m%d")
  
  inhoud = "<noinclude>{{VerwijderNav|Afbeeldingen}}</noinclude>\n"
  inhoud = inhoud + "== Toegevoegd " + now.strftime("%d/%m") + " te verwijderen vanaf "+ intwoweeks.strftime("%d/%m") + " ==\n"
  inhoud = inhoud + "<includeonly><span class='plainlinks'>[{{SERVER}}{{localurl:{{NAMESPACE}}:{{subst:PAGENAME}}|action=watch}} Dagpagina aan volglijst toevoegen] | [{{SERVER}}{{localurl:{{NAMESPACE}}:{{subst:PAGENAME}}|action=history}} Geschiedenis van dagpagina bekijken] </span> | [[{{NAMESPACE}}:{{subst:PAGENAME}}|Alleen dagpagina bekijken]]</includeonly>\n"
  inhoud = inhoud + "<!--\nInstructie bij het passeren van middernacht: Wacht totdat de bot een nieuwe pagina heeft aangemaakt (dit gebeurt als het goed is even over twaalven.)\nZie verder op [[WP:TV]]-->\n"
  inhoud = inhoud + "=== Toegevoegd " + now.strftime("%d/%m") + ": Deel 1 ===\n* ...\n\n"
  
  P = wikipedia.Page(wikipedia.getSite(u'nl'), pagename)
  if not P.exists():          # als 'ie bestaat doe ik lekker niks ;)
    P.put(inhoud)
    
  mainpage = wikipedia.Page(wikipedia.getSite(u'nl'), "Wikipedia:Te verwijderen afbeeldingen")
  mpInhoud = mainpage.get()
  
  if not P in mainpage.templatePages():
    mpInhoud = "".join(mpInhoud.split("<!-- {{"+pagename+"}} -->\n"))
    delen = mpInhoud.split("<!-- HIERVOOR -->")
    mpInhoud = delen[0] + "{{"+pagename+"}}\n<!-- HIERVOOR -->"+ delen[1]
    

  #nu nog de pagina voor over een week toevoegen
  dan = now + datetime.timedelta(days=8)
  intwoweeks = dan + datetime.timedelta(weeks=2)
  
  pagename = dan.strftime("Wikipedia:Te verwijderen afbeeldingen/Toegevoegd %Y%m%d")
  
  inhoud = "<noinclude>{{VerwijderNav|Afbeeldingen}}</noinclude>\n"
  inhoud = inhoud + "== Toegevoegd " + dan.strftime("%d/%m") + " te verwijderen vanaf "+ intwoweeks.strftime("%d/%m") + " ==\n"
  inhoud = inhoud + "<includeonly><span class='plainlinks'>[{{SERVER}}{{localurl:{{NAMESPACE}}:{{subst:PAGENAME}}|action=watch}} Dagpagina aan volglijst toevoegen] | [{{SERVER}}{{localurl:{{NAMESPACE}}:{{subst:PAGENAME}}|action=history}} Geschiedenis van dagpagina bekijken] </span>| [[{{NAMESPACE}}:{{subst:PAGENAME}}|Alleen dagpagina bekijken]]</includeonly>\n"
  inhoud = inhoud + "<!--\nInstructie bij het passeren van middernacht: Wacht totdat de bot een nieuwe pagina heeft aangemaakt (dit gebeurt als het goed is even over twaalven.)\nZie verder op [[WP:TV]].-->\n"
  inhoud = inhoud + "=== Toegevoegd " + dan.strftime("%d/%m") + ": Deel 1 ===\n* ...\n"
 
  P = wikipedia.Page(wikipedia.getSite(u'nl'), pagename)
  if not P.exists():          # als 'ie bestaat doe ik lekker niks ;)
    P.put(inhoud)
  
  delen = mpInhoud.split("<!-- EINDE QUEUE -->")
  mpInhoud = delen[0] + "<!-- {{"+pagename+"}} -->\n<!-- EINDE QUEUE -->" + delen[1]
  
  mainpage.put(mpInhoud)



#else:
  #print time.strftime("--not 00:00 yet. current time: %H:%M:%S") 
