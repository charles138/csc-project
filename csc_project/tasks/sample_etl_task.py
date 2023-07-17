# import pandas as pd
# from sklearn.datasets import fetch_california_housing
from csc_project.common import Task
from pyspark.sql.types import *
from pyspark.sql.functions import *
class SampleETLTask(Task):
    def _write_data(self):
        db = self.conf["output"].get("database", "default")
        table = self.conf["output"]["table"]
        self.logger.info(f"Writing housing dataset to {db}.{table}")
        ####========================================================
        ### Avoided using pandas 2.0 for
        ### Error: "AttributeError: 'DataFrame' object has no attribute 'iteritems'" in pandas 2.0.1. 
        ####========================================================
        # _data: pd.DataFrame = fetch_california_housing(as_frame=True).frame
        # df = self.spark.createDataFrame(_data)
        # df.write.format("delta").mode("overwrite").saveAsTable(f"{db}.{table}")
        inputdf_schema = StructType([ \
        StructField("MedInc", DoubleType(), True), \
        StructField("HouseAge", LongType(), True), \
        StructField("AveRooms", DoubleType(), True), \
        StructField("AveBedrms", DoubleType(), True), \
        StructField("Population", LongType(), True), \
        StructField("AveOccup", DoubleType(), True), \
        StructField("Latitude", DoubleType(), True), \
        StructField("Longitude", DoubleType(), True), \
        StructField("MedHouseVal", DoubleType(), True) \
        ])
        input_data = \
        [(8.3252,41,6.984126984126984,1.0238095238095237,322,2.5555555555555554,37.88,-122.23,4.526), \
        (8.3014,21,6.238137082601054,0.9718804920913884,2401,2.109841827768014,37.86,-122.22,3.585), \
        (7.2574,52,8.288135593220339,1.073446327683616,496,2.8022598870056497,37.85,-122.24,3.521), \
        (5.6431,52,5.8173515981735155,1.0730593607305936,558,2.547945205479452,37.85,-122.25,3.413), \
        (3.8462,52,6.281853281853282,1.0810810810810811,565,2.1814671814671813,37.85,-122.25,3.422), \
        (4.0368,52,4.761658031088083,1.1036269430051813,413,2.139896373056995,37.85,-122.25,2.697), \
        (3.6591,52,4.9319066147859925,0.9513618677042801,1094,2.1284046692607004,37.84,-122.25,2.992), \
        (3.12,52,4.797527047913447,1.061823802163833,1157,1.7882534775888717,37.84,-122.25,2.414), \
        (2.0804,42,4.294117647058823,1.1176470588235294,1206,2.026890756302521,37.84,-122.26,2.267), \
        (3.6912,52,4.970588235294118,0.9901960784313726,1551,2.172268907563025,37.84,-122.25,2.611), \
        (3.2031,52,5.477611940298507,1.0796019900497513,910,2.263681592039801,37.85,-122.26,2.815)]
        df = self.spark.createDataFrame(data=input_data, schema=inputdf_schema)
        df.write.format("delta").mode("overwrite").saveAsTable(f"{db}.{table}")
        self.logger.info("Dataset successfully written")
    def launch(self):
        self.logger.info("Launching sample ETL task")
        self._write_data()
        self.logger.info("Sample ETL task finished!")
# if you're using python_wheel_task, you'll need the entrypoint function to be used in setup.py
def entrypoint():  # pragma: no cover
    task = SampleETLTask()
    task.launch()
# if you're using spark_python_task, you'll need the __main__ block to start the code execution
if __name__ == '__main__':
    entrypoint()
