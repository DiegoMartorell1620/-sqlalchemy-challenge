# Import the dependencies.
import numpy as np

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
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)


# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station


# Create our session (link) from Python to the DB
session = Session(engine)

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
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/&lt;start&gt;<br/>"
        f"/api/v1.0/&lt;start&gt;/&lt;end&gt;<br/>")
     

@app.route("/api/v1.0/precipitation")
def precipitation():
#Convert the query results from your precipitation analysis 
#(i.e. retrieve only the last 12 months of data) to a dictionary using date as the key and prcp as the value
    results_precipitation = session.query(Measurement.date,Measurement.prcp).\
    filter(Measurement.date >= '2016-08-23').\
    order_by(Measurement.date).all()

    session.close()

    # Convert list of tuples into normal list
    all_results_precipitation = [{'Date': result[0], 'Precipitation': result[1]} for result in results_precipitation]

    return jsonify(all_results_precipitation)

@app.route("/api/v1.0/stations")
def stations():
#Return a JSON list of stations from the dataset.
    results_stations = session.query(Station.station).all()

    session.close()

    # Convert list of tuples into normal list
    all_results_stations = list(np.ravel(results_stations))

    return jsonify(all_results_stations)

@app.route("/api/v1.0/tobs")
def tobs():
#Query the dates and temperature observations of the most-active station for the previous year of data
    results_tobs =session.query(func.count(Measurement.tobs),Measurement.tobs).\
    filter(Measurement.date >= '2016-08-18').\
    filter(Measurement.station == 'USC00519281').\
    group_by(Measurement.tobs).\
    order_by(func.count(Measurement.tobs)).all()

    session.close()

    # Convert list of tuples into normal list
    all_results_tobs = [{'Count': result[0], 'Temperature': result[1]} for result in results_tobs]


    return jsonify(all_results_tobs)

@app.route("/api/v1.0/<start>")
#Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start date
def temperatures_start_date(start):
    results_tobs_start_date =session.query(func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)).\
    filter(Measurement.date >= start).all()

    session.close()

    # Convert list of tuples into normal list
    all_results_tobs_start_date= [{'Min Temperature': result[0], 'Average Temperature': result[1],'Max Temperature': result[2]} for result in results_tobs_start_date]

    return jsonify(all_results_tobs_start_date)

@app.route("/api/v1.0/<start>/<end>")
#Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start or start-end range.
def temperatures_start_date_end(start,end):
    results_tobs_start_date_end =session.query(func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)).\
    filter(Measurement.date >= start).filter(Measurement.date<=end).all()

    session.close()

    # Convert list of tuples into normal list
    all_results_tobs_start_date_end= [{'Min Temperature': result[0], 'Average Temperature': result[1],'Max Temperature': result[2]} for result in results_tobs_start_date_end]

    return jsonify(all_results_tobs_start_date_end)

