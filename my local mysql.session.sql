
DROP TABLE IF EXISTS hemoglobin_range, hematological_ranges, hematological_states, systemic_toxicity_symptoms, systemic_toxicity_grades,
                    treatment_recommendations;

CREATE TABLE hemoglobin_range(
    id INT PRIMARY KEY,
    sex VARCHAR(255) NOT NULL,
    category VARCHAR(255) NOT NULL,
    range_value VARCHAR(255) NOT NULL,
    good_after DATETIME,
    good_before DATETIME
);

INSERT INTO hemoglobin_range (id, sex, category, range_value, good_after, good_before) VALUES
(1, 'male', 'Severe Anemia', '0-8 mg/100cc'),
(2, 'male','Moderate Anemia', '8-10 mg/100cc'),
(3, 'male','Mild Anemia', '10-12 mg/100cc'),
(4, 'male','Normal Hemoglobin', '12-14 mg/100cc'),
(5, 'male','Polycytemia', '14+ mg/100cc'),
(6, 'female', 'Severe Anemia', '0-9 mg/100cc'),
(7, 'female', 'Moderate Anemia', '9-11 mg/100cc'),
(8, 'female', 'Mild Anemia', '11-13 mg/100cc'),
(9, 'female', 'Normal Hemoglobin', '13-16 mg/100cc'),
(10, 'female', 'Polycythemia', '16+ mg/100cc');

CREATE TABLE hematological_states (
    id INT PRIMARY KEY,
    gender VARCHAR(10) NOT NULL,
    state_name VARCHAR(255) NOT NULL
);

-- male hematological_states
INSERT INTO hematological_states (id, gender, state_name) VALUES
(1, 'male', 'Pancytopenia'),
(2, 'male', 'Leukopenia'),
(3, 'male', 'Suspected Polycytemia Vera'),
(4, 'male', 'Anemia'),
(5, 'male', 'Normal'),
(6, 'male', 'Polyhemia'),
(7, 'male', 'Suspected Leukemia'),
(8, 'male', 'Leukemoid reaction'),
(9, 'male', 'Suspected Polycytemia Vera');

-- female hematological_states
INSERT INTO hematological_states (id, gender, state_name) VALUES
(10, 'female', 'Pancytopenia'),
(11, 'female', 'Leukopenia'),
(12, 'female', 'Suspected Polycytemia Vera'),
(13, 'female', 'Anemia'),
(14, 'female', 'Normal'),
(15, 'female', 'Polyhemia'),
(16, 'female', 'Suspected Leukemia'),
(17, 'female', 'Leukemoid reaction'),
(18, 'female', 'Suspected Polycytemia Vera');


CREATE TABLE hematological_ranges (
    id INT PRIMARY KEY,
    state_id INT NOT NULL,
    hemoglobin_range VARCHAR(50) NOT NULL,
    wbc_range VARCHAR(50) NOT NULL,
    FOREIGN KEY (state_id) REFERENCES hematological_states(id)
);

-- male WBC and HEMOGLOBIN LEVEL data
INSERT INTO hematological_ranges (id, state_id, hemoglobin_range, wbc_range) VALUES
(1, 1, '0-13', '0-4000'),
(2, 2, '13-16', '0-4000'),
(3, 3, '16+', '0-4000'),
(4, 4, '0-13', '4000-10000'),
(5, 5, '13-16', '4000-10000'),
(6, 6, '16+', '4000-10000'),
(7, 7, '0-13', '10000+'),
(8, 8, '13-16', '10000+'),
(9, 9, '16+', '10000+');

-- female WBC and HEMOGLOBIN LEVEL data
INSERT INTO hematological_ranges (id, state_id, hemoglobin_range, wbc_range) VALUES
(10, 10, '0-12', '0-4000'),
(11, 11, '12-14', '0-4000'),
(12, 12, '14+', '0-4000'),
(13, 13, '0-12', '4000-10000'),
(14, 14, '12-14', '4000-10000'),
(15, 15, '14+', '4000-10000'),
(16, 16, '0-12', '10000+'),
(17, 17, '12-14', '10000+'),
(18, 18, '14+', '10000+');


CREATE TABLE systemic_toxicity_symptoms (
    id INT PRIMARY KEY,
    symptom_name VARCHAR(255) NOT NULL
);

INSERT INTO systemic_toxicity_symptoms (id, symptom_name) VALUES
(1, 'Fever'),
(2, 'Chills'),
(3, 'Skin-look'),
(4, 'Allergic-state');

CREATE TABLE systemic_toxicity_grades (
    id INT PRIMARY KEY,
    symptom_id INT NOT NULL,
    range_value VARCHAR(50) NOT NULL,
    grade VARCHAR(50) NOT NULL,
    FOREIGN KEY (symptom_id) REFERENCES systemic_toxicity_symptoms(id)
);

INSERT INTO systemic_toxicity_grades (id, symptom_id, range_value, grade) VALUES
(1, 1, '0-38.5', 'Grade I'),
(2, 1, '38.5-40.0', 'Grade II'),
(3, 1, '40.0+', 'Grade III'),
(4, 1, '40.0', 'Grade IV'),
(5, 2, 'None', 'Grade I'),
(6, 2, 'Shaking', 'Grade II'),
(7, 2, 'Rigor', 'Grade III'),
(8, 2, 'Rigor', 'Grade IV'),
(9, 3, 'Erythema', 'Grade I'),
(10, 3, 'Vesiculation', 'Grade II'),
(11, 3, 'Desquamation', 'Grade III'),
(12, 3, 'Exfoliation', 'Grade IV'),
(13, 4, 'Edema', 'Grade I'),
(14, 4, 'Bronchospasm', 'Grade II'),
(15, 4, 'Severe-Bronchospasm', 'Grade III'),
(16, 4, 'Anaphylactic-Shock', 'Grade IV');


CREATE TABLE treatment_recommendations (
    id INT PRIMARY KEY,
    gender VARCHAR(10) NOT NULL,
    hemoglobin_state VARCHAR(255) NOT NULL,
    hematological_state VARCHAR(255) NOT NULL,
    systemic_toxicity VARCHAR(255) NOT NULL,
    recommendation TEXT NOT NULL
);

INSERT INTO treatment_recommendations (id, gender, hemoglobin_state, hematological_state, systemic_toxicity, recommendation) VALUES
(1, 'male', 'Severe Anemia', 'Pancytopenia', 'GRADE I', 'Measure BP once a week'),
(2,'male', 'Moderate Anemia', 'Anemia', 'GRADE II', 'Measure BP every 3 days'),
(3,'male', 'Moderate Anemia', 'Anemia', 'GRADE II', 'Give aspirin 5g twice a week'),
(4,'male', 'Mild Anemia', 'Suspected Leukemia', 'GRADE III', 'Measure BP every day'),
(5,'male', 'Mild Anemia', 'Suspected Leukemia', 'GRADE III', 'Give aspirin 15g every day'),
(6,'male', 'Mild Anemia', 'Suspected Leukemia', 'GRADE III', 'Diet consultation'),
(7,'male', 'Normal Hemoglobin', 'Leukemoid reaction', 'GRADE IV', 'Measure BP twice a day'),
(8,'male', 'Normal Hemoglobin', 'Leukemoid reaction', 'GRADE IV', 'Give aspirin 15g every day'),
(9,'male', 'Normal Hemoglobin', 'Leukemoid reaction', 'GRADE IV', 'Exercise consultation'),
(10,'male', 'Normal Hemoglobin', 'Leukemoid reaction', 'GRADE IV', 'Diet consultation'),
(11,'male', 'Polyhemia', 'Suspected Polycytemia Vera', 'GRADE IV', 'Measure BP every hour'),
(12,'male', 'Polyhemia', 'Suspected Polycytemia Vera', 'GRADE IV', 'Give 1 gr magnesium every hour'),
(13,'male', 'Polyhemia', 'Suspected Polycytemia Vera', 'GRADE IV', 'Exercise consultation'),
(14,'male', 'Polyhemia', 'Suspected Polycytemia Vera', 'GRADE IV', 'Call family');

INSERT INTO treatment_recommendations (id, gender, hemoglobin_state, hematological_state, systemic_toxicity, recommendation) VALUES
(15,'female', 'Severe Anemia', 'Pancytopenia', 'GRADE I', 'Measure BP every 3 days'),
(16,'female', 'Moderate Anemia', 'Anemia', 'GRADE II', 'Measure BP every 3 days'),
(17,'female', 'Moderate Anemia', 'Anemia', 'GRADE II', 'Give Celectone 2g twice a day for two days drug treatment'),
(18,'female', 'Mild Anemia', 'Suspected Leukemia', 'GRADE III', 'Measure BP every day'),
(19,'female', 'Mild Anemia', 'Suspected Leukemia', 'GRADE III', 'Give 1 gr magnesium every 3 hours'),
(20,'female', 'Normal Hemoglobin', 'Leukemoid reaction', 'GRADE IV', 'Measure BP twice a day'),
(21,'female', 'Normal Hemoglobin', 'Leukemoid reaction', 'GRADE IV', 'Give 1 gr magnesium every hour'),
(22,'female', 'Normal Hemoglobin', 'Leukemoid reaction', 'GRADE IV', 'Exercise consultation'),
(23,'female', 'Normal Hemoglobin', 'Leukemoid reaction', 'GRADE IV', 'Diet consultation'),
(24,'female', 'Polyhemia', 'Suspected Polycytemia Vera', 'GRADE IV', 'Measure BP every hour'),
(25,'female', 'Polyhemia', 'Suspected Polycytemia Vera', 'GRADE IV', 'Give 1 gr magnesium every hour'),
(26,'female', 'Polyhemia', 'Suspected Polycytemia Vera', 'GRADE IV', 'Exercise consultation'),
(27,'female', 'Polyhemia', 'Suspected Polycytemia Vera', 'GRADE IV', 'Call help');



