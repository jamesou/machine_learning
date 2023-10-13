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
    model_file STRING,
    ml_experiment STRING,
    mlflow_url STRING
) USING DELTA;

 select * from (
    select p.id,p.gender,p.age,d.hypertension,d.heart_disease,
    l.smoking_history,l.bmi,b.HbA1c_level,b.blood_glucose_level,d.diabetes from patient p 
    left join diagnosis d on p.id = d.id
    left join lifestyle l on p.id = l.id
    left join blood_glucose b on p.id = b.id
 ) limit 10;