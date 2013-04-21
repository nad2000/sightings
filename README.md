# Sightings

This is a modified version of the sample application for "How to Build an API with Python and Flask" on Tech.Pro.

    1. instead of MySQL - sqlite3;
    2. dried out SQLAchemy result serialization;
    3. demostation of custom sqlite3 function creation both with extension library and Pythons;

Download data from [sightings.tsv https://www.dropbox.com/s/aoim0kwg7v30fii/sightings.tsv]

Remove double quotes:
    sed -i 's/"//g' sightings.tsv

Create sqlite3 DB and table:

    $ sqlite3 db/ufosightings.sqlite3

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

-- Import data:
.import /home/ENDACE/rad.cirskis/Downloads/sightings2.tsv sightings
