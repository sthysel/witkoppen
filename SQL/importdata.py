#! /usr/bin/env python2.4

import sys
import psycopg
import csv

errorfile = open("errorlog.txt", 'w')
writer = csv.writer(open("witkoppen-cleaned.csv", "w"))

def main():
    conn = connectToDB()
    cur = conn.cursor()    
    filename = getFileName()
    print "Importing Patient data from %s" % filename

    errcnt = 0
    err = None
    
    reader = csv.reader(open(filename), delimiter=",")
    for data in reader:
        fileno, surname, firstname, birthdate, contact, lastvisitdate = data[:6]

        err = None
        # ignore lines that does not start with a file number
        try:
            fileno = int(fileno)
        except ValueError:
            continue
            
        
        if surname: surname = surname.strip()
        if firstname: firstname = firstname.strip()
        if birthdate:  birthdate = birthdate.strip()
        else: birtdate = None
        if contact: contact = contact.strip()
        else: contact = None
        if lastvisitdate: lastvisitdate = lastvisitdate.strip()
        else: birthdate = None
        
        have_birth = """
        insert into patient.patient (file_number, surname, first_names, birth_date)
        values (%d, '%s', '%s', '%s')    
        """ % (fileno, surname, firstname, birthdate)

        no_birth = """
        insert into patient.patient (file_number, surname, first_names)
        values (%d, '%s', '%s')    
        """ % (fileno, surname, firstname)
        
        visit = """
        insert into patient.visit (file_number, visit_date)
        values (%d, '%s')    
        """ % (fileno, lastvisitdate)
        
        # contact
        contactQ = """
        insert into patient.contact (file_number, contact_type, info)
        values (%d, 'Patient Cell', '%s')    
        """ % (fileno, contact)

        

        err = None        
        try:    
            # patient data
            if birthdate:
                cur.execute(have_birth)
            else:
                cur.execute(no_birth)            
            # visits
            if lastvisitdate:
                cur.execute(visit)
            # contact
            if contact:  
                # print "[%s]" % contact              
                cur.execute(contactQ)
            
            writer.writerow((fileno, surname, firstname, birthdate, contact, lastvisitdate))

        except psycopg.IntegrityError, x:
            errcnt += 1
            err = x

        except psycopg.ProgrammingError, x:
            errcnt += 1
            err = x
        
        if err:
            conn.commit()
            err = str(err).split('\n')[0]
            errorQ = """
            insert into patient.source_error (file_number, error, data)
            values (%d, '%s', '%s')    
            """ % (fileno, err, ";".join(data))
            cur.execute(errorQ)
            
            errorfile.write(" ".join(data) + '\n')
            
        
        conn.commit()
    print errcnt

            
def connectToDB():
    try:
        return psycopg.connect("dbname='witkoppen' user='witkoppen' host='localhost' password='witkoppen'");
    except:
        print "Unable to connect to the database"
        sys.exit()

def getFileName():
    if len(sys.argv) != 2:
        print "Please specify data file on search line."
        sys.exit()
        
    return sys.argv[1]
        
if __name__ == "__main__":
    main()
