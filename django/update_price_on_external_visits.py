#!/usr/bin/python
# -*- coding: utf-8 -*-

import MySQLdb as mdb
import sys

con = None

last_valid_shpe_id = 0
last_price = 0

try:

    con = mdb.connect(host='localhost', user='root', 
        passwd='xxx', db='solotodo', port=3305);

    cur = con.cursor()
    cur.execute("SELECT ev.id, ev.date, ev.shn_id, sph.price from cotizador_externalvisit as ev left join cotizador_storeproducthistory as sph on (ev.shn_id = sph.registry_id and ev.date = sph.date) order by ev.shn_id, ev.date")
    
    for idx, row in enumerate(cur.fetchall()):
        if idx % 10000 == 0:
            print idx
        price = row[3]
        if price:
            last_price = price
            last_valid_shpe_id = row[2]
        else:
            if last_valid_shpe_id == row[2]:
                price = last_price
            else:
                price = 0
    
        query = 'UPDATE cotizador_externalvisit SET price=%d WHERE id=%d' % (price, row[0])
        cur.execute(query)
    
except mdb.Error, e:
  
    print "Error %d: %s" % (e.args[0],e.args[1])
    sys.exit(1)
    
finally:    
    if con:
        con.commit()
        cur.close()
        con.close()
