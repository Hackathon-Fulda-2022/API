# Some example data for the example usage in the api.py

from datetime import datetime

patient_dict = {
    'psName': 'Mohr',
    'pfName': 'Moritz',
    'birthdate': '31.09.1967',
    'bloodtype': 'A-',
    'sex': 'männlich',
    'roomID': '1',
    'allergies': 'Pollen',
    'startdate': '30.09.2022',
    'enddate': '',
    'insurancecard': 'Techniker Krankenkasse',
    'pflegegrad': '3',
    'doctor': 'Dr. Röhr',
    'contacts': '+49 178 9824590323\nPalmenweg 23a\n48463 Grähburg',
    'notes': '',
}
patientRequest_dict = {
    'patientName': 'Moritz Mohr',
    'pRStartDateTime': datetime.timestamp(datetime.now()),
    'pREmployee': 'Frau Müller',
    'pREndDateTime': '',
    'pRText': 'Ich fühle mich nicht so wohl, könnte demnächst bitte jemand kommen?',
    'pRprio': 'Hoch',
}
vitals_dict = {
    'vitType': '1',
    'vitValue': '81',
    'vitDateTime': datetime.timestamp(datetime.now()),
    'patientName': 'Moritz Mohr',
    'employeeName': '1',
    'vitReleased': ''
}
patientcondition_dict = {
    'patientName': 'Moritz Mohr',
    'pcDateTime': datetime.timestamp(datetime.now()),
    'pcType': '3',
    'pcText': 'Starke nässenden offene dekubitus linke Arschbacke. Starke verschlechterung geben über Vortag. Patient nur schwer ansprechbar.',
    'pcEmployeeName': '1',
    'pcReleased': '',
}
prescriptions_dict = {
    'medNo': '37',
    'medName': 'Ibu',
    'dose': '800mg',
    'form': 'Tablette',
    'frequency': '1010',
    'startDate': 1666886946,
    'endDate': '',
    'patientName': 'Moritz Mohr',
    'note': '',
    'reason': 'Schlüsselbein Operation',
    'prescReleased': '',
    'wechselwirkung': ''
}
medication_dict = {
    'medNumber': '',
    'patientName': 'Moritz Mohr',
    'employeeid': '',
    'medName': '',
    'dose': '',
    'form': '',
    'dateTime': 1667059746,
    'note': '',
    'reason': '',
    'medReleased': '',
}

employees_dict = {
    'efirstname': 'Petra',
    'esurename': 'Müller',
    'ejobdesc': 'Krankenpflegerin',
}

room_dict = {
    'roomName': '3B-12',
    'roomCapacity': '3'
}

roomConditions_dict = {
    'dateTime': datetime.timestamp(datetime.now()),
    'airQuality': '',
    'roomTemperature': '21.2',
}