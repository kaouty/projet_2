import pytest
from fastapi.testclient import TestClient
from main import api
import json
import os
import pickle

client = TestClient(api)



m = {
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
    }



#tester logreg
def test_predict(client):
  #with open('/home/ubuntu/projet2/api_fast/model_logreg.pkl', 'rb') as file:
    dat = pickle.load(open('/home/ubuntu/projet2/api_fast/model_logreg.pkl', "rb"))
    response = client.post("/predict/logreg?username=bob&password=builder",files=dat,json=m)
    assert response.status_code == 200
    assert response.json() == {"churn": "No"}



