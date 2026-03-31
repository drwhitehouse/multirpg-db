#!/usr/bin/env python3
""" multirpg database writer """

import sys
import re
import urllib.request
import urllib.error
import datetime
import psycopg2
from psycopg2 import sql

MY_DATABASE = "multirpg"
MY_DB_USER = "crab"
TABLE = "players"
CS = f"dbname={MY_DATABASE} user={MY_DB_USER}"
conn = psycopg2.connect(CS)
conn.autocommit = True

MYPLAYERS = ["HRH_H_Crab"]
STATSURL = "http://multirpg.net/rawplayers3.php"

def read_data(mystatsurl):
    """ read some data """
    try:
        with urllib.request.urlopen(mystatsurl) as response:
            data = response.read()
    except urllib.error.HTTPError as error:
        print(error.__dict__)
        sys.exit()
    except urllib.error.URLError as error:
        print(error.__dict__)
        sys.exit()
    # Convert bytes to string
    data=str(data, 'UTF8')
    # Fix the classes
    data = re.sub(r'\{[^{}]*\}', lambda x: x.group(0).replace(' ','_'), data)
    data=data.split('\n')
    return data

def get_myplayer(thisdata, thisplayer):
    """ parse some data """
    for string in thisdata:
        playerstats = dict(zip(string.split()[::2], string.split()[1::2]))
        if playerstats['char'] == thisplayer:
            return playerstats
    return None

def sanitise_data(thisnow, thesestats):
    """ strip out stuff we don't want """
    cleanstats = {}
    cleanstats.update({"date":thisnow})
    cleanstats.update({"char":thesestats["char"]})
    cleanstats.update({"rank":int(thesestats["rank"])})
    cleanstats.update({"level":int(thesestats["level"])})
    cleanstats.update({"sum":int(thesestats["sum"])})
    cleanstats.update({"gold":int(thesestats["gold"])})
    cleanstats.update({"bank":int(thesestats["bank"])})
    cleanstats.update({"bwon":int(thesestats["bwon"])})
    cleanstats.update({"blost":int(thesestats["blost"])})
    cleanstats.update({"ttl":str(datetime.timedelta(seconds=int(thesestats["ttl"])))})
    return cleanstats

def write_data(thesestats):
    """ write to the database """
    columns = [k for (k, v) in thesestats.items()]
    cur = conn.cursor()
    query = sql.SQL("insert into {} ({}) values ({})").format(
            sql.Identifier(TABLE),
            sql.SQL(", ").join(map(sql.Identifier, columns)),
            sql.SQL(", ").join(map(sql.Placeholder, columns)),
    )
    cur.execute(query, thesestats)
    cur.close()

def main():
    ''' start here '''
    mydata = read_data(STATSURL)
    now = datetime.datetime.now(datetime.UTC)
    for myplayer in MYPLAYERS:
        mystats = get_myplayer(mydata, myplayer)
        mystats = sanitise_data(now, mystats)
        if mystats['level'] < 101:
            write_data(mystats)

if __name__ == "__main__":
    main()
