#!/usr/bin/python
#-*- coding:utf-8 -*-
import re
import time
from datetime import datetime, timezone
import pandas as pd
import requests
import json

from example_data import *


class hackathon_api:
    #__api_path = "https://crypticorn-api.herokuapp.com/"
    __api_path = "http://127.0.0.1:5000/"


    def post_initialize_vitalsTypes(self):

        response = requests.post(
            self.__api_path + 'post_initialize_vitalsTypes',
            #headers={'Authorization': "Bearer " + self.__access_token},
            # json={
            #    "are_you_sure": are_you_sure
            # }
        )
        return json.loads(response.content)['status']

    def post_initialize_rooms(self, rooms_dict):

        response = requests.post(
            self.__api_path + 'post_initialize_rooms',
            #headers={'Authorization': "Bearer " + self.__access_token},
            json={
                "rooms_dict": rooms_dict
            }
        )
        return json.loads(response.content)['status']

    def post_new_patient(self, patient_dict):

        response = requests.post(
            self.__api_path + 'post_new_patient',
            #headers={'Authorization': "Bearer " + self.__access_token},
            json={
                "patient_dict": patient_dict
            }
        )
        return json.loads(response.content)['status']

    def post_new_employee(self, employee):

        response = requests.post(
            self.__api_path + 'post_new_employee',
            #headers={'Authorization': "Bearer " + self.__access_token},
            json={
               "employee": employee
            }
        )
        return json.loads(response.content)['status']

    def post_new_prescriptions(self, prescriptions_dict):

        response = requests.post(
            self.__api_path + 'post_new_prescriptions',
            #headers={'Authorization': "Bearer " + self.__access_token},
            json={
               "prescriptions_dict": prescriptions_dict
            }
        )
        return json.loads(response.content)['status']

    def post_new_patientRequest(self, patientRequest_dict):

        response = requests.post(
            self.__api_path + 'post_new_patientRequest',
            #headers={'Authorization': "Bearer " + self.__access_token},
            json={
                "patientRequest_dict": patientRequest_dict
             }
        )
        return json.loads(response.content)['status']

    def post_update_medication(self, medication_dict):

        response = requests.post(
            self.__api_path + 'post_update_medication',
            #headers={'Authorization': "Bearer " + self.__access_token},
            json={
               "medication_dict": medication_dict
            }
        )
        return json.loads(response.content)['status']

    def post_update_vitals(self, vitals_dict):

        response = requests.post(
            self.__api_path + 'post_update_vitals',
            #headers={'Authorization': "Bearer " + self.__access_token},
            json={
               "vitals_dict": vitals_dict
            }
        )
        return json.loads(response.content)['status']

    def post_update_patientcondition(self, patientcondition_dict):

        response = requests.post(
            self.__api_path + 'post_update_patientcondition',
            #headers={'Authorization': "Bearer " + self.__access_token},
            json={
                "patientcondition_dict": patientcondition_dict
            }
        )
        return json.loads(response.content)['status']

    def post_update_roomConditions(self, roomConditions_dict):

        response = requests.post(
            self.__api_path + 'post_update_roomConditions',
            #headers={'Authorization': "Bearer " + self.__access_token},
            json={
               "roomConditions_dict": roomConditions_dict
            }
        )
        return json.loads(response.content)['status']


if __name__ == '__main__':

    api = hackathon_api()
    #api.post_initialize_vitalsTypes()
    #api.post_new_patient(patient_dict)
    #api.post_new_patientRequest(patientRequest_dict)
    #api.post_update_vitals(vitals_dict)
    #api.post_update_patientcondition(patientcondition_dict)
    #api.post_new_prescriptions(prescriptions_dict)
    #api.post_update_medication(medication_dict)
    api.post_initialize_rooms(room_dict)
    api.post_update_roomConditions(roomConditions_dict)
    print()