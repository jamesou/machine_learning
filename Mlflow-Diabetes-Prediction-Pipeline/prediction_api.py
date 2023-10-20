from flask import Flask, request
from flask_cors import CORS
import mlflow
from pyspark.sql import SparkSession
import delta
import pandas as pd

#load dataset,select from delta lakehouse
def get_delta_spark() -> SparkSession:
    # set spark configurations
    builder = (
        SparkSession.builder.appName("MachineLearning")
        .config("spark.jars.packages", "io.delta:delta-core_2.12:2.2.0")
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
        .config("spark.sql.warehouse.dir", "/Users/jamesoujamesou/Downloads/sit_thesis/IT819/implementation/machine_learning/Mlflow-Diabetes-Prediction-Pipeline/databases")
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
        .config("spark.mlflow.trackingUri", "http://localhost:5000")
        .config("spark.jars.repositories","https://maven-central.storage-download.googleapis.com/maven2/")
    )
    # get spark engine
    spark = delta.configure_spark_with_delta_pip(builder).master("local[*]")\
        .enableHiveSupport()\
        .getOrCreate()
    spark.sparkContext.setLogLevel("ERROR")
    return spark

def initiate_model():
    print("initiate model information")
    with get_delta_spark() as spark:
        #load dataset,select from delta lakehouse
        df = spark.sql("select model_id,model_name, model_allcolumns,"
                    "model_features,ml_experiment,mlflow_url "
                    "from machine_learning.auto_model where model_name='Random_Forest' "
                    "order by create_timestamp desc limit 1").toPandas()
        model_id = df.loc[0, 'model_id']
        model_name = df.loc[0, 'model_name']
        ml_experiment = df.loc[0, 'ml_experiment']
        mlflow_url = df.loc[0, 'mlflow_url']
        print(model_id) 
        print(model_name) 
        print(ml_experiment) 
        print(mlflow_url)
        #declare global variable for all flask request
        global model_allcolumns 
        model_allcolumns = df.loc[0, 'model_allcolumns'].split(',')
        print(model_allcolumns)
        global model_features 
        model_features = df.loc[0, 'model_features'].split(',')
        print(model_features)
        mlflow.set_experiment(ml_experiment)
        mlflow.set_tracking_uri(mlflow_url) 
        # Actual Server URI instead of localhost
        # load model
        # dynamically get model file from DB
        logged_model = 'runs:/'+model_id+'/'+model_name
        # Load model as a PyFuncModel.
        global loaded_model
        loaded_model = mlflow.pyfunc.load_model(logged_model)
# api
app = Flask(__name__)
# fix cross domain issue
CORS(app)
#initiate the global model
initiate_model()

# API that returns prediction result in JSON
@app.route('/diabetes_predict', methods=['POST'])
def diabetes_predict():
    print("access diabetes_predict method")
    '''
    Collect some data from internet
    Hypertension: Prevalence in females aged 35-44: 10.8%, So hypertension is 0
    Heart disease: Prevalence in females aged 35-44: 1.1%, So heart_disease is 0
    BMI:    Normal BMI for females aged 35-44: 18.5-24.9
            Overweight BMI for females aged 35-44: 25-29.9    
            Obese BMI for females aged 35-44: 30 or greater  30
    HbA1c level:  Normal HbA1c level for females aged 35-44: 4.8-5.6%     
            Prediabetes HbA1c level for females aged 35-44: 5.7-6.4%
            Diabetes HbA1c level for females aged 35-44: 6.5% or greater  6.5
    blood glucose level:  Normal blood glucose level for females aged 35-44: 70-99 mg/dL
                          Prediabetes blood glucose level for females aged 35-44: 100-125 mg/dL
                          Diabetes blood glucose level for females aged 35-44: 126 mg/dL or greater 126
    '''
    json_data = request.get_json()
    print(json_data)
    df = cover_input_data(json_data)
    print(df)
    result = loaded_model.predict(df)[0]
    json_data[0]['diabetes_predict'] = result
    print(json_data)
    return str(result)

def cover_input_data(json_data):
    df = pd.DataFrame.from_dict(json_data)
    # enumerate type is encoded from string to 0,1
    df_encoded = pd.get_dummies(df, columns=['gender', 'smoking_history'])
    print(model_allcolumns)

    # features have the same order with fit,get data from delta lakehouse
    columns = model_allcolumns 
    # to fix the bug 'The feature names should match those that were passed during fit.' copy encoded df to sorted df
    df_encoded_sorted = pd.DataFrame([[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]],columns=columns)
    # print(df_encoded_sorted['gender_Female'])
    set_value_to_sorted_dataframe(df_encoded,columns,df_encoded_sorted)
    print(model_features)
    # cast type to int
    columns = model_features
    df_encoded_sorted[columns] = df_encoded_sorted[columns].astype(int)
    # print(df_encoded_sorted['gender_Female'])
    return df_encoded_sorted

def set_value_to_sorted_dataframe(df,columns,df_sorted):
    #reset the value to sorted dataframe
    for name in columns:
        if name in df.columns:
            print('The column '+name+' exists in the DataFrame.')
            df_sorted[name]=df[name]

if __name__ == "__main__":
    #set the port=8000
    #set use_reloader=False to improve performance and reduce multiple loading
    app.run(port=8000,debug=True,use_reloader=False)