#!/usr/bin/env python3
""" multirpg database reader """

import sys
import psycopg2
from psycopg2 import sql
import numpy
import matplotlib.pyplot as plt

MY_DATABASE = "multirpg"
MY_DB_USER = "crab"
TABLE = "players"
CS = f"dbname={MY_DATABASE} user={MY_DB_USER}"
QUERY = "SELECT date, rank FROM players WHERE char = 'testcrab'"

def plot_graph(x, y):
    """ plot the graph """
    fig, ax = plt.subplots()
    plt.xticks(rotation=90)
    ax.plot(x, y)
    ax.invert_yaxis()
    fig.tight_layout()
    plt.savefig('output/test.png')
    return

def main():
    ''' start here '''
    x_axis = []
    y_axis = []
    print("Connecting to database...")
    try:
        conn = psycopg2.connect(CS)
        cursor = conn.cursor()
        cursor.execute(QUERY)
        records = cursor.fetchall()
    except (Exception, psycopg2.Error) as error:
        print("Error while fetching data from PostgreSQL", error)
    for row in records:
        dt = row[0].replace(tzinfo=None) # We have to do this because numpy is deprecating timezone aware datetimes.
        x_axis.append(dt)
        y_axis.append(row[1])
    my_x_array = numpy.array(x_axis, dtype='datetime64[s]')
    my_y_array = numpy.array(y_axis)
    plot_graph(my_x_array, my_y_array)

if __name__ == "__main__":
    main()
