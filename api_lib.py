#!/usr/bin/python
#-*- coding:utf-8 -*-
import requests
import json


class hackathon_api:
    # Link to the deployed API on heroku Server
    __api_path = "https://hackathon2022fulda.herokuapp.com/"
    # Link to to a local running API
    #__api_path = "http://127.0.0.1:5000/"


    def post_initialize_vitalsTypes(self):
        '''
        Initialze the constant vitalsTypes table.
        :return: api response status code
        '''

        response = requests.post(
            self.__api_path + 'post_initialize_vitalsTypes',
        )
        return json.loads(response.content)['status']

    def post_initialize_rooms(self, rooms_dict):
        '''
        Initialize a new constant room in the facility.
        :param rooms_dict: special configured dictionary for this api endpoint
        :return: api response status code
        '''

        response = requests.post(
            self.__api_path + 'post_initialize_rooms',
            json={
                "rooms_dict": rooms_dict
            }
        )
        return json.loads(response.content)['status']

    def post_new_patient(self, patient_dict):
        """
        Adds new partient.
        :param rooms_dict: special configured dictionary for this api endpoint
        :return: api response status code
        """

        response = requests.post(
            self.__api_path + 'post_new_patient',
            json={
                "patient_dict": patient_dict
            }
        )
        return json.loads(response.content)['status']

    def post_new_employee(self, employee_dict):
        """
        Adds an employee, at the beginning of his/her work sift.
        :param employee_dict: special configured dictionary for this api endpoint
        :return: api response status code
        """

        response = requests.post(
            self.__api_path + 'post_new_employee',
            #headers={'Authorization': "Bearer " + self.__access_token},
            json={
               "employee": employee_dict
            }
        )
        return json.loads(response.content)['status']

    def post_new_prescriptions(self, prescriptions_dict):
        """
        Adds new prescriptions from the doc.
        :param rooms_dict: special configured dictionary for this api endpoint
        :return: api response status code
        """

        response = requests.post(
            self.__api_path + 'post_new_prescriptions',
            json={
               "rooms_dict": prescriptions_dict
            }
        )
        return json.loads(response.content)['status']

    def post_new_patientRequest(self, patientRequest_dict):
        """
        Adds new request from the partient to AI Anna or the employees.
        :param patientRequest_dict: special configured dictionary for this api endpoint
        :return: api response status code
        """

        response = requests.post(
            self.__api_path + 'post_new_patientRequest',
            json={
                "patientRequest_dict": patientRequest_dict
             }
        )
        return json.loads(response.content)['status']

    def post_update_medication(self, medication_dict):
        """
        If the patien gets medication, this function will be called
        :param medication_dict: special configured dictionary for this api endpoint
        :return: api response status code
        """

        response = requests.post(
            self.__api_path + 'post_update_medication',
            json={
               "medication_dict": medication_dict
            }
        )
        return json.loads(response.content)['status']

    def post_update_vitals(self, vitals_dict):
        """
        Update the vitals from speech or from meassurement devices.
        :param vitals_dict: special configured dictionary for this api endpoint
        :return: api response status code
        """

        response = requests.post(
            self.__api_path + 'post_update_vitals',
            json={
               "vitals_dict": vitals_dict
            }
        )
        return json.loads(response.content)['status']

    def post_update_patientcondition(self, patientcondition_dict):
        """
        Only text based information.
        :param patientcondition_dict: special configured dictionary for this api endpoint
        :return: api response status code
        """

        response = requests.post(
            self.__api_path + 'post_update_patientcondition',
            json={
                "patientcondition_dict": patientcondition_dict
            }
        )
        return json.loads(response.content)['status']

    def post_update_roomConditions(self, roomConditions_dict):
        """
        Updates room Conditions from measurement devices
        :param roomConditions_dict: special configured dictionary for this api endpoint
        :return: api response status code
        """

        response = requests.post(
            self.__api_path + 'post_update_roomConditions',
            json={
               "roomConditions_dict": roomConditions_dict
            }
        )
        return json.loads(response.content)['status']


if __name__ == '__main__':

    # Example Usage
    api = hackathon_api()
    api.post_initialize_vitalsTypes()
    #api.post_new_patient({
    #'psName': 'Mohr',
    #'pfName': 'Moritz',
    #'birthdate': '31.09.1967',
    #'bloodtype': 'A-',
    #'sex': 'männlich',
    #'roomID': '1',
    #'allergies': 'Pollen',
    #'startdate': '30.09.2022',
    #'enddate': '',
    #'insurancecard': 'Techniker Krankenkasse',
    #'pflegegrad': '3',
    #'doctor': 'Dr. Röhr',
    #'contacts': '+49 178 9824590323\nPalmenweg 23a\n48463 Grähburg',
    #'notes': '',
    #})
    print('Done')