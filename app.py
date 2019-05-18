import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

Base = automap_base()

Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station


session = Session(engine)

#################################################
# Flask Setup
#################################################

app = Flask(__name__)

@app.route("/")
def welcome():
    return (
        f"Welcome to my API!!<br/>"
        f"Available Routes:<br/>"
        f"(Note: Most recent available date is 2017-08-23 while the latest is 2010-01-01).<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/temp/start/end"
    )


@app.route("/api/v1.0/precipitation")
def percip():
    lastyear = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    PercipData = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= lastyear).all()
    precipdata = {date: prcp for date, prcp in precipitation}
    return jsonify(precipdata)

@app.route("/api/v1.0/stations")
def stations():
    stationcount = session.query(func.count(Station.station)).all()
    stations = list(np.ravel(stationcount))
    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def temp_monthly():
    lastyear = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    tempobs = session.query(Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= lastyear).all()
        monthtemp = list(np.ravel(tempobs))
        return jsonify(monthtemp)


@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
def tempovtime(start=None, end=None):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    if not end:
        results = session.query(*sel).\
            filter(Measurement.date >= start).all()
        temps = list(np.ravel(results))
        return jsonify(temps)

    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps)


if __name__ == '__main__':
    app.run()
