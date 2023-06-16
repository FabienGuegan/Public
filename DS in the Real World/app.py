import os
import json
import pickle
import joblib
import pandas as pd
from flask import Flask, jsonify, request
from peewee import (
    SqliteDatabase, PostgresqlDatabase, Model, IntegerField,
    FloatField, TextField, IntegrityError
)
from playhouse.shortcuts import model_to_dict
from playhouse.db_url import connect

########################################
# Begin database stuff

DB = connect(os.environ.get('DATABASE_URL') or 'sqlite:///predictions.db')


class Prediction(Model):
    admission_id = IntegerField(unique=True)
    observation = TextField()
    predicted_readmitted = TextField()
    actual_readmitted = TextField(null=True)

    class Meta:
        database = DB


DB.create_tables([Prediction], safe=True)

# End database stuff
########################################

########################################
# Unpickle the previously-trained model


with open(os.path.join('data', 'columns.json')) as fh:
    columns = json.load(fh)


with open(os.path.join('data', 'pipeline.pickle'), 'rb') as fh:
    pipeline = joblib.load(fh)


with open(os.path.join('data', 'dtypes.pickle'), 'rb') as fh:
    dtypes = pickle.load(fh)


# End model un-pickling
########################################

########################################
# Input validation functions


numerical_features = [
    'hemoglobin_level',
    'admission_id',
    'num_medications',
    'num_procedures',
    'number_diagnoses',
    'number_emergency',
    'number_inpatient',
    'number_outpatient',
    'patient_id',
    'num_lab_procedures',
    'time_in_hospital',
    'admission_source_code',
    'discharge_disposition_code',
    'admission_type_code']

categorical_features = [
    'blood_transfusion',
    'has_prosthesis',
    'A1Cresult',
    'age',
    'blood_type',
    'change',
    'complete_vaccination_status',
    'diabetesMed',
    'diag_1',
    'diag_2',
    'diag_3',
    'diuretics',
    'gender',
    'insulin',
    'max_glu_serum',
    'medical_specialty',
    'payer_code',
    'race',
    'weight']

#'readmitted'




def check_request(request):
    
    #check that no additional key is received
    for key in request.keys():
        if key not in columns:
            error = key
            return False, error

    #check that all keys are present 
    for key in columns:
        if key not in request.keys():
            error = key
            return False, error
    

    return True, ""


"""
    def check_valid_column(observation):
        
            Validates that our observation only has valid columns
            
            Returns:
            - assertion value: True if all provided columns are valid, False otherwise
            - error message: empty if all provided columns are valid, False otherwise
        
        
        valid_columns = {
        "SubjectRaceCode",
        "SubjectSexCode",
        "SubjectEthnicityCode",
        "StatuteReason", 
        "InterventionReasonCode", 
        "ResidentIndicator", 
        "SearchAuthorizationCode",
        "SubjectAge",
        "hour",
        "day_of_week",
        }
        
        keys = set(observation.keys())
        
        if len(valid_columns - keys) > 0: 
            missing = valid_columns - keys
            error = "Missing columns: {}".format(missing)
            return False, error
        
        if len(keys - valid_columns) > 0: 
            extra = keys - valid_columns
            error = "Unrecognized columns provided: {}".format(extra)
            return False, error    

        return True, ""
"""


def check_categorical_values(observation):
    """
        Validates that all categorical fields are in the observation and values are valid
        
        Returns:
        - assertion value: True if all provided categorical columns contain valid values, 
                           False otherwise
        - error message: empty if all provided columns are valid, False otherwise
    """
    
    valid_category_map = {
       'race': ['White', 'Caucasian', 'European', 'AfricanAmerican', 'EURO',
       'Afro American', '?', 'African American', 'WHITE', 'Asian',
       'Black', 'Hispanic', 'Other', 'Latino', 'AFRICANAMERICAN'],
       'gender': ['Male', 'Female', 'Unknown/Invalid'], 
       'age': ['[80-90)', '[40-50)', '[30-40)', '[70-80)', '[90-100)', '[50-60)','[60-70)', '[20-30)', "NaN", '[10-20)', '[0-10)'], 
       'weight': ['?', "NaN", '[50-75)', '[25-50)', '[75-100)', '[125-150)','[100-125)', '[0-25)', '[150-175)', '[175-200)'], 
       'payer_code': ['?', 'UN', 'MC', 'SP', 'DM', 'HM', 'MD', 'BC', 'CM', 'CP', 'WC','OG', 'PO', 'MP', 'OT', 'CH', 'SI'], 
       'medical_specialty': ['?', 'Family/GeneralPractice', 'InternalMedicine', 'Surgery-Neuro',
                            'Orthopedics-Reconstructive', 'Pulmonology', 'Surgery-General',
                            'Hematology/Oncology', 'Gastroenterology', 'Oncology',
                            'Emergency/Trauma', 'Cardiology', 'Neurology', 'Orthopedics',
                            'Nephrology', 'Surgery-Cardiovascular/Thoracic', 'Urology',
                            'Surgery-Vascular', 'ObstetricsandGynecology', 'Radiologist',
                            'Pediatrics', 'Surgery-Cardiovascular', 'DCPTEAM', 'Podiatry',
                            'Psychiatry', 'Endocrinology', 'Psychology',
                            'PhysicalMedicineandRehabilitation', 'Surgery-Thoracic',
                            'Endocrinology-Metabolism', 'Pediatrics-Endocrinology',
                            'Hematology', 'Osteopath', 'Pediatrics-Pulmonology',
                            'Otolaryngology', 'Obstetrics', 'Resident',
                            'Pediatrics-CriticalCare', 'Gynecology', 'SurgicalSpecialty',
                            'Radiology', 'Surgery-Plastic', 'Hospitalist', 'Pathology',
                            'Surgery-Colon&Rectal', 'InfectiousDiseases',
                            'Pediatrics-Hematology-Oncology', 'Surgery-Maxillofacial',
                            'Psychiatry-Child/Adolescent', 'Anesthesiology-Pediatric',
                            'Anesthesiology', 'PhysicianNotFound', 'Cardiology-Pediatric',
                            'Ophthalmology', 'Surgeon', 'Psychiatry-Addictive',
                            'Pediatrics-Neurology', 'Obsterics&Gynecology-GynecologicOnco',
                            'Rheumatology', 'AllergyandImmunology'], 
       'has_prosthesis': [False,  True],
       'complete_vaccination_status': ['Complete', 'Incomplete', 'None'], 
       'diag_1': ['185', '786', '590', '250.82', '486', '724', '411', '571', '715',
              '398', '733', '721', '410', '569', '996', '560', '518', '250.6',
              '414', '250.11', '599', '789', '274', '491', '564', '?', '156',
              '584', '38', '427', '574', '558', '575', '719', '162', '431',
              '434', '553', '428', '812', '493', '250.02', '722', '413', '780',
              '153', '997', '415', '435', '458', '295', '350', '530', '995',
              '424', '824', '200', '250.8', '707', '437', '576', 'V58', '552',
              '496', '562', '331', '188', '807', '820', '482', '404', '432',
              '401', '577', '250.42', '403', '515', '433', '250.7', '276',
              '250.1', '440', '642', '682', '611', 'V57', '250.03', '453', '296',
              '578', '202', '323', '511', '532', '238', '850', '600', '157',
              '136', '278', '805', '998', '659', '288', '555', '344', '716',
              '311', '535', '198', '285', '714', '218', '250.13', 'V55', '507',
              '250.81', '607', '211', '614', '54', '220', '280', '625', '244',
              '348', '648', '447', '309', '438', '727', '395', '250', '11',
              '846', '436', '728', '423', '483', '586', '487', '464', '250.2',
              '618', '481', '182', '250.22', '189', '572', '945', '920', 'V54',
              '802', '429', '681', '346', '250.83', '444', '813', '304', '522',
              '983', '250.32', '866', '416', '291', '581', '303', '787', '402',
              '808', '729', '261', '531', '823', '386', '656', '250.4', '860',
              '174', '250.12', '980', '42', '250.41', '8', '626', '294', '592',
              '933', '204', '536', '290', '420', '782', '466', '836', '596',
              '88', '790', '388', '718', '191', '751', '305', '452', '250.93',
              '490', '528', '426', '284', '79', '717', '534', '785', '332',
              '822', '307', '557', '730', '963', '540', '286', '568', '723',
              '131', '383', '227', '604', '277', '835', '825', '654', '470',
              '512', '380', '801', '924', '573', '338', '197', '455', '283',
              '255', '349', '969', '852', '794', '443', '293', '172', '608',
              '617', '792', '851', '591', '977', '451', '327', '193', 'V66',
              '815', '441', '239', 'V56', '292', '844', '173', '658', '781',
              '196', '345', '298', '233', '494', '459', '492', '865', '333',
              '322', '161', '225', '726', '519', '853', '710', '660', '179',
              '78', '967', '340', '864', '962', '663', '585', '446', '873',
              '550', '154', '300', '845', '593', '972', 'V63', '646', '965',
              '275', '620', '151', '282', '644', '164', '442', '287', '241',
              '514', '336', '816', '355', '566', '175', '537', '621', '709',
              '784', '793', '230', '250.23', '158', '112', '465', '235', '357',
              '516', '236', '425', 'V45', '250.33', '454', '783', '215', '203',
              '958', '297', '312', '595', '999', '737', '421', '922', '485',
              '556', '745', '799', '959', '351', '250.01', '892', '669', '567',
              '821', '916', '250.92', '150', '711', '973', '250.31', '9', '475',
              '480', '921', '840', '473', '694', '362', '661', '266', '541',
              '97', '306', '53', '588', '521', '989', '252', '250.43', '966',
              '250.52', '456', '66', '942', '183', '527', '184', '579', '495',
              '616', '359', '171', '524', '500', '245', '210', 'V71', '70',
              '725', '738', '430', '756', '991', '510', '320', '632', '253',
              '583', '337', '363', '810', '935', '970', '226', '601', '237',
              '347', 'V53', '377', '664', '513', '142', '533', '622', '217',
              '878', '35', '690', '695', '952', '250.21', '281', '843', '800',
              '693', '110', '652', '205', '368', '462', '448', '155', '250.5',
              '788', '680', '508', '627', '647', '705', '735', '955', '223',
              '353', '341', '375', '570', '826', '308', '208', '753', '396',
              '759', '7'], 

       'diag_2': ['788', '425', '250', 'V85', '276', '250.8', '998', '250.02', '584',
              '496', '250.01', '716', '250.1', '493', '280', '112', '197', '707',
              '401', '403', '428', '715', '?', '571', '995', '780', '414', '359',
              '486', '599', '287', '447', '434', '345', '919', '424', '781',
              '214', '305', '518', '300', '511', '585', '427', '295', '553',
              '285', 'E849', '705', '429', '70', '728', '201', '568', "NaN", '600',
              '733', '512', '411', '153', '530', '250.11', '41', 'E885', '242',
              '244', '997', '574', '250.51', '342', '785', '682', '786', '648',
              'V10', '799', '250.03', '337', '250.43', '413', '303', '250.82',
              '710', '533', '250.6', '578', '727', '492', '807', '410', '560',
              '284', '278', '198', '412', '564', 'V43', '294', '577', '293',
              'E932', '340', '296', 'V45', '595', '491', '996', '162', '402',
              '535', '151', '331', '179', '626', 'V42', '250.4', '218', '784',
              '731', '572', '618', '920', '438', '466', '693', '573', '567',
              '722', 'V58', 'E888', '250.41', '847', '614', '730', '437', '453',
              '250.92', '591', '291', '250.12', '261', 'E917', '435', '416',
              '802', '189', '253', '703', '255', '787', 'V72', 'E878', '738',
              '536', '396', '836', '531', '892', '38', '202', '211', '357',
              '864', 'V62', '292', '348', '575', '664', '174', '706', '440',
              '610', '482', '540', '557', '250.81', '723', '616', '312', '782',
              '368', '789', '304', '283', '507', '751', '465', '719', '590',
              '157', '135', 'V63', '426', '263', '250.5', '281', '681', '42',
              '805', '458', '433', '277', '333', '378', '250.42', '808', '386',
              'E934', 'V64', '272', '332', '8', '344', '196', '111', '356',
              '199', '250.7', '203', '873', '724', '53', '279', '569', '154',
              '663', '420', '204', '34', '473', '415', '452', '820', '592',
              '456', 'V46', '625', '262', '443', '729', '441', '783', '959',
              '297', '816', '481', '556', '250.93', '714', '790', '290', '910',
              '436', '282', '394', 'E942', '506', '562', '837', '759', 'E884',
              '301', 'E947', '813', '404', 'E880', '232', 'E939', '796', '515',
              '351', '349', '250.52', '576', '868', 'E930', '558', 'V12', '654',
              'V15', '185', '311', '593', '869', '642', 'V49', '617', '288',
              '250.31', '200', '721', '444', '252', '581', '451', 'V54', '223',
              '704', '684', 'V17', '208', 'E928', '607', '432', '883', '94',
              '172', '183', '822', '550', '711', '620', '397', '380', '842',
              '117', '156', '824', 'V14', '421', '250.83', '494', '490', '611',
              '350', 'E935', '644', '358', 'E919', '40', 'V23', '924', '286',
              '336', '933', '346', '275', '314', '455', '150', '758', '319',
              '794', '583', '9', '250.22', '365', '552', '487', '422', '274',
              '994', '289', '860', '999', '923', '238', '298', '753', '27',
              '537', '821', '659', '861', '852', '459', '726', '527', '152',
              '205', '260', '79', '377', '322', '826', '362', 'E819', '155',
              '922', '327', '268', '850', '661', '250.53', '309', '519', '480',
              '812', '250.13', '696', '446', '594', '320', '532', '11', '872',
              '521', '516', '462', 'V57', '138', '867', '680', '934', '258',
              '233', '191', '596', '746', 'V66', '324', '369', '31', '621',
              '647', '398', '701', '423', '565', '916', '310', '114', 'E870',
              '431', '524', 'E931', 'E968', '500', '463', 'E933', '685', 'V11',
              '460', '273', '485', '352', '307', '619', '909', '335', '717',
              '355', '478', '522', '250.91', '376', '958', '905', 'V65', '823',
              '141'], 
       'diag_3': ['601', '250.01', '401', '784', '276', '427', '250.02', '491',
              '599', '428', '585', '737', '244', '403', '496', '682', '272',
              '584', '70', '786', '493', '305', '?', '574', '482', '780', '414',
              '250', '433', 'E885', '425', '402', '424', '531', '716', '787',
              'V15', '410', '280', '38', '443', '571', '794', '285', '997',
              '693', '600', '596', '861', '41', '197', '250.6', 'E849', '518',
              '411', '593', '588', '278', '511', '707', '577', '722', '446',
              '438', '730', '250.53', '458', '250.4', '440', '250.8', '263',
              '277', '729', '466', '535', '203', '473', '805', 'V85', 'V45',
              '620', 'V14', 'E942', '294', '459', '413', '112', '789', 'V17',
              '225', 'V42', '416', '530', '250.82', '560', '296', '486', '301',
              '552', '956', '617', '54', 'V58', '357', '441', '910', '202',
              'E930', '310', '537', '536', '726', '562', '426', '799', '515',
              '710', '790', '924', 'E878', '578', '731', 'V12', 'V10', '996',
              '255', '533', '616', '781', '792', '303', '311', '465', '174',
              '198', '250.42', '800', '583', '995', '591', '611', '253', '300',
              '658', '356', '462', '397', 'V46', '453', '250.5', '342', '274',
              '204', '733', '250.52', '522', 'E933', '250.81', 'V03', '284',
              '304', '719', '295', 'E884', '998', 'E947', '568', '785', '287',
              '358', '922', '260', 'V16', '250.1', '293', '396', '492', '592',
              '153', '309', '742', 'V64', '348', '686', 'E935', '681', '404',
              '721', '437', '788', '412', '715', '250.92', '199', '728', '836',
              '155', '312', '291', '724', 'V65', '331', '572', '338', '523',
              '78', '808', 'V43', '337', '580', '5', '581', '378', 'V54', 'E888',
              '796', '558', '250.7', '8', 'E950', 'E934', '384', '661', '435',
              'E880', '494', '200', '196', '647', 'V72', '783', '162', '648',
              '218', 'V27', '782', '217', '368', '569', '680', '307', '516',
              'V49', '327', '250.03', '211', '451', '573', '7', 'E938', '447',
              '157', '834', 'V62', '290', '34', '275', '389', 'V09', '318',
              '429', '812', '250.93', '336', '696', '590', 'V06', '507', '281',
              '517', '420', '349', '250.83', '553', '373', '692', '299', '351',
              '610', '288', '555', '625', '286', '958', '741', '564', '346',
              '317', '484', '999', '532', '332', '745', 'E892', '738', '664',
              '820', '621', '250.41', '131', '595', 'E941', '423', '512', '170',
              '626', '250.51', '434', '380', '135', '915', '646', '607', '519',
              '235', '907', '712', '455', '824', '442', '334', '883', '273',
              '282', '807', 'E932', '652', '362', '344', '604', '79', '189',
              '575', '454', '659', '185', '279', '576', '456', '333', '521',
              '655', '850', '180', '354', '340', '714', '208', '923', '709',
              '150', '151', '663', '665', '242', '146', '478', '543', 'E858',
              '851', '727', 'E879', 'E812', 'E819', '802', '405', '845', '618',
              '913', '579', '17', '250.12', '11', '814', '840', 'E939', '138',
              '94', '598', '42', '415', '948', 'V70', '457', '382', '245', '656',
              '920', 'E905', 'V08', '685', '369', '916', '514', '252', 'V44',
              'E929', 'V55', '823', '642', '53', '214', '746', 'V02', '171',
              '490', 'V13', '461', '388', '718', '586', '567', '528', '161',
              '250.13', '306', '713', '649', '747', '928', '250.43', '379',
              '183', '386', '398', '711', '201', '251', '908', '394', '860',
              '614', 'V66', '238', '319', '205', '487', '376', '444', 'E920',
              '695', 'V63', '383', '825', '298', 'E931', '723', '361', '704',
              '753', '935', '292', '355', '261', '694', '873', '945', '154',
              '250.23', '841', '343', '345', 'E936', '793', '654', '867', '365',
              '627', '736', '35', '801', '110', '717', '605', '959', '250.11',
              '3', '534', '250.9', '445', '360', '250.2', '262', 'V23'],
              
       'blood_type': ['A-', 'O+', 'A+', 'B+', 'O-', 'AB-', 'AB+', 'B-'], 
       'blood_transfusion': [False,  True],
       'max_glu_serum': ['NONE', '>200', 'None', '>300', 'NORM', 'Norm'], 
       'A1Cresult': ['None', '>8', '>7', 'Norm'], 
       'diuretics': ['No', 'Yes'], 
       'insulin': ['No', 'Yes'], 
       'change': ['No', 'Ch'], 
       'diabetesMed': ['No', 'Yes']
    }
    
    for key, valid_categories in valid_category_map.items():
        if key in observation:
            value = observation[key]
            if value not in valid_categories:
                error = "Invalid value provided for {}: {}. Allowed values are: {}".format(
                    key, value, ",".join(["'{}'".format(v) for v in valid_categories]))
                return False, error
        else:
            error = "Categorical field {} missing"
            return False, error

    return True, ""


def check_numerical_values(observation):

    valid_num_range = {
        'admission_type_code': [1.0, 8.0],
        'discharge_disposition_code': [1.0, 28.0],
        'admission_source_code': [1, 22],
        'time_in_hospital': [1, 14],
        'num_lab_procedures': [1.0, 132.0],
        'num_procedures': [0, 6],
        'num_medications': [1.0, 70.0],
        'number_outpatient': [0, 35],
        'number_emergency': [0, 22],
        'number_inpatient': [0, 18],
        'number_diagnoses': [1, 16],
        'hemoglobin_level': [10.9, 18.1]
        }

    for key, valid_range in valid_num_range.items():

        if key not in observation: 
            error = f"Field {key} missing"
            return False, error
        


        value = observation[key]
     
        if not isinstance(value, int) and not isinstance(value, float):
            error = f"Field {key} is not an integer or float"
            return False, error
        
        if value < valid_range[0] or value > valid_range[1]:
            error = f"Field {key} is not within defined range"
            return False, error

    return True, ""

# End input validation functions
########################################

########################################
# Begin webserver stuff

app = Flask(__name__)


@app.route('/predict', methods=['POST'])
def predict():
    obs_dict = request.get_json()
  
    request_ok, error = check_request(obs_dict)
    
    if not request_ok:
        response = {'error': error}
        return jsonify(response)

    _id = obs_dict['admission_id']

    
    categories_ok, error = check_categorical_values(obs_dict)
    if not categories_ok:
        response = {'error': error}
        return jsonify(response)

    numerics_ok, error = check_numerical_values(obs_dict)
    if not numerics_ok:
        response = {'error': error}
        return jsonify(response)


    obs = pd.DataFrame([obs_dict], columns=columns).astype(dtypes)
    
    prediction = pipeline.predict(obs)[0]
    
    response = {'readmitted': prediction}
    
    p = Prediction(
        admission_id=_id,
        observation=obs_dict,
        predicted_readmitted = prediction
    )

    try:
        p.save()
    except IntegrityError:
        error_msg = "ERROR: Observation Id: '{}' already exists".format(_id)
        response["error"] = error_msg
        print(error_msg)
        DB.rollback()
    return jsonify(response)

    
@app.route('/update', methods=['POST'])
def update():
    obs = request.get_json()
    try:
        p = Prediction.get(Prediction.admission_id == obs['admission_id'])
        p.actual_readmitted = obs['readmitted']
        p.save()
        
        response = {
                    "admission_id": obs['admission_id'],
                    "actual_readmitted": obs['readmitted'],
                    "predicted_readmitted": p.predicted_readmitted
                    }

        return jsonify(response)
    except Prediction.DoesNotExist:
        error_msg = 'Admission Id: "{}" does not exist'.format(obs['admission_id'])
        return jsonify({'error': error_msg})


    
if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=5000)
