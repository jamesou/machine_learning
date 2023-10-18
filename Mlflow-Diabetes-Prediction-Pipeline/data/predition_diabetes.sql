CREATE database machine_learning;

CREATE TABLE machine_learning.patient (
    id STRING,
    gender STRING, 
    age STRING
) USING DELTA;

CREATE TABLE machine_learning.diagnosis (
    id STRING,
    hypertension STRING,
    heart_disease STRING,
    diabetes STRING
) USING DELTA;

CREATE TABLE machine_learning.lifestyle (
    id STRING,
    smoking_history STRING,
    bmi STRING
) USING DELTA;

CREATE TABLE machine_learning.blood_glucose (
    id STRING,
    HbA1c_level STRING,
    blood_glucose_level STRING
) USING DELTA;
--TODO initialise the model info
CREATE TABLE machine_learning.auto_model (
    model_id STRING,
    model_name STRING,
    model_params STRING,
    model_allcolumns STRING,
    model_features STRING,
    ml_experiment STRING,
    mlflow_url STRING,
    create_timestamp timestamp
) USING DELTA;

Delete from auto_model;
Insert into auto_model values('3c2ee0f8d34a401b9a77e707b5c36741','Random_Forest','{"criterion":"entropy","max_depth":1000,"max_features":"sqrt","min_samples_leaf":4,"min_samples_split":5,"n_estimators":600,"n_jobs":-1,"random_state":42}','age,hypertension,heart_disease,bmi,HbA1c_level,blood_glucose_level,gender_Female,gender_Male,gender_Other,smoking_history_No Info,smoking_history_current,smoking_history_ever,smoking_history_former,smoking_history_never,smoking_history_not current','gender_Female,gender_Male,gender_Other,smoking_history_No Info,smoking_history_current,smoking_history_ever,smoking_history_former,smoking_history_never,smoking_history_not current','diabetes_prediction','http://localhost:5000/',CURRENT_TIMESTAMP());
Insert into auto_model values('6f3568cd9b8e483d8ee6c82fb20859cf','Random_Forest','{"criterion":"entropy","max_depth":1000,"max_features":"sqrt","min_samples_leaf":4,"min_samples_split":5,"n_estimators":600,"n_jobs":-1,"random_state":42}','age,hypertension,heart_disease,bmi,HbA1c_level,blood_glucose_level,gender_Female,gender_Male,gender_Other,smoking_history_No Info,smoking_history_current,smoking_history_ever,smoking_history_former,smoking_history_never,smoking_history_not current','gender_Female,gender_Male,gender_Other,smoking_history_No Info,smoking_history_current,smoking_history_ever,smoking_history_former,smoking_history_never,smoking_history_not current','diabetes_prediction','http://localhost:5000/',CURRENT_TIMESTAMP());
Insert into auto_model values('4bca4b7d08dd4449a42e50fea0817653','K_Nearest_Neighbors','','age,hypertension,heart_disease,bmi,HbA1c_level,blood_glucose_level,gender_Female,gender_Male,gender_Other,smoking_history_No Info,smoking_history_current,smoking_history_ever,smoking_history_former,smoking_history_never,smoking_history_not current','gender_Female,gender_Male,gender_Other,smoking_history_No Info,smoking_history_current,smoking_history_ever,smoking_history_former,smoking_history_never,smoking_history_not current','diabetes_prediction','http://localhost:5000/',CURRENT_TIMESTAMP());
Insert into auto_model values('23a0cad928314effb6b4e1f4c9a424fc','SVM','','age,hypertension,heart_disease,bmi,HbA1c_level,blood_glucose_level,gender_Female,gender_Male,gender_Other,smoking_history_No Info,smoking_history_current,smoking_history_ever,smoking_history_former,smoking_history_never,smoking_history_not current','gender_Female,gender_Male,gender_Other,smoking_history_No Info,smoking_history_current,smoking_history_ever,smoking_history_former,smoking_history_never,smoking_history_not current','diabetes_prediction','http://localhost:5000/',CURRENT_TIMESTAMP());
Insert into auto_model values('4db1c748277148a78d2b50faf8af35cb','Logistic_Regression','','age,hypertension,heart_disease,bmi,HbA1c_level,blood_glucose_level,gender_Female,gender_Male,gender_Other,smoking_history_No Info,smoking_history_current,smoking_history_ever,smoking_history_former,smoking_history_never,smoking_history_not current','gender_Female,gender_Male,gender_Other,smoking_history_No Info,smoking_history_current,smoking_history_ever,smoking_history_former,smoking_history_never,smoking_history_not current','diabetes_prediction','http://localhost:5000/',CURRENT_TIMESTAMP());


select p.id,p.gender,p.age,d.hypertension,d.heart_disease,
l.smoking_history,l.bmi,b.HbA1c_level,b.blood_glucose_level,d.diabetes from patient p
left join diagnosis d on p.id = d.id
left join lifestyle l on p.id = l.id
left join blood_glucose b on p.id = b.id limit 10
