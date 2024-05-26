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

# Create engine using the `hawaii.sqlite` database file
engine = create_engine('sqlite:///Resources/hawaii.sqlite')

# Declare a Base using `automap_base()`
Base = automap_base()

# Use the Base class to reflect the database tables
Base.prepare(engine, reflect=True)

# Assign the measurement class to a variable called `Measurement` and
# the station class to a variable called `Station`
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create a session
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
    return(
        f"Avaiable Routes:<br/>"
        f"Precipitation: /api/v1.0/precipitation<br/>"
        f"Stations: /api/v1.0/stations<br/>"
        f"Temperatures: /api/v1.0/tobs<br/>"
        f"Temperature stat from the start date(yyyy-mm-dd): /api/v1.0/[start_date format:yyyy-mm-dd]<br/>"
        f"Temperature stat from start to end dates(yyyy-mm-dd): /api/v1.0/[start_date format:yyyy-mm-dd]/[end_date format:yyyy-mm-dd]<br/>"
    )

@app.route("/api/v1.0/<start_date>")
def Start_date(start_date):
    # Create Session
    session = Session(engine)

    # Query all tobs
    results_query = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                filter(Measurement.date >= start_date).all()

    session.close()

    # Create dictionary and append start_date_tobs list
    start_date_tobs = []
    for min, avg, max in results_query:
        start_date_dict = {}
        start_date_dict["min_temp"] = min
        start_date_dict["avg_temp"] = avg
        start_date_dict["max_temp"] = max
        start_date_tobs.append(start_date_dict) 
    return jsonify(start_date_tobs)

@app.route("/api/v1.0/<start_date>/<end_date>")
def Start_end_date(start_date, end_date):
    # Create Session
    session = Session(engine)

    # Query all tobs
    results_query = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()

    session.close()
  
    # Create dictionary and append to start_end_tobs list
    start_end_tobs = []
    for min, avg, max in results_query:
        start_end_dict = {}
        start_end_dict["min_temp"] = min
        start_end_dict["avg_temp"] = avg
        start_end_dict["max_temp"] = max
        start_end_tobs.append(start_end_dict) 
    

    return jsonify(start_end_tobs)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create Session
    session = Session(engine)

    # Query all tobs
    results_query = session.query(Measurement.date,  Measurement.tobs,Measurement.prcp).filter(Measurement.date >= '2016-08-23').\
    filter(Measurement.station=='USC00519281').order_by(Measurement.date).all()

    session.close()

    # Convert list to dictionary
    all_tobs = []
    for prcp, date,tobs in results_query:
        tobs_dict = {}
        tobs_dict["prcp"] = prcp
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs
        
        all_tobs.append(tobs_dict)

    return jsonify(all_tobs)

@app.route("/api/v1.0/stations")
def stations():
    # Create Session
    session = Session(engine)
    
    # Query all Stations
    results_query = session.query(Station.station).order_by(Station.station).all()

    session.close()

    # Convert tuples list into normal list
    all_stations = list(np.ravel(results_query))

    return jsonify(all_stations)

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create Session
    session = Session(engine)

    # Query all Precipitation
    results_query = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= "2016-08-24").all()

    session.close()

    # Convertvlist to Dictionary
    all_prcp = []
    for date,prcp  in results_query:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
               
        all_prcp.append(prcp_dict)

    return jsonify(all_prcp)

if __name__ == '__main__':
    app.run(debug=True)
