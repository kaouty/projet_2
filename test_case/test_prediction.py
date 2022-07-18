
import os
from main import api
from unittest import result
import requests
import json
# définition de l'adresse de l'API
api_address = '127.0.0.1'
# port de l'API
api_port = 8000
# requêtes pour alice v1
r = requests.post(
    url='http://{address}:{port}/predict/logreg?username=alice&password=wonderland'.format(address=api_address, port=api_port),
    headers= {
        'accept': 'application/json',
        'Content-Type': 'application/json'
        },
    json = {
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

)
output = '''
============================
       Model1 test
============================
request done at "/predict1"
| username="bob"
| password="builder"
expected result = Rain tomorrow
actual result = {test_result}
==> {test_status}
'''
# reponse en json
data = r.json()
status_code  = r.status_code
# affichage des résultats
if status_code == 200:
    test_status = 'SUCCESS'
else:
    test_status = 'FAILURE'

assert data ==  {"churn": "No"}
#print(output.format(test_result=test_result, test_status=test_status))