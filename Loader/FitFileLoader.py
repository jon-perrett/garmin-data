import fitparse
import pandas as pd


class FitFileLoader:

    def __init__(self,path):
        self.PATH = path
        self.FILE = fitparse.FitFile(path)

        for r in self.FILE.get_messages("sport"):
            self.activity_type = r.get_values()["sport"]
        
    def load(self):
        """
        Takes pathname of a .fit file and returns the record data as an object with the following

        Class Variables:
        activity_type : "running" | "cycle" | "swim" | "hike" | "other"
        time_data : Pandas DataFrame with timeseries data from the activity.
        activity_duration : length of activity in seconds
        activity_distance : distance of acitivty in metres
        max_hr : maximum heart rate in activity
        average_hr : average heart rate during activity
        max_speed : maximum speed (m/s)
        min_speed : minimum speed (m/s)
        average_speed : average speed (m/s)
        min_long : minimum longitude 
        max_long : maximum longitude
        min_lat : minimum latitude
        max_lat : maximum latitude
        min_altitude : minimum altitude (m)
        max_altitude : maximum altitude (m)
        elev_gain : elevation gained (m)


        Columns for run inlude:
        altitude : (m)
        distance: (m)
        enhanced_altitude: (m)
        enhanced_speed: (m/s)
        heart_rate: (bpm)
        position_lat: (semicircles)
        position_long: (semicircles)
        speed: (m/s)
        timestamp: (yyyy-mm-dd HH:MM:SS)
        """
        columns=["altitude","distance","enhanced_altitude","enhanced_speed","heart_rate","position_lat","position_long","speed","timestamp"]
        fitfile = self.FILE
        df = pd.DataFrame()
        # Iterate over all messages of type "record"
        # (other types include "device_info", "file_creator", "event", etc)
        for record in fitfile.get_messages("record"):
            # Records can contain multiple pieces of data (ex: timestamp, latitude, longitude, etc)
            
            df = df.append(record.get_values(),ignore_index=True)
            # for data in record:

            #     # Print the name and value of the data (and the units if it has any)
            #     if data.units:
            #         print(" * {}: {} ({})".format(data.name, data.value, data.units))
            #     else:
            #         print(" * {}: {}".format(data.name, data.value))

            # print("---")
        self.time_data = df[columns].sort_values(by="distance")
        self.activity_distance = df["distance"].max()
        self.max_hr = df["heart_rate"].max()
        self.average_hr = df["heart_rate"].mean()
        self.max_speed = df["speed"].max()
        self.min_speed = df["speed"].min()
        self.average_speed = df["speed"].mean()
        self.min_long = df["position_long"].min()
        self.max_long = df["position_long"].max()
        self.min_lat = df["position_lat"].min()
        self.max_lat = df["position_lat"].max()
        self.min_altitude = df["altitude"].min()
        self.max_altitude = df["altitude"].max()
        self.start_time = df["timestamp"][0]
        self.duration = df["timestamp"].max() - df["timestamp"].min()

    def list_messages(self,type):
        for record in self.FILE.get_messages(type):
            print(record)
            for data in record:

                print(" * {}: {}".format(data.name,data.value))


if __name__ == "__main__":
    f = FitFileLoader("garmin-data\_demo_data\slow_run.fit")
    print(f.activity_type)
    f.load()
    print(f.duration)