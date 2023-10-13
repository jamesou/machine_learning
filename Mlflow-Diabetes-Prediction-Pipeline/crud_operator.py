import os
import sys
import delta
import mimesis
from pyspark.sql import SparkSession
from pyspark.sql.functions import asc

builder = (
        SparkSession.builder.appName("MachineLearning")
        .config("spark.jars.packages", "io.delta:delta-core_2.12:2.2.0")
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
        .config("spark.sql.warehouse.dir", "/Users/jamesoujamesou/Downloads/sit_thesis/IT819/implementation/machine_learning/Mlflow-Diabetes-Prediction-Pipeline/databases")
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
        .config("spark.mlflow.trackingUri", "http://localhost:5000")
        .config("spark.jars.repositories","https://maven-central.storage-download.googleapis.com/maven2/")
    )

def get_spark() -> SparkSession:
    # spark-sql --conf spark.jars.packages=io.delta:delta-core_2.12:2.2.0 --conf spark.sql.extensions=io.delta.sql.DeltaSparkSessionExtension --conf spark.sql.warehouse.dir=/Users/jamesoujamesou/Downloads/sit_thesis/IT819/implementation/machine_learning/Mlflow-Diabetes-Prediction-Pipeline/databases --conf spark.sql.catalog.spark_catalog=org.apache.spark.sql.delta.catalog.DeltaCatalog --conf spark.sql.resultTable.borderStyle=unicode --conf spark.sql.resultTable.headerName=true --conf spark.sql.resultTable.maxColWidth=20
    spark = builder.master("local[*]")\
        .enableHiveSupport()\
        .getOrCreate()
    spark.sparkContext.setLogLevel("INFO")
    return spark

def get_delta_spark() -> SparkSession:
    # this way likes hiberate, use api to operate tables
    spark = delta.configure_spark_with_delta_pip(builder).master("local[*]")\
        .enableHiveSupport()\
        .getOrCreate()
    spark.sparkContext.setLogLevel("INFO")
    return spark
#Test function
def create_dataset(i: int = 100) -> list[dict]:
    fake = mimesis.Generic()
    output = [
        {
            "name": fake.person.name(),
            "surname": fake.person.surname(),
            "birthday": fake.datetime.date(1960, 2023),
            "email": fake.person.email(),
            "country": fake.address.country(),
            "state": fake.address.state(),
            "city": fake.address.city(),
        }
        for _ in range(i)
    ]
    return output

def use_delta_api():
    dir = os.getcwd() + os.sep + "databases"
    with get_delta_spark() as spark:
        # df = spark.createDataFrame(create_dataset(i=1_000_000))
        # df.write.format("delta").mode("overwrite").save(dir + os.sep + "people")
        # df.write \
        #     .format("delta") \
        #     .mode("overwrite") \
        #     .saveAsTable("delta_people")
        df = spark.read.format("delta").load(dir + os.sep + "people")
        df.groupBy("state").count().sort(asc("state")).show()
        df = df.select(df.name, df.surname, df.birthday, df.email, df.country, df.state, df.city)
        df.show()
        print("Number of records: ", df.count())
        df.printSchema()


def use_spark_sql():
    with get_delta_spark() as spark:
        # Query the Delta table
        df = spark.sql("SELECT * FROM machine_learning.patient limit 10")
        # Print the results
        df.show()

def load_cvs_data():
    with get_delta_spark() as spark:
        #load csv file
        csv_file_path = "/Users/jamesoujamesou/Downloads/sit_thesis/IT819/implementation/machine_learning/Mlflow-Diabetes-Prediction-Pipeline/datafiles/patient.csv"       
        spark.sql(f"INSERT INTO machine_learning.patient SELECT * FROM csv.`{csv_file_path}`")
        csv_file_path = "/Users/jamesoujamesou/Downloads/sit_thesis/IT819/implementation/machine_learning/Mlflow-Diabetes-Prediction-Pipeline/datafiles/diagnosis.csv"       
        spark.sql(f"INSERT INTO machine_learning.diagnosis SELECT * FROM csv.`{csv_file_path}`")
        csv_file_path = "/Users/jamesoujamesou/Downloads/sit_thesis/IT819/implementation/machine_learning/Mlflow-Diabetes-Prediction-Pipeline/datafiles/lifestyle.csv"       
        spark.sql(f"INSERT INTO machine_learning.lifestyle SELECT * FROM csv.`{csv_file_path}`")
        csv_file_path = "/Users/jamesoujamesou/Downloads/sit_thesis/IT819/implementation/machine_learning/Mlflow-Diabetes-Prediction-Pipeline/datafiles/blood_glucose.csv"       
        spark.sql(f"INSERT INTO machine_learning.blood_glucose SELECT * FROM csv.`{csv_file_path}`")

if __name__ == "__main__":
    try:
        #use_delta_api()
        use_spark_sql()
        # load_cvs_data()
    finally:
        sys.exit(0)

