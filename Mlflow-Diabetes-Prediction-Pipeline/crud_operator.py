import os

import delta
import mimesis
import pyspark

from pyspark.sql import SparkSession
from pyspark.sql.functions import asc
import pyspark.sql as sql
def get_spark() -> SparkSession:
    # this way likes hiberate, use api to operate tables
    # builder = (
    #     SparkSession.builder.appName("MachineLearning")
    #     .config("spark.jars.packages", "io.delta:delta-core_2.12:2.2.0")
    #     .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
    #     .config("spark.sql.warehouse.dir", "/Users/jamesoujamesou/Downloads/sit_thesis/IT819/implementation/machine_learning/Mlflow-Diabetes-Prediction-Pipeline/databases")
    #     .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
    #     .config("spark.mlflow.trackingUri", "http://localhost:5000")
    #     .config("spark.jars.repositories","https://maven-central.storage-download.googleapis.com/maven2/")
    #     .master("local[*]")
    #     .enableHiveSupport()
    #     .getOrCreate()
    # )
    # spark = delta.configure_spark_with_delta_pip(builder).getOrCreate()

    # spark-sql --conf spark.jars.packages=io.delta:delta-core_2.12:2.2.0 --conf spark.sql.extensions=io.delta.sql.DeltaSparkSessionExtension --conf spark.sql.warehouse.dir=/Users/jamesoujamesou/Downloads/sit_thesis/IT819/implementation/machine_learning/Mlflow-Diabetes-Prediction-Pipeline/databases --conf spark.sql.catalog.spark_catalog=org.apache.spark.sql.delta.catalog.DeltaCatalog --conf spark.jars.repositories=https://maven-central.storage-download.googleapis.com/maven2/
    spark = SparkSession.builder.appName("MachineLearning")\
        .config("spark.jars.packages", "io.delta:delta-core_2.12:2.2.0")\
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")\
        .config("spark.sql.warehouse.dir", "/Users/jamesoujamesou/Downloads/sit_thesis/IT819/implementation/machine_learning/Mlflow-Diabetes-Prediction-Pipeline/databases")\
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")\
        .config("spark.mlflow.trackingUri", "http://localhost:5000")\
        .config("spark.jars.repositories","https://maven-central.storage-download.googleapis.com/maven2/")\
        .master("local[*]")\
        .enableHiveSupport()\
        .getOrCreate()
    spark.sparkContext.setLogLevel("ERROR")
    return spark


def create_dataset(i: int = 100) -> list[dict]:
    fake = mimesis.Generic()
    output = [
        {
            "name": fake.person.name(),
            "surname": fake.person.surname(),
            "birthday": fake.datetime.date(1960, 2010),
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
    with get_spark() as spark:
        # df = spark.createDataFrame(create_dataset(i=1_000_000))
        # df.write.format("delta").mode("overwrite").save(dir + os.sep + "people")
        df = spark.read.format("delta").load(dir + os.sep + "people")

        df.groupBy("state").count().sort(asc("state")).show()
        df = df.select(df.name, df.surname, df.birthday, df.email, df.country, df.state, df.city)
        df.show()
        print("Number of records: ", df.count())
        df.printSchema()
    spark.stop()
def use_spark_sql():
    spark = get_spark()
    spark.sql("use machine_learning")
    # Query the Delta data file
    df = spark.sql(" SELECT * FROM patient limit 10")
    # Print the results
    df.show()
    spark.stop()

if __name__ == "__main__":
    use_spark_sql()
