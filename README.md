# sqlalchemy-challenge
SQLAlchemy module challenge

Part 1: Analyze and Explore the Climate Data [climate_starter](climate_starter.ipynb)

    Used the SQLAlchemy function to connect to the SQLite database.
    Used the SQLAlchemy automap_base() function to reflect the tables into classes, and then saved references to the classes named station and measurement.
    Linked Python to the database by creating a SQLAlchemy session.

    Precipitation Analysis:
    1. Found the most recent date in the dataset.
    2. Got the previous 12 months of precipitation data by querying the previous 12 months of data, using the most recent date.
    3. Loaded the query results into a Pandas DataFrame and sorted by date.
    4. Plotted the results on a bar chart by using the DataFrame plot method.
    5. Printed the summary statistics for the precipitation data.

    Station Analysis:
    1. Calculated the total number of stations in the dataset.
    2. Found the most-active stations and sorted in descending order.
    3. Station ID with the greatest number of observations - 'USC00519281'
    4. Calculated the lowest, highest, and average temperatures that filters on the most-active station id.
    5. Got the previous 12 months of temperature observation (TOBS) data and plotted the results on a histogram.

    Closed the session.

Part 2: Design Your Climate App [app.py](app.py)

    Designed a Flask API based on the previously developed queries.
    1. Listed all the available routes at the homepage (/).
    2. From precipitation analysis, retrieved only the last 12 months of data to a dictionary using date as the key and prcp as the value.Returned the json representation of the dictionary at (/api/v1.0/precipitation).
    3. Returned a JSON list of stations from the dataset at (/api/v1.0/stations).
    4. Returned a JSON list of temperature observations for the previous year at (/api/v1.0/tobs).
    5. Returned a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start or start-end range (/api/v1.0/<start> and /api/v1.0/<start>/<end>).
