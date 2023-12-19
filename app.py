from flask import Flask, request, jsonify
from datetime import datetime, timedelta
from pymongo import MongoClient

app = Flask(_name_)

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['metrics']
metric_collection = db['metric_data']

def persist_metric(metric):
    metric['timestamp'] = datetime.now()
    metric_collection.insert_one(metric)

def calculate_average_metrics(start_time):
    day_metrics = {"ram_consumed": 0, "cpu": 0, "disk_usage_percent": 0}
    month_metrics = {"ram_consumed": 0, "cpu": 0, "disk_usage_percent": 0}
    day_count = 0
    month_count = 0

    for metric in metric_collection.find({"timestamp": {"$gte": start_time}}):
        time_difference = datetime.now() - metric["timestamp"]

        if time_difference <= timedelta(days=1):
            day_metrics["ram_consumed"] += metric["ram_consumed"]
            day_metrics["cpu"] += metric["cpu"]
            day_metrics["disk_usage_percent"] += metric["disk_usage_percent"]
            day_count += 1

        if time_difference <= timedelta(days=30):
            month_metrics["ram_consumed"] += metric["ram_consumed"]
            month_metrics["cpu"] += metric["cpu"]
            month_metrics["disk_usage_percent"] += metric["disk_usage_percent"]
            month_count += 1

    if day_count > 0:
        day_metrics["ram_consumed"] /= day_count
        day_metrics["cpu"] /= day_count
        day_metrics["disk_usage_percent"] /= day_count

    if month_count > 0:
        month_metrics["ram_consumed"] /= month_count
        month_metrics["cpu"] /= month_count
        month_metrics["disk_usage_percent"] /= month_count

    return {"day": day_metrics, "month": month_metrics}

@app.route('/ingest', methods=['POST'])
def ingest():
    try:
        metric = request.get_json()
        persist_metric(metric)
        return jsonify({"message": "Metric ingested successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/report', methods=['GET'])
def report():
    try:
        start_time = datetime.now() - timedelta(days=30)
        average_metrics = calculate_average_metrics(start_time)
        return jsonify(average_metrics)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if _name_ == '_main_':
    app.run(debug=True)