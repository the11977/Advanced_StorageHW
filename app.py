# Import Flask
from flask import Flask, jsonify

# Dependencies and Setup
import numpy as np
import datetime as dt

# Python SQL Toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy.pool import StaticPool

#################################################
# Database Setup
#################################################
# Reference: https://stackoverflow.com/questions/33055039/using-sqlalchemy-scoped-session-in-theading-thread
engine = create_engine("sqlite:///Resources/hawaii.sqlite", connect_args={"check_same_thread": False}, poolclass=StaticPool, echo=True)

# Reflect Existing Database Into a New Model
Base = automap_base()
# Reflect the Tables
Base.prepare(engine, reflect=True)

# Save References to Each Table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create Session (Link) From Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################
# Home Route
@app.route("/")
def welcome():
        return """<html>
<h1>Hawaii Weather App w/ Flask API</h1>
<img src="data:image/jpeg;base64,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" alt="Hawaii Weather"/>
<p>Precipitation Analysis:</p>
<ul>
  <li><a href="/api/v1.0/precipitation">/api/v1.0/precipitation</a></li>
</ul>
<p>Station Analysis:</p>
<ul>
  <li><a href="/api/v1.0/stations">/api/v1.0/stations</a></li>
</ul>
<p>Temperature Analysis:</p>
<ul>
  <li><a href="/api/v1.0/tobs">/api/v1.0/tobs</a></li>
</ul>
<p>Start Day Analysis:</p>
<ul>
  <li><a href="/api/v1.0/2017-03-14">/api/v1.0/2017-03-14</a></li>
</ul>
<p>Start & End Day Analysis:</p>
<ul>
  <li><a href="/api/v1.0/2017-03-14/2017-03-28">/api/v1.0/2017-03-14/2017-03-28</a></li>
</ul>
</html>
"""

# Precipitation Route
@app.route("/api/v1.0/precipitation")
def precipitation():
        # Convert the Query Results to a Dictionary Using `date` as the Key and `prcp` as the Value
        # Calculate the Date 1 Year Ago from the Last Data Point in the Database
        one_year_ago = dt.date(2017,8,23) - dt.timedelta(days=365)
        # Design a Query to Retrieve the Last 12 Months of Precipitation Data Selecting Only the `date` and `prcp` Values
        prcp_data = session.query(Measurement.date, Measurement.prcp).\
                filter(Measurement.date >= one_year_ago).\
                order_by(Measurement.date).all()
        # Convert List of Tuples Into a Dictionary
        prcp_data_list = dict(prcp_data)
        # Return JSON Representation of Dictionary
        return jsonify(prcp_data_list)

# Station Route
@app.route("/api/v1.0/stations")
def stations():
        # Return a JSON List of Stations From the Dataset
        stations_all = session.query(Station.station, Station.name).all()
        # Convert List of Tuples Into Normal List
        station_list = list(stations_all)
        # Return JSON List of Stations from the Dataset
        return jsonify(station_list)

# TOBs Route
@app.route("/api/v1.0/tobs")
def tobs():
        # Query for the Dates and Temperature Observations from a Year from the Last Data Point
        one_year_ago = dt.date(2017,8,23) - dt.timedelta(days=365)
        # Design a Query to Retrieve the Last 12 Months of Precipitation Data Selecting Only the `date` and `prcp` Values
        tobs_data = session.query(Measurement.date, Measurement.tobs).\
                filter(Measurement.date >= one_year_ago).\
                order_by(Measurement.date).all()
        # Convert List of Tuples Into Normal List
        tobs_data_list = list(tobs_data)
        # Return JSON List of Temperature Observations (tobs) for the Previous Year
        return jsonify(tobs_data_list)

# Start Day Route
@app.route("/api/v1.0/<start>")
def start_day(start):
        start_day = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                filter(Measurement.date >= start).\
                group_by(Measurement.date).all()
        # Convert List of Tuples Into Normal List
        start_day_list = list(start_day)
        # Return JSON List of Min Temp, Avg Temp and Max Temp for a Given Start Range
        return jsonify(start_day_list)

# Start-End Day Route
@app.route("/api/v1.0/<start>/<end>")
def start_end_day(start, end):
        start_end_day = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                filter(Measurement.date >= start).\
                filter(Measurement.date <= end).\
                group_by(Measurement.date).all()
        # Convert List of Tuples Into Normal List
        start_end_day_list = list(start_end_day)
        # Return JSON List of Min Temp, Avg Temp and Max Temp for a Given Start-End Range
        return jsonify(start_end_day_list)

# Define Main Behavior
if __name__ == '__main__':
    app.run(debug=True)