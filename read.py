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
CHAR = "testcrab"
CS = f"dbname={MY_DATABASE} user={MY_DB_USER}"

def connect_db():
    """ connect to the database """
    print("Connecting to database...")
    try:
        conn = psycopg2.connect(CS)
        cursor = conn.cursor()
        query = sql.SQL("SELECT date, rank, sum FROM {} WHERE char = {}").format(
                sql.Identifier(TABLE),
                sql.Literal(CHAR),
        )
        cursor.execute(query)
        records = cursor.fetchall()
        conn.close()
    except (Exception, psycopg2.Error) as error:
        print("Error while fetching data from PostgreSQL", error)
    return records

def plot_graph(time_ax, rank_ax, sum_ax):
    """ plot the graph """
    fig, axs = plt.subplots(2,1)
    axs[0].plot(time_ax, rank_ax)
    axs[0].tick_params('x', labelrotation=45)
    axs[0].invert_yaxis()
    axs[0].set_title('rank')
    axs[1].plot(time_ax, sum_ax)
    axs[1].tick_params('x', labelrotation=45)
    axs[1].set_title('sum')
    fig.tight_layout()
    plt.savefig('output/test.png')
    return

def main():
    ''' start here '''
    my_time = []
    rank = []
    sum = []
    my_records = connect_db()
    for row in my_records:
        my_dt = row[0].replace(tzinfo=None) # We have to do this because numpy is deprecating timezone aware datetimes.
        my_time.append(my_dt)
        rank.append(row[1])
        sum.append(row[2])
    time_array = numpy.array(my_time, dtype='datetime64[s]')
    rank_array = numpy.array(rank)
    sum_array = numpy.array(sum)
    plot_graph(time_array, rank_array, sum_array)

if __name__ == "__main__":
    main()
