import PySimpleGUI as sg
import datetime
from database import PatientData
from dss_engine import DSSEngine

# ************** Utilities for GUI *****************
patient_data = PatientData(host="localhost", user="root", password="q6rh3b", database="patient_data")
engine = DSSEngine(patient_data)


# Get all recorded patients in the database
def get_patient_list():
    return patient_data.get_all_patients()


# Get all recorded LOINC numbers in the database
def get_loinc_list():
    return patient_data.get_all_loinc_numbers()


# Get a list of times of day in 15 min intervals
def get_time_list():
    # Generate a list of times in 15-minute intervals
    times = []
    for hour in range(24):
        for minute in [0, 15, 30, 45]:
            times.append(f"{hour:02d}:{minute:02d}")
    return times


# ************ Query managers ***********************
# direct ech GUI query to the relevant engine function
def query_database(query_type, **kwargs):
    result = None
    if query_type == "specific":
        result = query_retrieval_question(kwargs)
    elif query_type == "historical":
        result = query_retrieval_history(kwargs)
    elif query_type == "update":
        result = query_update_record(kwargs)
    elif query_type == "delete":
        result = query_delete_record(kwargs, result)
    elif query_type == "patient_state":
        # Simulate fetching patient state data
        # mock = [
        #     {
        #         "patient_name": "John Doe",
        #         "hemoglobin_state": "Normal",
        #         "hematological_state": "Stable",
        #         "toxicity_grade": "Grade 0",
        #         "recommendations": ["Continue current treatment", "Follow-up in 2 weeks"]
        #     },
        #     {
        #         "patient_name": "Jane Smith",
        #         "hemoglobin_state": "Low",
        #         "hematological_state": "Unstable",
        #         "toxicity_grade": "Grade 2",
        #         "recommendations": ["Adjust medication dosage", "Increase monitoring frequency"]
        #     }
        # ]

        result = query_patients_states(kwargs, result)

    return result["Successful"], result["result_list"], result["message"]


def query_patients_states(kwargs, result):
    db_state_date = kwargs['db_state_date']
    db_state_time = kwargs['db_state_time']
    query = (db_state_date, db_state_time)

    # Results
    result = {"Successful": True, "result_list": [], "message": ""}
    query_result = engine.patient_states(query)

    if isinstance(query_result, str):  # Case an Error message is returned from query
        result["Successful"] = False
        result["message"] = query_result
    else:
        result["result_list"] = query_result

    return result


def query_delete_record(kwargs, result):
    full_name = str(kwargs['patient_name'])
    first_name, last_name = full_name.split(" ")
    loinc_number = kwargs['loinc_number']
    valid_date = kwargs['valid_date']
    valid_time = kwargs['valid_time']
    transaction_date = kwargs['transaction_date']
    transaction_time = kwargs['transaction_time']
    query = (first_name, last_name, loinc_number,
             valid_date, valid_time, transaction_date, transaction_time)

    # Results
    result = {"Successful": True, "result_list": [], "message": ""}
    query_result = engine.delete_record(query)

    if isinstance(query_result, str):  # Case an Error message is returned from query
        result["Successful"] = False
        result["message"] = query_result
    else:
        result["result_list"] = query_result
        result["message"] = "Delete was Successful"

    return result


def query_update_record(kwargs):
    full_name = str(kwargs['patient_name'])
    first_name, last_name = full_name.split(" ")
    loinc_number = kwargs['loinc_number']
    new_value = kwargs['new_value']
    valid_date = kwargs['valid_date']
    valid_time = kwargs['valid_time']
    transaction_date = kwargs['transaction_date']
    transaction_time = kwargs['transaction_time']
    query = (first_name, last_name, loinc_number,
             valid_date, valid_time, transaction_date, transaction_time)

    # Results
    result = {"Successful": True, "result_list": [], "message": ""}
    query_result = engine.update_record(new_value, query)
    if isinstance(query_result, str):  # Case an Error message is returned from query
        result["Successful"] = False
        result["message"] = query_result
    else:
        result["result_list"] = query_result
        result["message"] = "Update was Successful"

    return result


def query_retrieval_history(kwargs):
    full_name = str(kwargs['patient_name'])
    first_name, last_name = full_name.split(" ")
    loinc_number = kwargs['loinc_number']
    from_db_state_date = kwargs['from_db_state_date']
    from_db_state_time = kwargs['from_db_state_time']
    to_db_state_date = kwargs['to_db_state_date']
    to_db_state_time = kwargs['to_db_state_time']
    query = (first_name, last_name, loinc_number,
             from_db_state_date, from_db_state_time, to_db_state_date, to_db_state_time)
    # Results
    result = {"Successful": True, "result_list": [], "message": ""}
    query_result = engine.retrieval_history_question(query)
    if isinstance(query_result, str):  # Case an Error message is returned from query
        result["Successful"] = False
        result["message"] = query_result
    else:
        result["result_list"] = query_result

    return result


def query_retrieval_question(kwargs):
    # Parameters
    full_name = str(kwargs['patient_name'])
    first_name, last_name = full_name.split(" ")
    loinc_number = kwargs['loinc_number']
    valid_date = kwargs['date']
    valid_time = kwargs['date']
    physician_date = kwargs['db_state_date']
    physician_time = kwargs['db_state_time']
    query = (first_name, last_name, loinc_number,
             valid_date, valid_time, physician_date, physician_time)

    # Results
    result = {"Successful": True, "result_list": [], "message": ""}
    query_result = engine.retrieval_question(query)
    if isinstance(query_result, str):  # Case an Error message is returned from query
        result["Successful"] = False
        result["message"] = query_result
    else:
        result["result_list"] = query_result
    return result


# GUI Manager
def create_gui():
    # Relevant lists for GUI
    patient_list = get_patient_list()
    loinc_list = get_loinc_list()
    time_list = get_time_list()

    # The GUI layout - Each tab in the list is a query
    layout = [
        [sg.TabGroup([
            [sg.Tab('Specific Query', [
                [sg.Text("Patient Full Name:"), sg.Combo(patient_list, key="-SQ-PATIENT_NAME-", size=(30, 1))],
                [sg.Text("LOINC Number:"), sg.Combo(loinc_list, key="-SQ-LOINC-", size=(30, 1))],
                [sg.Text("Date:"), sg.Input(key="-SQ-DATE-"),
                 sg.CalendarButton("Select Date", target="-SQ-DATE-", format="%Y-%m-%d")],
                [sg.Text("Time:"), sg.Combo(time_list, key="-SQ-TIME-", size=(30, 1))],
                [sg.Text("Database State Date:"), sg.Input(key="-SQ-DB_STATE_DATE-"),
                 sg.CalendarButton("Select DB State Date", target="-SQ-DB_STATE_DATE-", format="%Y-%m-%d")],
                [sg.Text("Database State Time:"), sg.Combo(time_list, key="-SQ-DB_STATE_TIME-", size=(30, 1))],
                [sg.Button("Query Specific", key="-SQ-QUERY-"), sg.Button("Clear", key="-SQ-CLEAR-")],
                [sg.Table(values=[], headings=["Patient Name", "LOINC Number", "Result", "Date", "Time"],
                          auto_size_columns=True, justification="left", num_rows=10, key="-SQ-RESULTS-")],
                 [sg.Text("", key="-SQ-MESSAGE-", text_color="green")]
            ]),
             sg.Tab('Historical Query', [
                 [sg.Text("Patient Full Name:"), sg.Combo(patient_list, key="-HQ-PATIENT_NAME-", size=(30, 1))],
                 [sg.Text("LOINC Number:"), sg.Combo(loinc_list, key="-HQ-LOINC-", size=(30, 1))],
                 [sg.Text("Date:"), sg.Input(key="-HQ-DATE-"),
                  sg.CalendarButton("Select Date", target="-HQ-DATE-", format="%Y-%m-%d")],
                 [sg.Text("Time:"), sg.Combo(time_list, key="-HQ-TIME-", size=(30, 1))],
                 [sg.Text("From DB State Date:"), sg.Input(key="-HQ-FROM_DB_STATE_DATE-"),
                  sg.CalendarButton("Select From Date", target="-HQ-FROM_DB_STATE_DATE-", format="%Y-%m-%d")],
                 [sg.Text("From DB State Time:"), sg.Combo(time_list, key="-HQ-FROM_DB_STATE_TIME-", size=(30, 1))],
                 [sg.Text("To DB State Date:"), sg.Input(key="-HQ-TO_DB_STATE_DATE-"),
                  sg.CalendarButton("Select To Date", target="-HQ-TO_DB_STATE_DATE-", format="%Y-%m-%d")],
                 [sg.Text("To DB State Time:"), sg.Combo(time_list, key="-HQ-TO_DB_STATE_TIME-", size=(30, 1))],
                 [sg.Button("Query Historical", key="-HQ-QUERY-"), sg.Button("Clear", key="-HQ-CLEAR-")],
                 [sg.Table(values=[], headings=["Patient Name", "LOINC Number", "Result", "Date", "Time", "DB State"],
                           auto_size_columns=True, justification="left", num_rows=10, key="-HQ-RESULTS-")],
                 [sg.Text("", key="-HQ-MESSAGE-", text_color="green")]
             ]),
             sg.Tab('Update Query', [
                 [sg.Text("Patient Full Name:"), sg.Combo(patient_list, key="-UQ-PATIENT_NAME-", size=(30, 1))],
                 [sg.Text("LOINC Number:"), sg.Combo(loinc_list, key="-UQ-LOINC-", size=(30, 1))],
                 [sg.Text("NEW VALUE TO INSERT:"), sg.Input(key="-UQ-VALUE-")],
                 [sg.Text("Valid Date:"), sg.Input(key="-UQ-VALID_DATE-"),
                  sg.CalendarButton("Select Valid Date", target="-UQ-VALID_DATE-", format="%Y-%m-%d")],
                 [sg.Text("Valid Time:"), sg.Combo(time_list, key="-UQ-VALID_TIME-", size=(30, 1))],
                 [sg.Text("Transaction Date:"), sg.Input(key="-UQ-TRANSACTION_DATE-"),
                  sg.CalendarButton("Select Transaction Date", target="-UQ-TRANSACTION_DATE-", format="%Y-%m-%d")],
                 [sg.Text("Transaction Time:"), sg.Combo(time_list, key="-UQ-TRANSACTION_TIME-", size=(30, 1))],
                 [sg.Button("Update Query", key="-UQ-QUERY-"), sg.Button("Clear", key="-UQ-CLEAR-")],
                 [sg.Table(values=[], headings=["Patient Name", "LOINC Number", "Result", "Valid Date", "Valid Time",
                                                "Transaction Date", "Transaction Time"],
                           auto_size_columns=True, justification="left", num_rows=10, key="-UQ-RESULTS-")],
                 [sg.Text("", key="-UQ-MESSAGE-", text_color="green")]
             ]),
             sg.Tab('Delete Query', [
                 [sg.Text("Patient Full Name:"), sg.Combo(patient_list, key="-DQ-PATIENT_NAME-", size=(30, 1))],
                 [sg.Text("LOINC Number:"), sg.Combo(loinc_list, key="-DQ-LOINC-", size=(30, 1))],
                 [sg.Text("Valid Date:"), sg.Input(key="-DQ-VALID_DATE-"),
                  sg.CalendarButton("Select Valid Date", target="-DQ-VALID_DATE-", format="%Y-%m-%d")],
                 [sg.Text("Valid Time:"), sg.Combo(time_list, key="-DQ-VALID_TIME-", size=(30, 1))],
                 [sg.Text("Transaction Date:"), sg.Input(key="-DQ-TRANSACTION_DATE-"),
                  sg.CalendarButton("Select Transaction Date", target="-DQ-TRANSACTION_DATE-", format="%Y-%m-%d")],
                 [sg.Text("Transaction Time:"), sg.Combo(time_list, key="-DQ-TRANSACTION_TIME-", size=(30, 1))],
                 [sg.Button("Delete Query", key="-DQ-QUERY-"), sg.Button("Clear", key="-DQ-CLEAR-")],
                 [sg.Table(values=[], headings=["Patient Name", "LOINC Number", "Result", "Valid Date", "Valid Time",
                                                "Transaction Date", "Transaction Time"],
                           auto_size_columns=True, justification="left", num_rows=10, key="-DQ-RESULTS-")],
                 [sg.Text("", key="-DQ-MESSAGE-", text_color="green")]
             ]),
             sg.Tab('Patient State', [
                 [sg.Text("Database State Date:"), sg.Input(key="-PS-DB_STATE_DATE-"),
                  sg.CalendarButton("Select DB State Date", target="-PS-DB_STATE_DATE-", format="%Y-%m-%d")],
                 [sg.Text("Database State Time:"), sg.Combo(time_list, key="-PS-DB_STATE_TIME-", size=(30, 1))],
                 [sg.Button("Query Patient State", key="-PS-QUERY-"), sg.Button("Clear", key="-PS-CLEAR-")],
                 [sg.Table(values=[],
                           headings=["Patient Name", "Hemoglobin State", "Hematological State", "Toxicity Grade"],
                           auto_size_columns=True, justification="left", num_rows=10, key="-PS-RESULTS-")],
                 [sg.Multiline(size=(60, 5), key="-PS-RECOMMENDATIONS-", disabled=True)]
             ])
            ]
        ])]
    ]

    # Opening the GUI window
    window = sg.Window("Clinical DSS", layout, resizable=True)

    # Logical loop for directing each use button pushes / selections to a relevant function
    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break
        elif event == "-SQ-QUERY-":
            is_successful, results, message = query_database("specific",
                                     patient_name=values["-SQ-PATIENT_NAME-"],
                                     loinc_number=values["-SQ-LOINC-"],
                                     date=values["-SQ-DATE-"],
                                     time=values["-SQ-TIME-"],
                                     db_state_date=values["-SQ-DB_STATE_DATE-"],
                                     db_state_time=values["-SQ-DB_STATE_TIME-"])
            if is_successful:
                window["-SQ-RESULTS-"].update(values=[list(result.values()) for result in results])
            else:
                window["-SQ-MESSAGE-"].update(message)
        elif event == "-HQ-QUERY-":
            is_successful, results, message = query_database("historical",
                                     patient_name=values["-HQ-PATIENT_NAME-"],
                                     loinc_number=values["-HQ-LOINC-"],
                                     date=values["-HQ-DATE-"],
                                     time=values["-HQ-TIME-"],
                                     from_db_state_date=values["-HQ-FROM_DB_STATE_DATE-"],
                                     from_db_state_time=values["-HQ-FROM_DB_STATE_TIME-"],
                                     to_db_state_date=values["-HQ-TO_DB_STATE_DATE-"],
                                     to_db_state_time=values["-HQ-TO_DB_STATE_TIME-"])
            if is_successful:
                window["-HQ-RESULTS-"].update(values=[list(result.values()) for result in results])
            else:
                window["-HQ-MESSAGE-"].update(message)
        elif event == "-UQ-QUERY-":
            is_successful, results, message = query_database("update",
                                              patient_name=values["-UQ-PATIENT_NAME-"],
                                              loinc_number=values["-UQ-LOINC-"],
                                              new_value=values['-UQ-VALUE-'],
                                              valid_date=values["-UQ-VALID_DATE-"],
                                              valid_time=values["-UQ-VALID_TIME-"],
                                              transaction_date=values["-UQ-TRANSACTION_DATE-"],
                                              transaction_time=values["-UQ-TRANSACTION_TIME-"])
            if is_successful:
                window["-UQ-RESULTS-"].update(values=[list(result.values()) for result in results])
            window["-UQ-MESSAGE-"].update(message)
        elif event == "-DQ-QUERY-":
            is_successful, results, message = query_database("delete",
                                              patient_name=values["-DQ-PATIENT_NAME-"],
                                              loinc_number=values["-DQ-LOINC-"],
                                              valid_date=values["-DQ-VALID_DATE-"],
                                              valid_time=values["-DQ-VALID_TIME-"],
                                              transaction_date=values["-DQ-TRANSACTION_DATE-"],
                                              transaction_time=values["-DQ-TRANSACTION_TIME-"])
            if is_successful:
                window["-DQ-RESULTS-"].update(values=[list(result.values()) for result in results])
            window["-DQ-MESSAGE-"].update(message)
        elif event == "-PS-QUERY-":
            is_successful, results, message = query_database("patient_state",
                                     db_state_date=values["-PS-DB_STATE_DATE-"],
                                     db_state_time=values["-PS-DB_STATE_TIME-"])
            if is_successful:
                window["-PS-RESULTS-"].update(values=[[r["patient_name"], r["hemoglobin_state"], r["hematological_state"], r["toxicity_grade"]] for r in results])
                all_recommendations = ""
                for patient in results:
                    patient_name = patient['patient_name']
                    recommendations = "\n  - ".join(patient['recommendations'])
                    all_recommendations += f"Recommendations for {patient_name}:\n  - {recommendations}\n\n"
                # Update the GUI element with all patients' recommendations
                window["-PS-RECOMMENDATIONS-"].update(all_recommendations)
        elif event in ("-SQ-CLEAR-", "-HQ-CLEAR-", "-UQ-CLEAR-", "-DQ-CLEAR-", "-PS-CLEAR-"):
            prefix = event[:4]  # Either "-SQ-" or "-HQ-", or "-UQ-", or "-DQ-", or "-PS-"
            for key in values:
                if key.startswith(prefix):
                    if key.endswith("PATIENT_NAME-"):
                        window[key].update(value="")
                    else:
                        window[key]("")
            window[f"{prefix}RESULTS-"].update(values=[])
            if prefix in ("-UQ-", "-DQ-"):
                window[f"{prefix}MESSAGE-"].update("")

    window.close()


if __name__ == "__main__":
    create_gui()