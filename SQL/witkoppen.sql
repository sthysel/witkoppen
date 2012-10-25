DROP INDEX patient_pkey;

DROP TABLE patient.visit;
DROP TABLE patient.address;
DROP TABLE patient.contact;
DROP TABLE patient.source_error;
DROP TABLE patient.patient;

CREATE TABLE patient.patient (
       file_number INTEGER DEFAULT -1 NOT NULL
     , surname VARCHAR(128)
     , first_names VARCHAR(128)
     , birth_date VARCHAR(10)
     , gender VARCHAR(10) DEFAULT 'Undefined'
     , nationalID VARCHAR(20) DEFAULT ''
     , nationality VARCHAR(128) DEFAULT ''
     , note TEXT DEFAULT ''
     , callname VARCHAR(10) DEFAULT ''
     , language VARCHAR(20) DEFAULT ''
     , occupation VARCHAR(128) DEFAULT ''
     , ethnicity VARCHAR(100) DEFAULT ''
     , marital_status VARCHAR(12) DEFAULT 'Single'
     , dependants TEXT DEFAULT ''
     , employer VARCHAR(128) DEFAULT ''
     , PRIMARY KEY (file_number)
);

CREATE TABLE patient.source_error (
       file_number INTEGER
     , error TEXT
     , data TEXT
);

CREATE TABLE patient.contact (
       file_number INTEGER NOT NULL
     , contact_type VARCHAR(128) DEFAULT ''
     , info TEXT DEFAULT ''
     , CONSTRAINT FK_contact_1 FOREIGN KEY (file_number)
                  REFERENCES patient.patient (file_number)
);

CREATE TABLE patient.address (
       file_number INTEGER
     , description VARCHAR(128)
     , lines TEXT
     , code VARCHAR(10)
     , CONSTRAINT FK_address_1 FOREIGN KEY (file_number)
                  REFERENCES patient.patient (file_number)
);

CREATE TABLE patient.visit (
       file_number INTEGER NOT NULL
     , visit_date VARCHAR(10)
     , note TEXT DEFAULT ''
     , CONSTRAINT FK_visit_1 FOREIGN KEY (file_number)
                  REFERENCES patient.patient (file_number)
);

