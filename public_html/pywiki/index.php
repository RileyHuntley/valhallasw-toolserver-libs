<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/2002/REC-xhtml1-20020801/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
  <head>
    <title>PyWikipediaBot Nightlies</title>
    <link rel="stylesheet" href="/~valhallasw/main.css" />
  </head>
  <body>
    <h1>PyWikipediaBot Nightlies</h1>
    <h2>Nightly downloads</h2>
    <p>The nightlies are generated every night at 20:00 UTC. There are several packages:</p>
    <!-- begin automagically generated section -->
    <?php
      $file = fopen('packages', 'r') or die ('Could not open package list. View <a href="log">logs</a> or <a href="package">packages</a>');
      $gendate = fgets($file);
      $package = rtrim(fgets($file));
      while (!feof($file)) {
        print '<h3>'.$package.'</h3><div style="margin-left: 3em; margin-right: 20%;">';
        print '<pre>';
        include('log/'.$package.'/latest.log');
        print '</pre>';
        print '<ul><li>The <a href="log/'.$package.'/svn.log">svn update log</a> and latest <a href="log/'.$package.'/latest.log">commit log</a></li>';
      
        print '<li>The compression logs:';
        print '<ul>';
        print '<li><a href="log/'.$package.'/tar.bz2.log">bzip2</a></li>';
        print '<li><a href="log/'.$package.'/tgz.log">gzip2</a></li>';
        print '<li><a href="log/'.$package.'/zip.log">zip</a></li>';
        print '</ul>or alternatively, browse the <a href="log/'.$package.'">'.$package.'log directory</a></li>';
      
        print '<li>The packages:';
        print '<ul>';
        print '<li><a href="package/'.$package.'/'.$package.'-nightly.tar.bz2">'.$package.'-nightly.tar.bz2</a></li>';
        print '<li><a href="package/'.$package.'/'.$package.'-nightly.tgz">'.$package.'-nightly.tgz</a></li>';
        print '<li><a href="package/'.$package.'/'.$package.'-nightly.zip">'.$package.'-nightly.zip</a></li>';
        print '</ul>or alternatively, browse the <a href="log/'.$package.'">'.$package.' package directory</a></li>';
        print '</ul></div>';
        $package = rtrim(fgets($file));
      }
    ?><!-- end automagically created stuff -->
    <h2>FAQ</h2>
    <ul>
      <li>
        Q: What are those nasty CVS/ directories for?<br/>
        A: I am too lazy to no pack them and it's useable for people too lazy to do a normal checkout. This allows people to use - for example - <a href="http://www.tortoisecvs.org">TortoiseCVS</a> without filling any scary forms. And it only takes 10 kB anyway.
      </li>
      <li>
        Q: How can I use the framework?<br/>
        A: Read the <a href="http://meta.wikimedia.org/wiki/Using_the_python_wikipediabot">manual</a>
      </li>
      <li>
        Q: OMG BUG!!!!!!1111oneoneone<br/>
        A: Report them at the <a href="http://sourceforge.net/tracker/?atid=603138&amp;group_id=93107&amp;func=browse">bug tracker</a>
      </li>
      <li>
        Q: I've got a support or feature request, or a patch<br/>
        A: <a href="http://sourceforge.net/tracker/?atid=603139&amp;group_id=93107&amp;func=browse">Support requests</a>, <a href="http://sourceforge.net/tracker/?atid=603141&amp;group_id=93107&amp;func=browse">Feature requests</a>, <a href="http://sourceforge.net/tracker/?atid=603140&amp;group_id=93107&amp;func=browse">Patches</a>. Or join us on irc: <a href="irc://irc.freenode.net/pywikipediabot">#pywikipediabot on freenode</a>.
      </li>
      <li>
        Q: I want to stay updated<br/>
        A: Subscribe to the <a href="http://lists.wikimedia.org/mailmain/pywikipedia-l">mailing list</a>, join us on <a           href="irc://irc.freenode.net/pywikipediabot">IRC</a>.
      </li>
    </ul>
    <div>
      <div style="float:right; margin-top: 3px;">
       <a href="http://validator.w3.org/check?uri=referer" style="border-bottom: none;">
         <img src="http://www.w3.org/Icons/valid-xhtml10-blue" alt="Valid XHTML 1.0 Strict" height="31" width="88" />
       </a>
      </div>
      <p class="footer">
        Latest pywikipedia nightly was generated at: <? echo $gendate; ?><br/>Web site revision: $Id$
      </p>
    </div>
  </body>
</html>