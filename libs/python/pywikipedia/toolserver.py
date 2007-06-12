import querier
import time, datetime
import wikipedia, catlib

__Q = querier.querier()

class NoDatabase(wikipedia.Error):
    """No such database"""

def query(*args, **kwargs):
    return __Q.do(*args, **kwargs)

class _tools:
    def replag(self, database, format = "%(days)id %(hours)ih %(minutes)im %(seconds)is"):
        """ Returns replication lag of database in a tuple
            returns (days, hours, seconds)
        """
        timestamp = query(""" SELECT rev_timestamp
                              FROM %s.revision
                              ORDER BY rev_id DESC
                              LIMIT 1 """
                              % (database)
                         )[0]['rev_timestamp']
        behind = datetime.datetime.utcnow() - datetime.datetime(*time.strptime(timestamp, "%Y%m%d%H%M%S")[0:6])
        return format % {'days': behind.days, 'hours': behind.seconds/3600, 'minutes': (behind.seconds/60)%60, 'seconds': behind.seconds%60}
    
    def dbName(self, site):
        """ Returns the database name of the given site """
        sites = query(""" SELECT dbname
                          FROM toolserver.wiki
                          WHERE domain=%s """
                          , site.hostname()
                     )
        if len(sites) == 0:
            raise NoDatabase(u'No database found for hostname %s of site %s' % (site.hostname(), site.__repr__()))
        return sites[0]['dbname']

class _tests:
    def isIncludedIn(self, page, inpage):
        q = """ SELECT 1
                FROM %s.templatelinks
                WHERE tl_from=(
                    SELECT page_id
                    FROM %s.page
                    WHERE page_title=%%s AND page_namespace=%%s
                ) AND tl_title=%%s AND tl_namespace=%%s """ % ((page.site().dbName(),)*2)
        res = query(q, (  page.titleWithoutNamespace(True),   page.namespace(),
                        inpage.titleWithoutNamespace(True), inpage.namespace()))
        return (len(res) > 0)

    def isRedirectTo(self, frompage, topage):
        q = """ SELECT 1
                FROM %s.redirect
                WHERE rd_from=(
                    SELECT page_id
                    FROM %s.page
                    WHERE page_title=%%s AND page_namespace=%%s
                ) AND rd_title=%%s AND rd_namespace=%%s
                LIMIT 1 """ % ((frompage.site().dbName(),)*2)  #what do interlanguage redirects look like?
        res = query(q, (frompage.titleWithoutNamespace(True), frompage.namespace(),
                          topage.titleWithoutNamespace(True),   topage.namespace()) )
        return (len(res) > 0)
    
    def exists(self, page):
        q = """ SELECT 1
                FROM %s.page
                WHERE page_title=%%s AND page_namespace=%%s
                LIMIT 1 """ % page.site().dbName()
        res = query(q, (page.titleWithoutNamespace(True), page.namespace()))
        return (len(res) > 0)

class _generators:
    
    def _generate(self, q, min, step, params, allowNone = False):
        more = True
        q += " LIMIT %s, %s"
        
        if (type(params) != type((min, step))):
            params = (params, )
         
        while more:
            if wikipedia.verbose:
                print q % (params + (min, step))
            data = query(q, (params + (min, step)))
            if len(data) < step:
                more = False
            min += step

            for row in data:
                if (allowNone or None not in row.values()):
                    yield row
    
    ########################### FORWARD  GENERATORS (page_id -> otherpage_namespace/otherpage_title)
    def getPagelinks(self, page, min=0, step=50, sort=""):
        q = """ SELECT pl_namespace, pl_title
                FROM %s.pagelinks
                WHERE pl_from=(
                    SELECT page_id
                    FROM %s.page
                    WHERE page_title=%%s AND page_namespace=%%s) """ % ((page.site().dbName(), )*2)
        q += sort           
        for row in self._generate(q, min, step, (page.titleWithoutNamespace(True), page.namespace())):
            yield wikipedia.Page(page.site(), row['pl_title'].decode('utf-8'), page.site(), row['pl_namespace'])
 
    def getTemplatelinks(self, page, min=0, step=50, sort=""):
        q = """ SELECT tl_namespace, tl_title
                FROM %s.templatelinks
                WHERE tl_from=(
                    SELECT page_id
                    FROM %s.page
                    WHERE page_title=%%s AND page_namespace=%%s) """ % ((page.site().dbName(), )*2)
        q += sort
        for row in self._generate(q, min, step, (page.titleWithoutNamespace(True), page.namespace())):
            yield wikipedia.Page(page.site(), row['tl_title'].decode('utf-8'), page.site(), row['tl_namespace'])   
                     
    def getLanglinks(self, page, min=0, step=50, sort=""):
        q = """ SELECT ll_lang, ll_title
                FROM %s.langlinks
                WHERE ll_from=(
                    SELECT page_id
                    FROM %s.page
                    WHERE page_title=%%s AND page_namespace=%%s) """ % ((page.site().dbName(), )*2)
        q += sort
        for row in self._generate(q, min, step, (page.titleWithoutNamespace(True), page.namespace())):
            yield wikipedia.Page(wikipedia.Site(row['ll_lang']), row['ll_title'].decode('utf-8'), page.site())

    def getCategorylinks(self, page, min=0, step=50, sort=""):
        q = """ SELECT cl_to, cl_sortkey
                FROM %s.categorylinks
                WHERE cl_from=(
                    SELECT page_id
                    FROM %s.page
                    WHERE page_title=%%s AND page_namespace=%%s) """ % ((page.site().dbName(), )*2)
        q += sort
        for row in self._generate(q, min, step, (page.titleWithoutNamespace(True), page.namespace())):
            yield catlib.Category(page.site(), page.site().category_namespace() + ':' + row['cl_to'].decode('utf-8'), page.site(), row['cl_sortkey'].decode('utf-8'))

    def getImagelinks(self, page, min=0, step=50, sort=""):    
        q = """ SELECT il_to
                FROM %s.imagelinks
                WHERE il_from=(
                    SELECT page_id
                    FROM %s.page
                    WHERE page_title=%%s AND page_namespace=%%s) """ % ((page.site().dbName(), )*2)
        q += sort
        for row in self._generate(q, min, step, (page.titleWithoutNamespace(True), page.namespace())):
            yield wikipedia.ImagePage(page.site(), page.site().image_namespace() + ":" + row['il_to'].decode('utf-8'), page.site()) 
    
    def getRedirect(self, page, min=0, step=50, sort=""):
        q = """ SELECT rd_namespace, rd_title
                FROM %s.redirect
                WHERE rd_from=(
                    SELECT page_id
                    FROM %s.page
                    WHERE page_title=%%s AND page_namespace=%%s) """ % ((page.site().dbName(), )*2)
        q += sort
        for row in self._generate(q, min, step, (page.titleWithoutNamespace(True), page.namespace())):
            yield wikipedia.Page(page.site(), row['rd_title'].decode('utf-8'), page.site(), row['rd_namespace'])   
    
    def getRevision(self, page, min=0, step=50, format='%Y%m%d%H%M%S', sort="ORDER BY rev_id DESC"):
        q = """ SELECT rev_id, rev_comment, rev_user_text, rev_timestamp
                FROM %s.revision
                WHERE rev_page=(
                    SELECT page_id
                    FROM %s.page
                    WHERE page_title=%%s AND page_namespace=%%s) """ % ((page.site().dbName(), )*2)
        q += sort
        for row in self._generate(q, min, step, (page.titleWithoutNamespace(True), page.namespace())):
            date = time.strftime(format, time.strptime(row['rev_timestamp'], "%Y%m%d%H%M%S"))
            yield { 'revision'  :   row['rev_id'],
                    'comment'   :   row['rev_comment'].tostring().decode('utf-8'),
                    'user'      :   row['rev_user_text'].decode('utf-8'),
                    'date'      :   date
                  }
    
    ########################### BACKWARD GENERATORS (page_ns/title -> otherpage_id)
    def getReferences(self, page, min=0, step=50):
        q = """ SELECT page_namespace, page_title
                FROM %s.pagelinks
                LEFT JOIN %s.page
                ON page_id = pl_from
                WHERE pl_title=%%s AND pl_namespace=%%s """ % ((page.site().dbName(), )*2)
    
        for row in self._generate(q, min, step, (page.titleWithoutNamespace(True), page.namespace())):
            yield wikipedia.Page(page.site(), row['page_title'].decode('utf-8'), page.site(), row['page_namespace'])

    def getInclusions(self, page, min=0, step=50):
        q = """ SELECT page_namespace, page_title
                    FROM %s.templatelinks
                    LEFT JOIN %s.page
                    ON page_id = tl_from
                    WHERE tl_title=%%s and tl_namespace=%%s 
                    LIMIT %%s, %%s""" % ((page.site().dbName(),)*2)
        
        for row in self._generate(q, min, step, (page.titleWithoutNamespace(True), page.namespace())):
            yield wikipedia.Page(page.site(), row['page_title'].decode('utf-8'), page.site(), row['page_namespace'])
    
    def getCategoryMembers(self, page, min=0, step=50):
        if (page.namespace() != 14):
            raise wikipedia.Error("%s is not in category namespace '%s'" % (page.__repr__(), page.site().category_namespace()))
            
        q = """ SELECT page_namespace, page_title
                FROM %s.categorylinks
                LEFT JOIN %s.page
                ON page_id = cl_from
                WHERE cl_to=%%s """ % ((page.site().dbName(), )*2)
        
        for row in self._generate(q, min, step, page.titleWithoutNamespace(True)):
            if (row['page_namespace'] == 14):
                yield catlib.Category(page.site(), page.site().category_namespace() + ':' + row['page_title'].decode('utf-8'), page.site())
            else:
                yield wikipedia.Page(page.site(), row['page_title'].decode('utf-8'), page.site(), row['page_namespace'])

                    

Tools = _tools()
Tests = _tests()
Generators = _generators()
