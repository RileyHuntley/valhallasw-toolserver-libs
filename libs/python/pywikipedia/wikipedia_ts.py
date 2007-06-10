"""
Monkey patch script to use the toolserver for wikipedia-funkyness
"""
# 
# (C) Merlijn 'valhallasw' van Deen, 2007
#
# Distributed under the terms of the MIT license.
#
__version__ = '$Id$'
#
import monkeypatch
import toolserver
import wikipedia
import itertools
import catlib_ts
import warnings

#_bfunc = {}
#def _backup(f):
#    """ Decorator for backup functions. The backup functions are stored in the _bfunc dict
#    """
#    def new_f(*args, **kwds):
#        if kwds.pop('original', False ):
#            return _bfunc[f.func_name](*args, **kwds)
#        else:
#            return f(*args, **kwds)
#    new_f.func_name = f.func_name
#    return new_f

##############################-[ wikipedia.Site ]-##############################
@monkeypatch.bak
def _wikipedia_Site_dbName(self):
    """ Returns the database name as used on the Toolserver
    """
    return toolserver.Tools.dbName(self)

##############################-[ wikipedia.Page ]-##############################
@monkeypatch.bak
def _wikipedia_Page_getEditPage(self, get_redirect=False, throttle=True, sysop=False, oldid=None, nofollow_redirects=False):
    """ Gets the source of a wiki page through WikiProxy
        TODO: finish (use permalink things in localhost/~daniel/WikiSense/WikiProxy.php
    """
    isWatched = False
    editRestriction = None
    if wikipedia.verbose:
        wikipedia.output(u'Getting page %s' % self.aslink())
    path = 'http://localhost/~daniel/WikiSense/WikiProxy.php'

@monkeypatch.bak
def _wikipedia_Page_permalink(self):
    """ Get the permalink page for this page """
    return "http://%s%s&oldid=%i" % (self.site().hostname(), self.site().get_address(self.title()), self.latestRevision())

@monkeypatch.bak
def _wikipedia_Page_latestRevision(self):
    """ Gets the latest revision from the database """
    if not self._permalink:
        ret = toolserver.query(""" SELECT page_latest
                                   FROM %s.page
                                   WHERE page_title=%%s AND page_namespace=%%s """
                                   % (self.site().dbName())
                                   , (self.titleWithoutNamespace(True), self.namespace())
                              )
        if (len(ret) == 0):
            raise wikipedia.NoPage('No revisions found for page %%s' % self.__repr__())
        else:
            self._permalink = u'%i\n      ' % ret[0]['page_latest']
    return self._permalink

@monkeypatch.bak
def _wikipedia_Page_exists(self):
    #TODO: think about how to fix SectionErrors
    if self.section():
        return _wikipedia_Page_exists(self, original=True)
    else:
        return toolserver.Tests.exists(self)

@monkeypatch.bak
def _wikipedia_Page_isRedirectPage(self):
    """ Returns whether the page is a redirect """
    ret = toolserver.query(""" SELECT page_is_redirect
                               FROM %s.page
                               WHERE page_title=%%s AND page_namespace=%%s """
                               % (self.site().dbName())
                               , (self.titleWithoutNamespace(True), self.namespace())
                          )
    return (len(ret) != 0 and ret[0]['page_is_redirect'] != 0)

@monkeypatch.bak
def _wikipedia_Page_isEmpty(self):
    """
    True if the page has less than 4 characters, except for
    language links and category links, False otherwise.
    Categories from templates are counted!
    Can raise wikipedia.NoPage
    """
    # retrieve page id and page length
    ret = toolserver.query("""SELECT page_id, page_len
                              FROM %s.page
                              WHERE page_title=%%s AND page_namespace=%%s"""
                              % self.site().dbName()
                              , (self.titleWithoutNamespace(True), self.namespace())
                          )
    if (len(ret) == 0):
        raise wikipedia.NoPage('No such page %%s' % self.__repr__())

    page_id = ret[0]['page_id']
    length = ret[0]['page_len']
    # remove length of langlink links
    ret = toolserver.query(""" SELECT COALESCE(SUM(LENGTH(ll_lang) + LENGTH(ll_title) + 5), 0) AS SUM
                               FROM %s.langlinks
                               WHERE ll_from=%%s
                               GROUP BY ll_from """
                               % self.site().dbName()
                               , page_id
                          )
    if (len(ret) > 0):
        length -= ret[0]['sum']

    # remove length of category links
    ret = toolserver.query(""" SELECT COALESCE(SUM(LENGTH(cl_to) + LENGHT(cl_sortkey) + 5), 0) AS SUM
                               FROM %s.categorylinks
                               WHERE cl_from=%%s
                               GROUP BY cl_from """
                               % self.site().dbName()
                               , page_id
                          )
    if (len(ret) > 0):
        length -= ret[0]['sum']

    return (length < 4)

@monkeypatch.bak
def _wikipedia_Page_botMayEdit(self):
    """ retrieve from the database wether {{bots}} or {{nobots}} are on the page
        if nobots is there, return false; if bots is there, run the original
        function. if nothing is there, return true
    """
    botsTemplate = wikipedia.Page(self.site(), 'template:bots')
    nobotsTemplate = wikipedia.Page(self.site(), 'template:nobots')
    if toolserver.Tests.isIncludedIn(botsTemplate, self):
        return _wikipedia_Page_botMayEdit(self, original=True)
    elif toolserver.Tests.isIncludedIn(nobotsTemplate, self):
        return False
    else:
        return True

@monkeypatch.bak
def _wikipedia_Page_getReferences(self, allow_redirect=True, allow_inclusion=True, require_inclusion=False, require_redirect=False):
    refPages = []
    generators = []

    if (allow_inclusion):
        generators.append(toolserver.Generators.getInclusions(self))
    if (not require_inclusion):
        generators.append(toolserver.Generators.getReferences(self))

    for page in itertools.chain(*generators):
        if page in refPages:
            continue
        refPages.append(page)

        is_redirect = toolserver.Tests.isRedirectTo(page, self)
        if (not is_redirect and require_redirect):
            continue

        yield page

        if (is_redirect and allow_redirect):
            if wikipedia.verbose:
                wikipedia.output('Returning links to redirect %s' % p.__repr__())
            for rpage in _wikipedia_Page_getReferences(p, False, allow_inclusion, require_inclusion, require_redirect):
                if rpage in refPages:
                    continue
                refPages.append(rpage)
                yield rpage

#getFileLinks not implemented. As far as I can see it has no use?

@monkeypatch.bak
def _wikipedia_Page_interwiki(self):
    return [page for page in toolserver.Generators.getLanglinks(self)]
    
@monkeypatch.bak
def _wikipedia_Page_categories(self):
    return [cat for cat in toolserver.Generators.getCategorylinks(self)]

@monkeypatch.bak
def _wikipedia_Page_linkedPages(self):
    """ Gives the normal (not-interwiki, non-category) pages the page, 
        or any included templates, links to, as a list of Page objects.
        If you need only the direct links, use original=True. The original
        function will then be used.
    """
    return [page for page in toolserver.Generators.getPagelinks(self)]

@monkeypatch.bak
def _wikipedia_Page_imagelinks(self, followRedirects = False, loose = False):
    """ Returns images used on the page, including images used in templates """
    if followRedirects or loose:
        warnings.warn("followRedirects and loose are not suppored. Use 'original=True'.", DeprecationWarning)
    return [image for image in toolserver.Generators.getImagelinks(self)]

@monkeypatch.bak
def _wikipedia_Page_templates(self):
    """ Returns all used templates (as strings) used in the page. Includes recursive inclusions!
        Use original=True for original usage """
    return [template.title() for template in self.templatePages()]

@monkeypatch.bak
def _wikipedia_Page_templatePages(self):
    """ Returns all used templates (as pages) used in the page. Includes recursive inclusions!
        Use original=True for original usage """
    return [template for template in toolserver.Generators.getTemplatelinks(self)]

@monkeypatch.bak
def _wikipedia_Page_getRedirectTarget(self):
    if not self.exists():
        raise wikipedia.NoPage(self)
    if not self.isRedirectPage():
        raise IsNotRedirectPage(self)
    try:
        return toolserver.Generators.getRedirect(self).next()
    except StopIteration:
        raise IsNotRedirectPage(self)

patches = {
            "wikipedia.Site.dbName"         : "_wikipedia_Site_dbName",  #            "wikipedia.Site.getEditPage"    : "_wikipedia_getEditPage",
            "wikipedia.Page.permalink"      : "_wikipedia_Page_permalink",
            "wikipedia.Page.latestRevision" : "_wikipedia_Page_latestRevision",
            "wikipedia.Page.exists"         : "_wikipedia_Page_exists",
            "wikipedia.Page.isRedirectPage" : "_wikipedia_Page_isRedirectPage",
            "wikipedia.Page.isEmpty"        : "_wikipedia_Page_isEmpty",
            "wikipedia.Page.botMayEdit"     : "_wikipedia_Page_botMayEdit",
            "wikipedia.Page.getReferences"  : "_wikipedia_Page_getReferences",
            "wikipedia.Page.interwiki"      : "_wikipedia_Page_interwiki",
            "wikipedia.Page.categories"     : "_wikipedia_Page_categories",
            "wikipedia.Page.linkedPages"    : "_wikipedia_Page_linkedPages",
            "wikipedia.Page.imagelinks"     : "_wikipedia_Page_imagelinks",
            "wikipedia.Page.templates"      : "_wikipedia_Page_templates",
            "wikipedia.Page.templatePages"  : "_wikipedia_Page_templatePages"            
          }

monkeypatch.patch(patches, globals(), locals())
#for p in patches:
#    exec("if %(x)s.__name__ == '%(xs)s':\n  _bfunc['%(y)s'] = %(x)s\n  print '[b] Patching %(x)s...'\nelse:\n  print '[ ] Patching %(x)s...'"
#        % {'x': p, 'xs': p.split('.')[-1], 'y': patches[p]}
#        , globals(), locals())
#    exec("%s = %s"           % (p, patches[p]), globals(), locals())