# Import the dependencies.
import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Database = automap_base()
Database.prepare(autoload_with = engine)

# reflect the tables
Measurement = Database.classes.measurement
Station = Database.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"Precipitation: /api/v1.0/precipitation<br/>"
        f"Stations: /api/v1.0/stations<br/>"
        f"Tempretures: /api/v1.0/tobs"
        f"Start: /api/v1.0/<start>"
        f"End: /api/v1.0/<start>/<end"
    )
        
@app.route("/api/v1.0/precipitation")
def precipitation():
    
    session = Session(engine)
    start_date = (dt.date(2017,8,23)) - (dt.timedelta(days = 365))
    results = prcp_scores = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= start_date)

    session.close()

    precipitation = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict["Date"] = date
        prcp_dict["Percipitation"] = prcp
        precipitation.append(prcp_dict)

    return jsonify(precipitation)

@app.route("/api/v1.0/stations")
def stations():
    
    session = Session(engine)
    start_date = (dt.date(2017,8,23)) - (dt.timedelta(days = 365))
    results = session.query(Station.station, Station.name, Station.latitude, Station.longitude, Station.elevation).distinct().all()
    
    session.close()

    stations = []
    for station, name, latitude,longitude,elevation in results:
        prcp_dict = {}
        prcp_dict["Station"] = station
        prcp_dict["Name"] = name
        prcp_dict["Latitude"] = latitude
        prcp_dict["Longitude"] = longitude
        prcp_dict["Elevation"] = elevation

        stations.append(prcp_dict)

    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def tempretures():

    session = Session(engine)
    start_date = (dt.date(2017,8,23)) - (dt.timedelta(days = 365))
    results = session.query(Measurement.tobs, Measurement.date).filter(Measurement.date >= start_date).filter(Measurement.station == 'USC00519281')
    
    session.close()

    tobs_data = []
    for date, tobs in results:
        tobs_dict = {}
        tobs_dict["Date"] = date
        tobs_dict["Tobs"] = tobs
        tobs_data.append(tobs_dict)

    return jsonify(tobs_data)


@app.route('/api/v1.0/<start>')
def Starts(start):
    session = Session(engine)
    start_date = (dt.date(2017,8,23)) - (dt.timedelta(days = 365))
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start_date).all()
    session.close()

    tobs_data = []
    for min,avg,max in results:
        tobs_dict = {}
        tobs_dict["Min"] = min
        tobs_dict["Average"] = avg
        tobs_dict["Max"] = max
        tobs_data.append(tobs_dict)

    return jsonify(tobs_data)

@app.route('/api/v1.0/<start>/<end>')
def Starts_Ends(start, end):
    session = Session(engine)
    start_date = (dt.date(2017,8,23)) - (dt.timedelta(days = 365))
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start_date).all()
    session.close()

    tobs_data = []
    for min,avg,max in results:
        tobs_dict = {}
        tobs_dict["Min"] = min
        tobs_dict["Average"] = avg
        tobs_dict["Max"] = max
        tobs_data.append(tobs_dict)

    return jsonify(tobs_data)


if __name__ == '__main__':
    app.run(debug=True)