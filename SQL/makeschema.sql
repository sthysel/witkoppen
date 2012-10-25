-- Creating the witkoppen schemas and associated tables

DROP SCHEMA patient CASCADE;

CREATE SCHEMA patient AUTHORIZATION witkoppen;
COMMENT ON SCHEMA patient IS 'Contains Patient related tables';

CREATE TABLE patient.patient
(
  file_number int4 NOT NULL DEFAULT -1,
  surname text,
  first_names text,
  birth_date date DEFAULT NULL,
  contact_no text,
  last_visit date
) 
WITHOUT OIDS;
ALTER TABLE patient.patient OWNER TO witkoppen;
COMMENT ON TABLE patient.patient IS 'Patients';
ALTER TABLE patient.patient
  ADD CONSTRAINT patient_pkey PRIMARY KEY(file_number);

