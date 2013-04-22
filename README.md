# Sightings #

This is a modified version of the sample application for ["How to Build an API
with Python and Flask" on Tech.Pro.
by Lalith
Polepeddi](http://tech.pro/tutorial/1213/how-to-build-an-api-with-python-and-flask)
with following changes:

1. instead of MySQL it uses sqlite3;
2. dried out SQLAchemy result serialization;
3. demonstration of custom sqlite3 function creation both with extension
   library and Pythons.

You would need to follow the original instruction with slight modifications:

### Data preparation ###

Download data from
[sightings.tsv](https://www.dropbox.com/s/aoim0kwg7v30fii/sightings.tsv) and
remove double quotes:

    sed -i 's/"//g' sightings.tsv

### Create sqlite3 DB and the table for storing data ###

Create DB in the same place **routes.py** located:

    $ sqlite3 ufosightings.sqlite3

    CREATE TABLE sightings (
         id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
         sighted_at INTEGER ,
         reported_at INTEGER ,
         location TEXT,
         shape TEXT,
         duration TEXT,
         description TEXT,
         lat REAL,
         lng REAL
    );

### Import data ###

    -- Import data:
    .headers off
    .separator "\t"
    .import <path to the the file with removed '"'>/sightings.tsv sightings


