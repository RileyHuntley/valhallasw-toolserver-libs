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

import monkeypatch
import toolserver
import wikipedia
import catlib
import itertools

#############################-[ catlib.Category ]-##############################
@monkeypatch.bak
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

monkeypatch.patch(patches, globals(), locals())
                    
            
        
        