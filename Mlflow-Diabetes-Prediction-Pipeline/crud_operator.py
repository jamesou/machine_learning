import os

import delta
import mimesis
import pyspark

from pyspark.sql import SparkSession
from pyspark.sql.functions import asc

def get_spark() -> SparkSession:
    builder = (
        pyspark.sql.SparkSession.builder.appName("MachineLearning")
        .config("spark.jars.packages", "io.delta:delta-core_2.12:2.0.0")
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
        .config("spark.sql.warehouse.dir", "/Users/jamesoujamesou/Downloads/sit_thesis/IT819/implementation/machine_learning/Mlflow-Diabetes-Prediction-Pipeline/database")
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
        .config("spark.mlflow.trackingUri", "http://localhost:5000")
    )
    spark = delta.configure_spark_with_delta_pip(builder).getOrCreate()
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


def main():
    dir = os.getcwd() + os.sep + "database"
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




if __name__ == "__main__":
    main()
