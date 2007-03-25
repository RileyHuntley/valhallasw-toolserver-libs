#! /home/valhallasw/bin/python
# $Id$

import cgi
import cgitb; cgitb.enable()

import sys, os
sys.path.append('/home/valhallasw/libs/python') #viewable through http://tools.wikimedia.de/~valhallasw/libs/python
import querier, sqlfunctions, cgifunctions


print """Content-type: text/html\n\n
<html>
<head>
<style type="text/css">
#txt {
  border:none;
  text-align:center;
  font-family:verdana;
  font-size:50pt;
  font-weight:bold;
  border-right-color:#FFFFFF
}
body
{
font-family: Georgia, "Times New Roman", Times, serif;
font-size: 10pt;
margin: 0;
}
a:hover
{
  color: white;
  background-color: blue;
}
 
</style>

<title>Moderatoren van Wikipedia-nl</title>

<script type="text/javascript">
<!--

var mins
var secs;

function cd() {
 	mins = 1 * m("10"); // change minutes here
 	secs = 0 + s(":01"); // change seconds here (always add an additional second to your total)
 	redo();
}

function m(obj) {
 	for(var i = 0; i < obj.length; i++) {
  		if(obj.substring(i, i + 1) == ":")
  		break;
 	}
 	return(obj.substring(0, i));
}

function s(obj) {
 	for(var i = 0; i < obj.length; i++) {
  		if(obj.substring(i, i + 1) == ":")
  		break;
 	}
 	return(obj.substring(i + 1, obj.length));
}

function dis(mins,secs) {
 	var disp;
 	if(mins <= 9) {
  		disp = " 0";
 	} else {
  		disp = " ";
 	}
 	disp += mins + ":";
 	if(secs <= 9) {
  		disp += "0" + secs;
 	} else {
  		disp += secs;
 	}
 	return(disp);
}

function redo() {
 	if(count==81)return;
   secs--;
 	if(secs == -1) {
  		secs = 59;
  		mins--;
 	}
 	document.cd.disp.value = dis(mins,secs); // setup additional displays here.
 	if((mins == 0) && (secs == 0)) {
  		window.alert("Je tijd is om! Eens zien hoe je het gedaan hebt."); 
  		showMissed(); 
 	} else {
 		cd = setTimeout("redo()",1000);
 	}
}

function init() {
  cd();
}
window.onload = init;

var count=0;
var found=new Array();
var states=new Array("""

Q = querier.querier()
n = u""
for nick in Q.do("select user_name from nlwiki_p.user right join nlwiki_p.user_groups on user_id=ug_user where ug_group = 'sysop'"):
	n += u'"'+nick['user_name'].decode('utf-8')+'",'
n = n.rstrip(",")
print n.encode('utf-8');
print """);
function checkStates(fld){
if(fld.value.length>1){
for(var i=0;i<states.length;i++){
   if(fld.value.toLowerCase()==states[i].toLowerCase()){
    found[found.length]=states[i];
    found.sort();
    states.splice(i,1);
    fld.value="";
    count++;
    var msg="";
    for(var x=0;x<found.length;x++){
      msg+=found[x]+", ";
      if((x+1)%5==0)msg+="<BR>";
    }
    document.getElementById("found").innerHTML=msg;
    var remainmsg=" moderatoren blijven over";
    if(count==80)remainmsg=" moderator blijft over";
    document.getElementById("remain").innerHTML="<B>"+(81-count)+remainmsg+"</B>";
    if(count==81){
      		window.alert("Het is je gelukt!"); 
    }
  }
  }
  }else{
  if(fld.value==" ")fld.value="";
  }
 }
function showMissed(){
    var msg="";
    msg+='<BR><FONT COLOR=RED><B>Je bent vergeten:</B>';
    for(var x=0;x<states.length;x++){
      msg+=states[x]+", ";
      if((x+1)%5==0)msg+="<BR>";
    }
    msg+='</FONT><br>Bedankt voor het spelen!';
    document.getElementById("header").innerHTML=msg;
 }
//-->
</script>
</head>
<body><center>
<br><h1>Moderatoren van Wikipedia-nl</h1><br>
<DIV id="header">
<p>Je hebt 10 minuten om je zoveel mogelijk van de moderatoren van de Nederlandstalige Wikipedia te herinneren.<br>

Na 10 minuten zullen de correcte antwoorden verschijnen zodat je kunt zien welke je vergeten bent.</p>
</DIV>
<form name="cd">
<input id="txt" readonly="true" type="text" value="01:00" border="0" name="disp">
</form>
<center>
<table>
<tr><td align="center">
<DIV id="remain"><B>81 moderatoren blijven over</b></DIV>
<input type="text" onKeyUp="checkStates(this);" name="input"><br>
</td></tr>
<tr>
<td align="center">

<B>Tot dusver genoemd:</b>
<DIV id="found">Niets</DIV>
</td>
</tr></table>


</center>

<address style="position:absolute; bottom: 5px; left: 5px">Original version by <a href="http://nl.wikipedia.org/wiki/Gebruiker:troefkaart">troefkaart</a>; Dynamic (toolserver) version by <a href="http://nl.wikipedia.org/wiki/Gebruiker:valhallasw">valhallasw</a></address>
</body>

</html>"""

