#!/usr/bin/env python
# $Id$

# Simple script to update the RRD database of nlwiki page 'Wikipedia:De kroeg'
import sys
sys.path.append('/home/valhallasw/libs/python')
import querier, rrd
db = rrd.RRD('kroeg.rrd')
Q = querier.querier()
size = Q.do('select page_len from nlwiki_p.page where page_id=336336')[0]['page_len']
revs = Q.do('select count(*) as c from nlwiki_p.revision where rev_page=336336')[0]['c']
db.update(size,revs)
