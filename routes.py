#!/usr/bin/env python

from flask import Flask, request, jsonify
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ufosightings.sqlite3'


class Sighting(db.Model):
    __tablename__ = 'sightings'
    id = db.Column(db.Integer, primary_key=True)
    sighted_at = db.Column(db.Integer)
    reported_at = db.Column(db.Integer)
    location = db.Column(db.String(100))
    shape = db.Column(db.String(10))
    duration = db.Column(db.String(10))
    description = db.Column(db.Text)
    lat = db.Column(db.Float(6))
    lng = db.Column(db.Float(6))

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


def add_trig_functions(dbapi_connection, connection_record):
    """
    Defines missing trigonomic functions iplemented in Python
    """
    from math import sin, cos, acos, pi
    dbapi_connection.create_function("acos", 1, acos)
    dbapi_connection.create_function("cos", 1, lambda a: cos(a * pi / 180.))
    dbapi_connection.create_function("sin", 1, lambda a: sin(a * pi / 180.))
    # instead calling many trigonometric funcions implement just one distance:
    dbapi_connection.create_function("distance", 4, lambda lng0, lat0, lng, lat:
        3959 * acos(
            cos(lat0 * pi / 180.) * cos(lat * pi / 180.) * cos((lng - lng0) * pi / 180.)
            + sin(lat0 * pi / 180.) * sin(lat * pi / 180.)
        ) )


def load_sqlite_extension(dbapi_connection, connection_record):
    """
    Loads extension implementing trigonomical funcions
    NB! Works only if your rebuild sqlite3 supprt.
    enable_load_extension is disabled by default.
    """
    dbapi_connection.enable_load_extension(True)
    dbapi_connection.load_extension("./sql_trig.so")


@app.route('/sightings/', methods=['GET'])
def sightings():
    if request.method == 'GET':
        lim = request.args.get('limit', 10)
        off = request.args.get('offset', 0)

        radius = request.args.get('radius', 10)
        location = request.args.get('location', ',')
        lat, lng = location.split(',')

        if lat and lng and radius:
            from sqlalchemy import event
            # Define Python trigonomical functions:
            event.listen(db.engine, 'connect', add_trig_functions)
            # Load trigonomical function extension:
            ##event.listen(db.engine, 'connect', load_sqlite_extension)

            query = """
            SELECT id, location, distance( %(longitude)s, %(latitude)s, lng, lat) AS distance
            FROM sightings
            WHERE distance < %(radius)s
            ORDER BY distance LIMIT %(limit)s
            """ % {"latitude": lat, "longitude": lng, "radius": radius, "limit": lim}

            results = Sighting.query.from_statement(query).all()

        else:
            results = Sighting.query.limit(lim).offset(off).all()

        return jsonify(items=[r.to_dict() for r in results])


@app.route('/sightings/<int:sighting_id>', methods=['GET'])
def sighting(sighting_id):
    if request.method == 'GET':
        result = Sighting.query.filter_by(id=sighting_id).first()
        return jsonify(items=result.to_dict())


if __name__ == '__main__':
    app.run(debug=True, port=5555)
