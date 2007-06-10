"""
Monkey patch script to use the toolserver for category-funkyness
"""
# 
# (C) Merlijn 'valhallasw' van Deen, 2007
#
# Distributed under the terms of the MIT license.
#
__version__ = '$Id$'
#

import toolserver
import wikipedia
import catlib
import itertools

_bfunc = {}
def _backup(f):

    """ Decorator for backup functions. The backup functions are stored in the _bfunc dict
    """
    def new_f(*args, **kwds):
        if kwds.pop('original', False ):
            return _bfunc[f.func_name](*args, **kwds)
        else:
            return f(*args, **kwds)
    new_f.func_name = f.func_name
    return new_f

#############################-[ catlib.Category ]-##############################
@_backup
def _catlib_Category__parseCategory(self, recurse = False, purge = False, startFrom = None):
    if not startFrom:
        startFrom = 0
    ns = self.site().category_namespaces()
    catsdone = []
    catstodo = [(self, recurse)]
    
    # Get subcats and articles
    for (cat, recurselevel) in catstodo:
        if type(recurselevel) == type(1):
            newrecurselevel = recurselevel - 1
        else:
            newrecurselevel = recurselevel
        catsdone.append(cat)
        
        wikipedia.output('Getting [[%s]] from %s...' % (cat.title(), cat.site().dbName()))
        for page in toolserver.Generators.getCategoryMembers(cat, startFrom):
            if type(page) == catlib.Category:
                if recurselevel and page not in catsdone:
                    catstodo.append((page, newrecurselevel))
                yield catlib.SUBCATEGORY, page.title()
            else:
                yield catlib.ARTICLE, page.title()
    # Get supercats
    for supercat in toolserver.Generators.getCategories(self):
        yield catlib.SUPERCATEGORY, supercat.title()
        
patches =   {
                "catlib.Category._parseCategory": "_catlib_Category__parseCategory"
            }

for p in patches:
    exec("if %(x)s.__name__ == '%(xs)s':\n  _bfunc['%(y)s'] = %(x)s\n  print '[b] Patching %(x)s...'\nelse:\n  print '[ ] Patching %(x)s...'"
        % {'x': p, 'xs': p.split('.')[-1], 'y': patches[p]}
        , globals(), locals())
    exec("%s = %s"           % (p, patches[p]), globals(), locals())
                    
            
        
        