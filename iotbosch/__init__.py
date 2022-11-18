import logging
import json
import re
import azure.functions as func
from urllib.parse import urlencode
from urllib.request import Request, urlopen
import requests

def remove_empty_elements(d):
    """recursively remove empty lists, empty dicts, or None elements from a dictionary"""

    def empty(x):
        return x is None or x == {} or x == []

    if not isinstance(d, (dict, list)):
        return d
    elif isinstance(d, list):
        return [v for v in (remove_empty_elements(v) for v in d) if not empty(v)]
    else:
        return {k: v for k, v in ((k, remove_empty_elements(v)) for k, v in d.items()) if not empty(v)}

def change_payload(payload):
    """takes given data and converts it to needed format"""
    response = {}
    response["device"] = {"deviceId" : payload["assets"][0]["trackingDeviceId"], "modelId": "dtmi:iotDemo02:AssetTrackingTelemetryData_5yj;1"}
    # "dtmi:iotDemo02:AssetTrackingTelemetryData_5yj;1"
  #  response["measurements"] = payload
  #  response["measurements"] ={"timestamp" : payload["assets"][0]["measurements"][0]["timestamp"], 
  #                             "Tracking" : {"lon" : payload["assets"][0]["measurements"][0]["geoLocation"]["longitude"],
  #                                              "lat" : payload["assets"][0]["measurements"][0]["geoLocation"]["latitude"],
  #                                              "alt" : payload["assets"][0]["measurements"][0]["geoLocation"]["altitude"]}, 
  #                             "ITemp" : payload["assets"][0]["measurements"][0]["temperature"]["value"]}
    response["measurements"] ={"Tracking" : {"lon" : payload["assets"][0]["measurements"][0]["geoLocation"]["longitude"],
                                             "lat" : payload["assets"][0]["measurements"][0]["geoLocation"]["latitude"],
                                             "alt" : payload["assets"][0]["measurements"][0]["geoLocation"]["altitude"]}, 
                               "ITemp" : payload["assets"][0]["measurements"][0]["temperature"]["value"]}
    return response


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    req_body = req.get_json()
    req_body = remove_empty_elements(req_body)
    req_body = change_payload(req_body)

    data = json.dumps(req_body)
    logging.info(data)


    url = 'https://iotc-fnt7byip75uxp7w.azurewebsites.net/api/IoTCIntegration?code=_WEFn2E9rBHnWxZGr0h5q99nJzHXs1YRYq5nY692tpV_AzFu6oT3oQ==' # Set destination URL here


    header = {"Content-type": "application/json",
            "Accept": "text/plain"} 

    response_decoded_json = requests.post(url, data=json.dumps(req_body), headers=header)
    logging.info(response_decoded_json.status_code)

    if response_decoded_json.status_code != 200:
        return func.HttpResponse(f"Error malformed data",status_code=500) 
    else:
        return func.HttpResponse(
             f"{data}",
             status_code=200
        )
