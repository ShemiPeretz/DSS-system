USE patient_data;

-- Drop the existing tables if they exist
DROP TABLE IF EXISTS test_results;

-- Create the unified table
CREATE TABLE test_results (
    id INT PRIMARY KEY,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    loinc_num VARCHAR(50) NOT NULL,
    value VARCHAR(50) NOT NULL,
    unit VARCHAR(50),
    valid_start_time DATETIME,
    transaction_time DATETIME
);

-- Insert data directly into the unified table
-- INSERT INTO test_results (id, first_name, last_name, loinc_num, value, unit, valid_start_time, transaction_time) VALUES
-- (1, 'Eyal', 'Rothman', '11218-5', 4500, 'cells/ml', '2018-05-17 13:11:00', '2018-05-27 10:00:00'),
-- (2, 'Eyal', 'Rothman', '11218-5', 4450, 'cells/ml', '2018-05-17 13:11:00', '2018-05-28 10:00:00'),
-- (3, 'Eli', 'Call', '11218-5', 5500, 'cells/ml', '2018-05-18 15:00:00', '2018-05-21 10:00:00'),
-- (4, 'Eyal', 'Rothman', '11218-5', 5000, 'cells/ml', '2018-05-17 17:00:00', '2018-05-20 10:00:00'),
-- (5, 'Eyal', 'Rothman', '11218-5', 5500, 'cells/ml', '2018-05-18 11:00:00', '2018-05-21 10:00:00'),
-- (6, 'Eyal', 'Rothman', '11218-5', 4400, 'cells/ml', '2018-05-18 13:00:00', '2018-05-28 10:00:00');
