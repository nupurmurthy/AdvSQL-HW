import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


engine = create_engine("sqlite:///hawaii.sqlite")


Base = automap_base()

Base.prepare(engine, reflect=True)

climate = Base.classes.climate


app = Flask(__name__)



@app.route("/")
def Homepage():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs/name"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    date = session.query(measurement.date).order_by(measurement.date.desc()).first()
    year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    precipation = session.query(measurement.date, measurement.prcp).filter(measurement.date > last_year).order_by(measurement.date).all()

    total = []
    for result in preccipitation:
        row = {}
        row["date"] = precipitation[0]
        row["prcp"] =precipitation[1]
        total.append(row)

    return jsonify(total)

@app.route("/api/v1.0/stations")
def stations():
    stations_q = session.query(station.name, station.station)
    stations_read = pd.read_sql(stations_q.statement, stations_q.session.bind)
    return jsonify(stations.to_dict())

@app.route("/api/v1.0/tobs")
def temperature(age):

    date = session.query(measurement.date).order_by(measurement.date.desc()).first()
    year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    temp = session.query(measurement.date, measurement.tobs).filter(measurement.date > last_year).order_by(measurement.date).all()

    total = []
    for result in temperature:
        row = {}
        row["date"] = temp[0]
        row["tobs"] = temp[1]
        total.append(row)

    return jsonify(total)

@app.route("/api/v1.0/<start>")
def start_one(start):

    start= dt.datetime.strptime(start, '%Y-%m-%d')
    last = dt.timedelta(days=365)
    start = start-last
    end =  dt.date(2017, 8, 23)
    data = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).filter(measurement.date >= start).filter(measurement.date <= end).all()
    trip = list(np.ravel(data))
    return jsonify(trip)

@app.route("/api/v1.0/<start>/<end>")
def start_two(start,end):

    start= dt.datetime.strptime(start, '%Y-%m-%d')
    end= dt.datetime.strptime(end,'%Y-%m-%d')
    last = dt.timedelta(days=365)
    start_one = start-last
    end_one = end-last
    data = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).filter(measurement.date >= start).filter(measurement.date <= end).all()
    trip = list(np.ravel(data))
    return jsonify(trip)

if __name__ == '__main__':
    app.run(debug=True)
