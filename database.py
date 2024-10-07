import pandas as pd
import random
import datetime
import mysql.connector

def abstract_data(measurements):
    # Define a function to categorize the WBC count
    def categorize_wbc(value):
        value = int(value)
        if value < 4000:
            return 'wbc_low'
        elif 4000 <= value <= 10000:
            return 'wbc_medium'
        else:
            return 'wbc_high'

    # Apply the function to the 'value' column and create a new 'state' column
    measurements['state'] = measurements['value'].apply(categorize_wbc)
    return measurements


class PatientData:
    def __init__(self, host, user, password, database):
        self.db_connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.cursor = self.db_connection.cursor()

    # Get patient by first name and last name
    def get_patient_data(self, first_name, last_name):
        print('@@@@@@@')
        self.cursor.execute(
            "SELECT first_name, last_na, loinc_num, value, unit, valid_start_time, transaction_time\
            FROM test_results p\
            WHERE first_name = %s AND last_name = %s",
            (first_name, last_name,)
        )
        return self.cursor.fetchall()

    # Get patient by first name and last name until thw last relevant time
    def get_patient_data_by_valid_end_time(self, first_name, last_name, end_datetime):
        self.cursor.execute(
            """
            SELECT loinc_num, value, unit, valid_start_time, transaction_time
            FROM patients p
            JOIN test_results t ON p.id = t.patient_id
            WHERE first_name = %s AND last_name = %s
            AND valid_start_time <= %s
            ORDER BY valid_start_time DESC
            """,
            (first_name, last_name, end_datetime)
        )
        return self.cursor.fetchall()
        
        if result == []:
            print("No data found for the given first name and last name.")
            return None  # You can return None or any other indicator for no data found

        return result










    def time_interval_table(self, first_name, last_name):
        patient_data = self.get_patient_data(first_name, last_name)
        patient_data_columns = ['first_name', 'last_name','loinc_num', 'value','unit','valid_start_time','transaction_time']
        df = pd.DataFrame(patient_data, columns=patient_data_columns)

        # Filter the DataFrame to include only WBC measurements
        wbc = df[df['unit'] == 'cells/ml']
        hemoglobin = df[df['unit'] == 'gr/dl']

        # Sort the DataFrame by valid_start_time
        wbc = wbc.sort_values(by=['valid_start_time'])
        hemoglobin = hemoglobin.sort_values(by=['valid_start_time'])
        abstracts_1 = abstract_data(wbc)
        abstracts_2 = abstract_data(hemoglobin)

        return abstracts_1, abstracts_2


    def dictinary_of_time_interval(self, measurements):
        # Initialize variables
        intervals = {}
        interval_start = measurements.iloc[0]['valid_start_time']
        interval_name = 'interval_1'
        intervals[interval_name] = [interval_start]
        interval_index = 1

        # Iterate through the DataFrame to find intervals
        for i in range(1, len(measurements)):
            current_time = measurements.iloc[i]['valid_start_time']
            previous_time = measurements.iloc[i - 1]['valid_start_time']

            current_state = measurements.iloc[i]['state']
            previous_state = measurements.iloc[i - 1]['state']

            # Check if the time difference is more than 2 days
            if current_time - previous_time < datetime.timedelta(days=2) and current_state == previous_state:
                intervals[interval_name].append(current_time)
            else:
                intervals[interval_name].append(previous_time)
                interval_index += 1
                interval_name = f'interval_{interval_index}'
                intervals[interval_name] = [current_time]

        # Remove duplicates in intervals
        for key in intervals:
            intervals[key] = [intervals[key][0] - datetime.timedelta(days=2), intervals[key][-1] + datetime.timedelta(days=2)]

        print(intervals)
        return intervals


    # Add a patient to the database
    def add_patient(self, id, first_name, last_name):
        self.cursor.execute(
            "INSERT INTO patients (id, first_name, last_name) VALUES (%s, %s, %s)",
            (id, first_name, last_name)
        )
        self.db_connection.commit()
        return self.cursor.lastrowid

    # Add test results for a patient
    def add_test_result(self, id, patient_id, loinc_num, value, unit, valid_start_time, transaction_time):
        self.cursor.execute(
            "INSERT INTO test_results (id, patient_id, loinc_num, value, unit, valid_start_time, transaction_time) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (id, patient_id, loinc_num, value, unit, valid_start_time, transaction_time)
        )
        self.db_connection.commit()

    # Get patient test results
    def get_test_results(self, patient_id):
        self.cursor.execute(
            "SELECT loinc_num, value, unit, valid_start_time, transaction_time FROM test_results WHERE patient_id = %s",
            (patient_id,)
        )
        return self.cursor.fetchall()

    def get_all_patients(self):
        self.cursor.execute("SELECT DISTINCT first_name, last_name FROM patients")
        patients = self.cursor.fetchall()
        return patients

    def get_all_loinc_numbers(self):
        self.cursor.execute("SELECT DISTINCT loinc_num FROM test_results")
        loincs = self.cursor.fetchall()
        return loincs



    def __del__(self):
        self.cursor.close()
        self.db_connection.close()

# if __name__ == "__main__":
#     patient_data = PatientData(host="localhost", user="root", password="q6rh3b", database="patient_data")

    # data = patient_data.get_patient_data('Eyal', 'Rothman')
    # for d in data:
    #     print(d)

    # abstracts_1, abstracts_2 = patient_data.time_interval_table('Eyal', 'Rothman')
    # print(abstracts_1)
    # print(abstracts_2)
    # dict_ = patient_data.dictinary_of_time_interval(abstracts_1)

    # data = pd.get_patient_data('Eyal', 'Rothman')
    # print(type(data))
    # for d in data:
    #     print(d)

    # Add patients
    # idan_id = pd.add_patient(3, "Idan", "Gal")

    # Add test results
    # pd.add_test_result(51, 1, '11218-5', 4500, 'cells/ml', '2018-05-17 13:11:00', '2018-05-27 10:00:00')
    # pd.add_test_result(23, 2, '11218-5', 5500, 'cells/ml', '2018-05-18 15:00:00', '2018-05-21 10:00:00')

    # # Retrieve and print test results for Eyal
    # test_results = kb.get_test_results(eyal_id)
    # for result in test_results:
    #     print(result)

