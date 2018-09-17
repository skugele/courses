DROP TABLE IF EXISTS PATIENTS;
CREATE TABLE PATIENTS (
   PATIENT_ID   INT                    NOT NULL,  -- Unique identifier for a patient
   FIRST_NAME   VARCHAR (128)          NOT NULL,  -- Patient's first name
   LAST_NAME    VARCHAR (128)          NOT NULL,  -- Patient's last name
   DOB          DATE                   NOT NULL,  -- Patient's date of birth
   SEX          ENUM('MALE', 'FEMALE') NOT NULL,  -- Patient's sex
   PRIMARY KEY (PATIENT_ID)
);

INSERT INTO PATIENTS VALUES (1, 'Tony', 'Stark', '1970-05-29', 'MALE');
INSERT INTO PATIENTS VALUES (2, 'Stephen', 'Strange', '1930-11-18', 'MALE');
INSERT INTO PATIENTS VALUES (3, 'Natasha', 'Romanoff', '1928-01-01', 'FEMALE');
