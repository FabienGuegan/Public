# Overview

The Hazel and Bazel Hospital, in Los Angeles, California, has contacted us regarding suspicion of malpractice and is currently under investigation by the Fair Medical Practices Bureau. Situations have come to light where patients have been wrongfully medically discharged, resulting in severe health consequences for the patient. Our main objective is to identify patients who are likely to return to the hospital in less than 30 days, for which the hospital might be liable for wrongful discharge before due time.  

The reasons for this are still unknown, and investigation into this matter is required. It is unknown if this is a demographic-specific issue or specific to any of the medical specialities/services. Additionally, they want us to create and deploy a REST API endpoint for patient discharge verification. This will be integrated directly into the hospital’s system to be triggered every time the medical dismissal information for a patient is filled in in their system. You will be responsible for setting this system up and running it for a year.	

They ask you to provide a service that they can call, with two endpoints. 
- Predict: to which they will send requests for new predictions
- Update: to which they will send the actual information if a person should or should not have been discharged

The hospital staff will use those endpoints to do several rounds of tests and pick the first 10 teams based on a mix of F1-score and the fairness requirement. Those teams will be called on to present their service and model.

# Objective

In this hackathon, you will tackle a binary classification problem setup in a real-world scenario. As described in the previous sections, this problem will consist of predicting, based on a number of features, if a person should or should not be discharged. Some of these features are considered sensitive - such as race and gender - and will need special attention to avoid discriminating against minorities.

You will be given an initial dataset with a number of examples. You should use this dataset to build a model, taking into account the different requirements the client posed, in particular:

- You want to maximize the percentage of correct predictions
- Your model should not yield differences among gender or race as measured by the difference in the above metric by more than 0.15

The dataset contains the following fields. The field that you must use as outcome is:
- readmitted


With this in mind, you should set up a server that serves this model, with two endpoints, described below:

Endpoint
POST /predict

Expected payload (input)

{"admission_id": 82679, "patient_id": 81317898, "race": "Caucasian", "gender": "Male", "age": NaN, "weight": "?", "admission_type_code": 3.0, "discharge_disposition_code": 3.0, "admission_source_code": 1, "time_in_hospital": 7, "payer_code": "MC", "medical_specialty": "Family/GeneralPractice", "has_prosthesis": false, "complete_vaccination_status": "Complete", "num_lab_procedures": 44.0, "num_procedures": 1, "num_medications": 13.0, "number_outpatient": 0, "number_emergency": 0, "number_inpatient": 2, "diag_1": "585", "diag_2": "491", "diag_3": "276", "number_diagnoses": 9, "blood_type": "O+", "hemoglobin_level": 15.6, "blood_transfusion": false, "max_glu_serum": "None", "A1Cresult": "None", "diuretics": "No", "insulin": "Yes", "change": "Ch", "diabetesMed": "Yes"}

Expected response (output)
{
   "readmitted": "Yes"
}

Endpoint
POST /update

Expected payload (input)
{"admission_id": 82679, "readmitted": "No"}

Expected response (output)
{
  "admission_id": 82679,
  "actual_readmitted": "Yes",
  "predicted_readmitted": "Yes"
}

If your application receives a request that doesn’t respect the formats defined above, it can either return an appropriate error message or ignore the request. But in any case, it should be fault-tolerant, i.e, it shouldn’t die because it received a weird request! 
A trial round of evaluation will happen, where some dummy examples will be sent for you to assert if your endpoints are working fine. By this point, you should have provided your endpoint so that it can be queried. Shortly after, there will be a first round of evaluation where your server will be queried for predictions, producing a score over the first metric. This score will show up in a leaderboard so you can see how well you are faring against other teams. 

After the predictions, a round of updates will be sent back to your update endpoint, which you should store and use as feedback. Use this second set of data to improve your model and prepare for the final round of predictions. If by any chance, you fail to store the data from the updates, the data will be sent to you in a csv. However, you will be penalized for not having your server properly set up. Finally, after you retrained and re-assessed your model, you will go through the final evaluation, where another round of evaluation will trigger several prediction requests to your server, producing a final score. 

To summarize:
- Build a model to tackle the presented problem
- Serve your model and provide a predict endpoint
- Provide an update endpoint for receiving the true values 
- Retrain your model and re-deploy for a final assessment

