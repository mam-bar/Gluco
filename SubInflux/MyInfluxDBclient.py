from influxdb_client_3 import InfluxDBClient3, Point
from datetime import datetime, timedelta
import pandas as pd


class MyinfluxDBclient:
    def __init__(self, database="Sensors"):
        self.token = "rqEgnFIBjcYHTsMUQh1w3sNWSEu4dQ2Cz1cn-jZsawQO2SgZssL26BPtKgZ-GMQeaISYkZYGJiSRS-q568IGMg=="
        self.org = "Barati"
        self.host = "https://eu-central-1-1.aws.cloud2.influxdata.com"
        self.influxDBclient = InfluxDBClient3(
            host=self.host, token=self.token, org=self.org, database=database
        )

        self.database = database

    def LastN(self, client_id, Nminutes):
        query = f"""
                    SELECT * 
                    FROM 'Glucose Level' 
                    WHERE time >= now() - interval '{Nminutes} minutes'
                    AND "userID" = '{client_id}'
        """

        # Execute the query in SQL mode
        result = self.influxDBclient.query(query=query, language="sql", mode="pandas")
        summary = {
            "Highest": float(round(result["measurement"].max(), 2)),
            "Lowest": float(round(result["measurement"].min(), 2)),
            "Average": float(round(result["measurement"].mean(), 2)),
        }
        return summary

    def writeInflux(self, client_id, sensor_id, measurement):
        data = {
            "userID": client_id,
            "sensorID": sensor_id,
            "measurement": measurement,
        }

        point = (
            Point("Glucose Level")
            .tag("userID", data["userID"])  # userID as a tag
            .tag("sensorID", data["sensorID"])  # sensorID as a tag
            .field("measurement", data["measurement"])  # Single field for measurements
        )
        self.influxDBclient.write(database=self.database, record=point)


# grafana all access token = c7-RJGk55WD8RHEyYRycG3UqoG_YyLHOM0BmMpKySx2-cKu1WrkBSNNDUqkh38VrTZD5o-F5WWcrXXfJW6OzWg==
if __name__ == "__main__":
    db = MyinfluxDBclient("Sensors")
    print(db.LastN("Alireza", 2))
