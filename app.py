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
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with = engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

#Checkpoint_1
print("SQLITE Data Uploaded")

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################
#homepage route
@app.route("/")
def homepage():
    """List all available routes"""
    return(
        f"Welcome to your Hawaiian Vacation weather guide!<br/>"
        f"<p> Please make your selection from the Available Routes:<p>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start_date/<start_date><br/>"
        f"/api/v1.0/start_date&end_date/<start>/<end>"
        f"<p> Please note: input 'start' and 'end' date should be in the format MMDDYYYY.</p>"
    )
#precipitation route
@app.route("/api/v1.0/precipitation")
def precip():
    #retrieve the last 12 months of precipitation data
    year_precip = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= "2016, 8, 23").all()

    #convert to a dictionary using date as the key and prcp as the value
    
    precip_dict = dict((key, value) for key, value in year_precip)
    return jsonify(precip_dict)

#Stations route
#Return a a list of all stations from the dataset
@app.route("/api/v1.0/stations")
def stations():
    #query all station names
    result = session.query(Station.name).all()
    
    #convert list
    all_stations = list(np.ravel(result))
    return jsonify(all_stations)

#tobs route
#Return all temp observations from the most active station for the previous year

@app.route("/api/v1.0/tobs")
def tobs():
    #query the dates and tobs of the most active station

    results = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.station == "USC00519281").\
        filter(Measurement.date >= "2016, 8, 23").all()
    #return a list of tobs for the previous year
    most_active_temp = list(np.ravel(results))
    return jsonify(most_active_temp)


#start range route
#Return a list
@app.route("/api/v1.0/start_date/<start_date>")
def define_start(start_date):
   
    temp = [
        func.min(Measurement.tobs),
        func.max(Measurement.tobs),
        func.avg(Measurement.tobs)]
    result = dt.datetime.strptime(start_date,"%m%d%Y")
    start_temp = session.query(*temp).\
        filter(Measurement.date >= result).all()
    final_temp= list(np.ravel(start_temp))
    return jsonify(final_temp)
#start-end range route
@app.route("/api/v1.0/start_date&end_date/<start>/<end>")
def define_start_end(start, end):
    temps = [
        func.min(Measurement.tobs),
        func.max(Measurement.tobs),
        func.avg(Measurement.tobs)]
     
    result1 = dt.datetime.strptime(start,"%m%d%Y")
    result2 = dt.datetime.strptime(end, "%m%d%Y")
    
    start_end_temp = session.query(*temps).\
        filter(Measurement.date >= result1).\
        filter(Measurement.date <= result2).all()
    last_temp= list(np.ravel(start_end_temp))
    return jsonify(last_temp)

#Close session
session.close()



if __name__ == "__main__":
    app.run(debug=True)