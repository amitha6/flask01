# flask01

Implementation of two APIS endpoints /report and /ingest. /ingest API will consume a metric-data point with three metric points and /report endpoint will return the JSON object of average of collected datapoints over a day and month. Both the API's are implemented in Flask with MongoDB databse.   

How to run the code:   

Make sure you have python installed.  

Install both flask and pymongo  

pip install Flask pymongo  

Ensure you have the MongoDb server running.   

Command to run the application: python app.py  

Open postman and make a post request at 5000 to /ingest endpoint http://127.0.0.1:5000/ingest with JSON payload containing the metrics.    

The get request http://127.0.0.1:5000/report API endpoint will return the average JSON object over a day and a month.   


