# multirpg-db

- create the user and database:
- # su - postgres
- $ createuser --pwprompt mypguser
- $ createdb -O mypguser multirpg
- create the table (as mypguser):
- psql multirpg
- multirpg=> create table players (id serial PRIMARY KEY, date timestamptz, char text, rank integer, level integer, sum integer, gold integer, bank integer, bwon integer, blost integer, ttl text);
- create the index:
- multirpg=> create index date_index ON players (date);
