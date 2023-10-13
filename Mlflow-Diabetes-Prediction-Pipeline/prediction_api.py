import json
from flask import Flask, request,jsonify
from flask_cors import CORS
import mlflow
import pandas as pd

#TODO Parameterised constant
mlflow.set_experiment('diabetes_prediction')
mlflow.set_tracking_uri("http://localhost:5000/") # Actual Server URI instead of localhost
# load model
# todo dynamically get model file from DB
logged_model = 'runs:/6f3568cd9b8e483d8ee6c82fb20859cf/Random_Forest'
# Load model as a PyFuncModel.
loaded_model = mlflow.pyfunc.load_model(logged_model)
# api
app = Flask(__name__)
CORS(app)
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
    df_encoded = pd.get_dummies(df, columns=['gender', 'smoking_history'])
    columns = ['age', 'hypertension', 'heart_disease', 'bmi',
    'HbA1c_level', 'blood_glucose_level', 'gender_Female',
    'gender_Male', 'gender_Other',
    'smoking_history_No Info', 'smoking_history_current',
    'smoking_history_ever', 'smoking_history_former', 'smoking_history_never',
    'smoking_history_not current'] #features have the same order with fit
    # to fix the bug 'The feature names should match those that were passed during fit.' copy encoded df to sorted df
    df_encoded_sorted = pd.DataFrame([[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]],columns=columns)
    # print(df_encoded_sorted['gender_Female'])
    set_value_to_sorted_dataframe(df_encoded,columns,df_encoded_sorted)
    # cast type to int
    columns = ['gender_Female', 'gender_Male',
               'gender_Other', 'smoking_history_No Info', 'smoking_history_current',
               'smoking_history_ever', 'smoking_history_former',
               'smoking_history_never', 'smoking_history_not current']
    df_encoded_sorted[columns] = df_encoded_sorted[columns].astype(int)
    # print(df_encoded_sorted['gender_Female'])
    return df_encoded_sorted

def set_value_to_sorted_dataframe(df,columns,df_sorted):
    for name in columns:
        if name in df.columns:
            print('The column '+name+' exists in the DataFrame.')
            df_sorted[name]=df[name]

if __name__ == "__main__":
    app.run(port=8000,debug=True)