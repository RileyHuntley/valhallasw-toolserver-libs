""" Monkey patch function """

# 
# (C) Merlijn 'valhallasw' van Deen, 2007
#
# Distributed under the terms of the MIT license.
#
__version__ = '$Id$'
#

_bfunc = {}
def bak(f):
    """ Decorator for backup functions. The backup functions are stored in the _bfunc dict
    """
    def new_f(*args, **kwds):
        if kwds.pop('original', False ):
            return _bfunc[f.func_name](*args, **kwds)
        else:
            return f(*args, **kwds)
    new_f.func_name = f.func_name
    return new_f

def patch(patches, glob, loc):
    for p in patches:
        exec("if %(x)s.__name__ == '%(xs)s':\n  monkeypatch._bfunc['%(y)s'] = %(x)s\n  print '[b] Patching %(x)s...'\nelse:\n  print '[ ] Patching %(x)s...'" % {'x': p, 'xs': p.split('.')[-1], 'y': patches[p]} , glob, loc)
        exec("%s = %s"           % (p, patches[p]), glob, loc)
