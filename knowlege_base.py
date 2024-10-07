import mysql.connector
import pandas as pd
import numpy as np

class KnowledgeBase:
    def __init__(self, host, user, password, database):
        self.db_connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.cursor = self.db_connection.cursor()

    def get_goodbefore_goodafter(self, param):
        #ההמוגלובין  תקף חודש לפני ושבוע אחרי 
        #התאי דם הלבנים עם תוקף של יום יומיים גג לפני ואחרי 
        gbga = {'hemoglobin_level': [(1,0,0),(0,1,0)], 'wbc_level': [(0,0,2),(0,0,2)],
                'systemic_toxicity': [(1,0,0), (1,0,0)]}
        return gbga[param]
    
    def get_concepts(self, sex):
        query = """
            SELECT sex, category, range_value 
            FROM concepts 
            WHERE sex = %s
        """
        self.cursor.execute(query, (sex,))
        return self.cursor.fetchall()


    def add_concept(self,id, data_dict):
        for category, values in data_dict.items():
            sex, range_value = values[0], values[1]
            print(sex)
            print(range_value)
            self.cursor.execute(
                "INSERT INTO concepts (id, sex, category, range_value) VALUES (%s, %s, %s, %s)",
                (id, sex, category, range_value)
            )
        self.db_connection.commit()


    def get_hematological_states(self, gender):
        query = """
            SELECT s.state_name, r.hemoglobin_range, r.wbc_range 
            FROM hematological_states s 
            JOIN hematological_ranges r ON s.id = r.state_id 
            WHERE s.gender = %s
        """
        self.cursor.execute(query, (gender,))
        return self.cursor.fetchall()

    def add_hematological_state(self, gender, data_dict):
        for ranges, state_name in data_dict.items():
            hemoglobin_range, wbc_range = ranges
            self.cursor.execute(
                "INSERT INTO hematological_states (gender, state_name) VALUES (%s, %s)",
                (gender, state_name)
            )
            state_id = self.cursor.lastrowid
            self.cursor.execute(
                "INSERT INTO hematological_ranges (state_id, hemoglobin_range, wbc_range) VALUES (%s, %s, %s)",
                (state_id, hemoglobin_range[1], wbc_range[1])
            )
        self.db_connection.commit()

    def get_systemic_toxicity(self):
        query = """
            SELECT s.symptom_name, g.range_value, g.grade 
            FROM systemic_toxicity_symptoms s 
            JOIN systemic_toxicity_grades g ON s.id = g.symptom_id
        """
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def add_systemic_toxicity(self, data_dict):
        for symptom, grades in data_dict.items():
            self.cursor.execute(
                "INSERT INTO systemic_toxicity_symptoms (symptom_name) VALUES (%s)",
                (symptom,)
            )
            symptom_id = self.cursor.lastrowid
            for range_value, grade in grades.items():
                self.cursor.execute(
                    "INSERT INTO systemic_toxicity_grades (symptom_id, range_value, grade) VALUES (%s, %s, %s)",
                    (symptom_id, range_value, grade)
                )
        self.db_connection.commit()

    def get_treatment_recommendations(self, gender):
        query = """
            SELECT hemoglobin_state, hematological_state, systemic_toxicity, recommendation 
            FROM treatment_recommendations 
            WHERE gender = %s
        """
        self.cursor.execute(query, (gender,))
        return self.cursor.fetchall()

    def add_treatment_recommendations(self, gender, data_dict):
        for states, recommendations in data_dict.items():
            hemoglobin_state, hematological_state, systemic_toxicity = states
            for recommendation in recommendations:
                self.cursor.execute(
                    "INSERT INTO treatment_recommendations (gender, hemoglobin_state, hematological_state, systemic_toxicity, recommendation) VALUES (%s, %s, %s, %s, %s)",
                    (gender, hemoglobin_state[1], hematological_state[1], systemic_toxicity[1], recommendation)
                )
        self.db_connection.commit()

    def __del__(self):
        self.cursor.close()
        self.db_connection.close()


if __name__ == "__main__":
    kb = KnowledgeBase(host="localhost", user='root', password="q6rh3b", database="kb")

    # retrieve concepts
    # male_hemoglobin_levels = kb.get_concepts("male")
    # print(type(male_hemoglobin_levels))
    # for tuple in male_hemoglobin_levels:
    #      print(tuple)
    

    # retrieve treatment recommendations for males
    # male_treatment_recommendations = kb.get_treatment_recommendations("male")
    # for recommendation in male_treatment_recommendations:
        # print(recommendation)

    dict_ = {'Severe': ['male', '999-1000']}
    kb.add_concept('33',dict_)

    
    
