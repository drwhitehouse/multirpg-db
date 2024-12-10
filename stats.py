#!/usr/bin/env python3
""" multirpg database sampler """

import sys
import re
import urllib.request
import urllib.error

#MYPLAYERS=["HRH_H_Crab","testcrab","macrocrab"]
MYPLAYERS=["HRH_H_Crab"]
STATSURL="http://multirpg.net/rawplayers3.php"

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

def sanitise_data(thesestats):
    """ strip out stuff we don't want """
    cleanstats = {}
    cleanstats.update({"char":thesestats["char"]})
    cleanstats.update({"rank":thesestats["rank"]})
    cleanstats.update({"level":thesestats["level"]})
    cleanstats.update({"sum":thesestats["sum"]})
    cleanstats.update({"ttl":thesestats["ttl"]})
    cleanstats.update({"gold":thesestats["gold"]})
    cleanstats.update({"bank":thesestats["bank"]})
    return cleanstats

# Start here

mydata = read_data(STATSURL)

for myplayer in MYPLAYERS:
    mystats = get_myplayer(mydata, myplayer)
    mystats = sanitise_data(mystats)
    print(mystats)
    print()
