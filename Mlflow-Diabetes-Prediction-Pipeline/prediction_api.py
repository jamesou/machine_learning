import json
from flask import Flask, request,jsonify
import mlflow
import pandas as pd

mlflow.set_experiment('diabetes_prediction')
mlflow.set_tracking_uri("http://localhost:5000/") # Actual Server URI instead of localhost
# load model
# todo dynamically get model file from DB
logged_model = 'runs:/af15394323534cac9f0ce983c736e88e/Random_Forest'
# Load model as a PyFuncModel.
loaded_model = mlflow.pyfunc.load_model(logged_model)
# api
app = Flask(__name__)

# functions
@app.route('/diabetes_predict', methods=['POST'])
def diabetes_predict():
    '''
    API that returns prediction result in JSON
    Returns:
        json_result
    '''
    print("access diabetes_predict method")
    # turple_data = {"age": 39, "hypertension": 1, "heart_disease": 0, "bmi": 79, "HbA1c_level": 8.8,
    #              "blood_glucose_level": 145, "gender_Female": 1, "gender_Male": 0, "gender_Other": 0,
    #              "smoking_history_No Info": 1, "smoking_history_current": 0, "smoking_history_ever": 0,
    #              "smoking_history_former": 0, "smoking_history_never": 0, "smoking_history_not current": 0},
    # dict_data = {'gender': 'Female', 'age': 39, 'hypertension': 1, 'heart_disease': 0, 'smoking_history': 'No Info',
    #              'bmi': 79, 'HbA1c_level': 8.8, 'blood_glucose_level': 145},
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
    json_data[0]['diabetes_predict'] = loaded_model.predict(df)[0]
    #todo 3.design a web page for patient to use this functionality
    return str(json_data)

def cover_input_data(json_data):
    #todo 1.select patient's info from db(Data Lakehouse) accroding to name，2.get features from table
    #Q1: Do i need to design webpage? Q2: Do i need to use Pyspark as calculate engine(It mentioned by paper)
    #Q3: Should I save these data(feature data,patience data etc) into DB or Data Lakehosue?
    #    If yes, Do I use my mac pc to install lakehouse? Is there free platform for student research?
    df = pd.DataFrame.from_dict(json_data)
    df_encoded = pd.get_dummies(df, columns=['gender', 'smoking_history'])
    columns = ['gender_Female', 'gender_Male',
       'gender_Other', 'smoking_history_No Info', 'smoking_history_current',
       'smoking_history_ever', 'smoking_history_former',
       'smoking_history_never', 'smoking_history_not current']
    for column in columns:
        add_column_to_dataframe(df_encoded, column)
    # cast type to int
    # print(df_encoded['gender_Female'])
    df_encoded[columns] = df_encoded[columns].astype(int)
    # print(df_encoded['gender_Female'])
    return df_encoded

def add_column_to_dataframe(df,name):
    if name in df.columns:
        print('The column '+name+' exists in the DataFrame.')
    else:
        print('The column '+name+' does not exist in the DataFrame.')
        df[name]=0

if __name__ == "__main__":
    app.run(port=8000,debug=True)