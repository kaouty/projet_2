import pandas as pd
import numpy as np 
import pickle
import base64
import uvicorn

from typing import List, Optional
from pydantic import BaseModel

from fastapi import FastAPI, Request


users_db = [
    {
        'user_id': 1,
        'username': 'alice',
        'password': 'd29uZGVybGFuZA=='
    },
    {
        'user_id': 2,
        'username': 'bob',
        'password': 'YnVpbGRlcg=='
    },
    {
        'user_id': 3,
        'username': 'clementine',
        'password': 'bWFuZGFyaW5l'
    }
]

class Client(BaseModel):
    gender: str
    SeniorCitizen: int
    Partner: Optional[str] = None
    Dependents: str
    tenure: Optional[int] = None
    PhoneService: str
    MultipleLines: Optional[str] = None
    InternetService: str
    OnlineSecurity: Optional[str] = None
    OnlineBackup: Optional[str] = None
    DeviceProtection: Optional[str] = None
    TechSupport: Optional[str] = None
    StreamingTV: Optional[str] = None
    StreamingMovies: Optional[str] = None
    Contract: str
    PaperlessBilling: Optional[str] = None
    PaymentMethod: Optional[str] = None
    MonthlyCharges: float
    TotalCharges: Optional[float] = None


api = FastAPI(
    title='Churn API'
)

@api.get('/status')
async def get_status():
    """Returns 1
    """
    return 1


@api.get('/identification/{username}/{password}')
def get_identification(username, password):
    """Returns l'identification d'utilisateur :
        user_status == 1: identifié
        user_status == 0: non identifié
    """
    password_base64 = base64.standard_b64encode(password.encode()).decode('ascii')
    #return password_base64
    users = list(filter(lambda x: x.get('username') == username and x.get('password') == password_base64, users_db))

    if len(users) > 0:
        # l'utilisateur est identifié
        return {'user_status': 1}
    else:
        # l'utilisateur n'est pas identifié
        return {'user_status': 0}


@api.post('/predict/{model}')
def get_predict(model:str, username:str, password:str, client: Client):
    output = {}

    user = get_identification(username, password)

    if user['user_status'] == 0:
        output = {'user_status': 'Incorrect username or password'}
        return output

    tenure = client.tenure
    MonthlyCharges = client.MonthlyCharges
    TotalCharges = client.TotalCharges

    gender_Female = 1 if client.gender == 'Female' else 0
    gender_Male = 1 if client.gender == 'Male' else 0

    SeniorCitizen_0 = 1 if client.SeniorCitizen == 0 else 0
    SeniorCitizen_1 = 1 if client.SeniorCitizen == 1 else 0

    Partner_No = 1 if client.Partner == 'No' else 0
    Partner_Yes = 1 if client.Partner == 'Yes' else 0

    Dependents_No = 1 if client.Dependents == 'No' else 0
    Dependents_Yes = 1 if client.Dependents == 'Yes' else 0

    PhoneService_No = 1 if client.PhoneService == 'No' else 0
    PhoneService_Yes = 1 if client.PhoneService == 'Yes' else 0

    MultipleLines_No = 1 if client.MultipleLines == 'No' else 0
    MultipleLines_Nophoneservice = 1 if client.MultipleLines == 'No phone service' else 0
    MultipleLines_Yes = 1 if client.MultipleLines == 'Yes' else 0

    InternetService_DSL = 1 if client.InternetService == 'DSL' else 0
    InternetService_Fiberoptic = 1 if client.InternetService == 'Fiber optic' else 0
    InternetService_No = 1 if client.InternetService == 'No' else 0

    OnlineSecurity_No = 1 if client.OnlineSecurity == 'No' else 0
    OnlineSecurity_Nointernetservice = 1 if client.OnlineSecurity == 'No internet service' else 0
    OnlineSecurity_Yes = 1 if client.OnlineSecurity == 'Yes' else 0

    OnlineBackup_No = 1 if client.OnlineBackup == 'No' else 0
    OnlineBackup_Nointernetservice = 1 if client.OnlineBackup == 'No internet service' else 0
    OnlineBackup_Yes = 1 if client.OnlineBackup == 'Yes' else 0

    DeviceProtection_No = 1 if client.DeviceProtection == 'No' else 0
    DeviceProtection_Nointernetservice = 1 if client.DeviceProtection == 'No internet service' else 0
    DeviceProtection_Yes = 1 if client.DeviceProtection == 'Yes' else 0

    TechSupport_No = 1 if client.TechSupport == 'No' else 0
    TechSupport_Nointernetservice = 1 if client.TechSupport == 'No internet service' else 0
    TechSupport_Yes = 1 if client.TechSupport == 'Yes' else 0

    StreamingTV_No = 1 if client.StreamingTV == 'No' else 0
    StreamingTV_Nointernetservice = 1 if client.StreamingTV == 'No internet service' else 0
    StreamingTV_Yes = 1 if client.StreamingTV == 'Yes' else 0

    StreamingMovies_No = 1 if client.StreamingMovies == 'No' else 0
    StreamingMovies_Nointernetservice = 1 if client.StreamingMovies == 'No internet service' else 0
    StreamingMovies_Yes = 1 if client.StreamingMovies == 'Yes' else 0

    Contract_Monthtomonth = 1 if client.Contract == 'Month-to-month' else 0
    Contract_Oneyear = 1 if client.Contract == 'One year' else 0
    Contract_Twoyear = 1 if client.Contract == 'Two year' else 0

    PaperlessBilling_No = 1 if client.PaperlessBilling == 'No' else 0
    PaperlessBilling_Yes = 1 if client.PaperlessBilling == 'Yes' else 0

    PaymentMethod_Banktransfer = 1 if client.PaymentMethod == 'Bank transfer (automatic)' else 0
    PaymentMethod_Creditcard = 1 if client.PaymentMethod == 'Credit card (automatic)' else 0
    PaymentMethod_Electroniccheck = 1 if client.PaymentMethod == 'Electronic check' else 0
    PaymentMethod_Mailedcheck = 1 if client.PaymentMethod == 'Mailed check' else 0

    features = [tenure,
               MonthlyCharges,
               TotalCharges,
               gender_Female,
               gender_Male,
               SeniorCitizen_0,
               SeniorCitizen_1,
               Partner_No,
               Partner_Yes,
               Dependents_No,
               Dependents_Yes,
               PhoneService_No,
               PhoneService_Yes,
               MultipleLines_No,
               MultipleLines_Nophoneservice,
               MultipleLines_Yes,
               InternetService_DSL,
               InternetService_Fiberoptic,
               InternetService_No,
               OnlineSecurity_No,
               OnlineSecurity_Nointernetservice,
               OnlineSecurity_Yes,
               OnlineBackup_No,
               OnlineBackup_Nointernetservice,
               OnlineBackup_Yes,
               DeviceProtection_No,
               DeviceProtection_Nointernetservice,
               DeviceProtection_Yes,
               TechSupport_No,
               TechSupport_Nointernetservice,
               TechSupport_Yes,
               StreamingTV_No,
               StreamingTV_Nointernetservice,
               StreamingTV_Yes,
               StreamingMovies_No,
               StreamingMovies_Nointernetservice,
               StreamingMovies_Yes,
               Contract_Monthtomonth,
               Contract_Oneyear,
               Contract_Twoyear,
               PaperlessBilling_No,
               PaperlessBilling_Yes,
               PaymentMethod_Banktransfer,
               PaymentMethod_Creditcard,
               PaymentMethod_Electroniccheck,
               PaymentMethod_Mailedcheck]

    columns = ['tenure',
               'MonthlyCharges',
               'TotalCharges',
               'gender_Female',
               'gender_Male',
               'SeniorCitizen_0',
               'SeniorCitizen_1',
               'Partner_No',
               'Partner_Yes',
               'Dependents_No',
               'Dependents_Yes',
               'PhoneService_No',
               'PhoneService_Yes',
               'MultipleLines_No',
               'MultipleLines_No phone service',
               'MultipleLines_Yes',
               'InternetService_DSL',
               'InternetService_Fiber optic',
               'InternetService_No',
               'OnlineSecurity_No',
               'OnlineSecurity_No internet service',
               'OnlineSecurity_Yes',
               'OnlineBackup_No',
               'OnlineBackup_No internet service',
               'OnlineBackup_Yes',
               'DeviceProtection_No',
               'DeviceProtection_No internet service',
               'DeviceProtection_Yes',
               'TechSupport_No',
               'TechSupport_No internet service',
               'TechSupport_Yes',
               'StreamingTV_No',
               'StreamingTV_No internet service',
               'StreamingTV_Yes',
               'StreamingMovies_No',
               'StreamingMovies_No internet service',
               'StreamingMovies_Yes',
               'Contract_Month-to-month',
               'Contract_One year',
               'Contract_Two year',
               'PaperlessBilling_No',
               'PaperlessBilling_Yes',
               'PaymentMethod_Bank transfer (automatic)',
               'PaymentMethod_Credit card (automatic)',
               'PaymentMethod_Electronic check',
               'PaymentMethod_Mailed check']

    final_features = [np.array(features)]

    if model == 'logreg':
        model_ml = pickle.load(open('model_logreg.pkl', 'rb'))

    elif model == 'knn':
        model_ml = pickle.load(open('model_knn.pkl', 'rb'))

    elif model == 'dtree':
        model_ml = pickle.load(open('model_dtree.pkl', 'rb'))

    if model_ml:
        prediction = model_ml.predict(final_features)
        output = {'churn': prediction[0]}

    """ TEST :
    curl -X 'POST' \
      'http://127.0.0.1:8000/predict/logreg?username=alice&password=wonderland' \
      -H 'accept: application/json' \
      -H 'Content-Type: application/json' \
      -d '{
      "gender": "Female",
      "SeniorCitizen": 1,
      "Partner": "No",
      "Dependents": "Yes",
      "tenure": 14,
      "PhoneService": "No",
      "MultipleLines": "No",
      "InternetService": "No",
      "OnlineSecurity": "No",
      "OnlineBackup": "No",
      "DeviceProtection": "No",
      "TechSupport": "No",
      "StreamingTV": "No",
      "StreamingMovies": "No",
      "Contract": "Month-to-month",
      "PaperlessBilling": "Yes",
      "PaymentMethod": "Credit card (automatic)",
      "MonthlyCharges": 58.99,
      "TotalCharges": 789.9
    }'
    RESULTAT: 
    [
      "No"
    ]
    """

    return output
if __name__ == '__main__':
    uvicorn.run(api, host='127.0.0.1', port=8000, debug=True)


