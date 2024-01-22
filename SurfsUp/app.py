# Import the dependencies.
import numpy as np
import pandas as pd
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
# engine = create_engine("sqlite:///Resources/hawaii.sqlite")
engine = create_engine("sqlite:///SurfsUp/Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Station = Base.classes.station
Measurement = Base.classes.measurement

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
def home():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start_date<br/>"
        f"/api/v1.0/start_date/end_date"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return JSON representation of precipitation data for the last 12 months."""
    # Calculate the date one year from the last date in the data set
    most_recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]

    # Calculate the date one year from the last date in data set.
    one_year_ago = pd.to_datetime(most_recent_date) - pd.DateOffset(days=365)
    one_year_ago_str = one_year_ago.strftime('%Y-%m-%d')  # Convert to string

    # Perform a query to retrieve the data and precipitation scores
    precipitation_data = session.query(Measurement.date, Measurement.prcp)\
                        .filter(Measurement.date >= one_year_ago_str)\
                        .order_by(Measurement.date).all()

    # Convert the query results to a dictionary
    precipitation_dict = {date: prcp for date, prcp in precipitation_data}

    return jsonify(precipitation_dict)



@app.route("/api/v1.0/stations")
def stations():
    """Return JSON list of stations from the dataset."""
    # Query station data
    station_data = session.query(Station.station, Station.name).all()

    # Convert the query results to a list of dictionaries
    stations_list = [{"Station": station, "Name": name} for station, name in station_data]

    return jsonify(stations_list)


@app.route("/api/v1.0/tobs")
def tobs():
    """Query the dates and temperature observations of the most-active station for the previous year of data.
    Return a JSON list of temperature observations for the previous year.
    """
    most_active_station = session.query(Measurement.station, func.count(Measurement.station))\
                            .group_by(Measurement.station)\
                            .order_by(func.count(Measurement.station).desc())\
                            .first()[0]

    most_recent_date = session.query(func.max(Measurement.date)).scalar()
    one_year_ago = dt.datetime.strptime(most_recent_date, "%Y-%m-%d") - dt.timedelta(days=365)

    tobs_data = session.query(Measurement.date, Measurement.tobs)\
                .filter(Measurement.station == most_active_station)\
                .filter(Measurement.date >= one_year_ago)\
                .all()

    tobs_list = [{"Date": date, "Temperature": tobs} for date, tobs in tobs_data]

    return jsonify(tobs_list)


@app.route("/api/v1.0/<start>")
def temperature_start(start):
    """Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start.
    Calculate TMIN, TAVG, and TMAX for all the dates greater than or equal to the start date.
    """
    temperature_data = session.query(func.min(Measurement.tobs),
                                     func.avg(Measurement.tobs),
                                     func.max(Measurement.tobs))\
                                    .filter(Measurement.date >= start)\
                                    .all()

    temperature_list = [{"TMIN": tmin, "TAVG": tavg, "TMAX": tmax} for tmin, tavg, tmax in temperature_data]

    return jsonify(temperature_list)


@app.route("/api/v1.0/<start>/<end>")
def temperature_range(start, end):
    """Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start-end range.
    Calculate TMIN, TAVG, and TMAX for the dates from the start date to the end date, inclusive.
    """
    temperature_data = session.query(func.min(Measurement.tobs),
                                     func.avg(Measurement.tobs),
                                     func.max(Measurement.tobs))\
                                    .filter(Measurement.date >= start)\
                                    .filter(Measurement.date <= end)\
                                    .all()

    temperature_list = [{"TMIN": tmin, "TAVG": tavg, "TMAX": tmax} for tmin, tavg, tmax in temperature_data]

    return jsonify(temperature_list)


if __name__ == "__main__":
    app.run(debug=True)