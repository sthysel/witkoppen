
import psycopg
import time

from Peripherals.BarWriter import BARWRITER
from Registry import Registry
from Data import Result

CS = "dbname=witkoppen host=localhost user=witkoppen password=witkoppen"

class Connect:
    def __init__(self):
        
        self.conn = None
        self.lastSearchData = None # last search criteria
        
        try:
            self.conn = psycopg.connect(CS)
        except psycopg.OperationalError, x:
            print x
            
    def saveBio(self, data):
        """ save biography data """
        
        query = """
        update patient.patient
        set surname='%(surname)s',
            first_names='%(first_names)s',
            birth_date='%(birth_date)s',
            gender='%(gender)s',
            nationalid='%(nationalid)s',
            nationality='%(nationality)s',
            note='%(note)s',
            callname='%(callname)s',
            language='%(language)s',
            occupation='%(occupation)s',
            marital_status='%(marital_status)s',
            dependants='%(dependants)s',
            ethnicity='%(ethnicity)s',
            employer='%(employer)s'
        where patient.file_number='%(file_number)d'        
        """ % data
        
        # print query
        
        cursor = self.conn.cursor()
        cursor.execute(query)
        self.conn.commit()
        
        if self.lastSearchData:
            res = self.search(self.lastSearchData)
            Registry.get("SEARCH").presentResult()
            
            
    def search(self, data):
        """search database """
        
        self.lastSearchData = data
        
        query = """
        select * from patient.patient where """
        
        filenoquery = "file_number=%(folderno)s" % data
        surnamequery = "surname ~* '%(surname)s'" % data
        firstnamequery = "first_names ~* '%(name)s'" % data
        bdatequery = "birth_date ~* '%(bdate)s'" % data
        
        post = """
        order by surname desc
        limit 50
        """ 
        
        qlist = []
        if data["folderno"]:
            qlist.append(filenoquery)
        if data["surname"]:
            qlist.append(surnamequery)
        if data["name"]:
            qlist.append(firstnamequery)
        if data["bdate"]:
            qlist.append(bdatequery)   
        
        if len(qlist) > 1:
            mq = " and ".join(qlist)
        elif len(qlist) != 0: 
            mq = qlist[0]
        else:
            BARWRITER.write("No Matches Found")
            return []
            
        
        q = query + mq + post
        
        cursor = self.conn.cursor()
        cursor.execute(q)
        
        # set the rusult 
        Result.setResult(cursor.dictfetchall())
        BARWRITER.write("Save Completed at %s" %  time.ctime())
            
    def addnewBioEntry(self, data):
        """add new DB entry"""
        
        query = """
        insert into patient.patient
        (file_number, surname, first_names, birth_date,
         gender, nationalid, nationality,
         note, callname, language, occupation, marital_status,
         ethnicity, employer)

         values(%(file_number)d, '%(surname)s', '%(first_names)s', '%(birth_date)s', '%(gender)s', '%(nationalid)s',
                '%(nationality)s', '%(note)s', '%(callname)s', '%(language)s', '%(occupation)s', '%(marital_status)s',
                '%(ethnicity)s', '%(employer)s')
        """ % data
        
        # print query
        
        try:
            cursor = self.conn.cursor()
            cursor.execute(query)
            self.conn.commit()
        except psycopg.IntegrityError, x:
            msg = "Failed to Add entry,\nFile Number %d already in use" % data['file_number']
            from Dialogs.Utils import displayMessage
            displayMessage(msg)
            BARWRITER.write(msg)
            return
        
        if self.lastSearchData:
            res = self.search(self.lastSearchData)
            Registry.get("SEARCH").presentResult()
            
        BARWRITER.write("New Entry Added at %s" %  time.ctime())
        
    def deleteEntry(self, folderNo):
        """ delete the folder from the database"""
        
        query = """
        delete from patient.contact where file_number='%(file_number)d';
        delete from patient.visit where file_number='%(file_number)d';
        delete from patient.patient where file_number='%(file_number)d';
        """ % {"file_number":folderNo}
        
        cursor = self.conn.cursor()
        cursor.execute(query)
        self.conn.commit()
        
    def saveContacts(self, file_number, data):
        """ save contacts"""
                
        query = """
        delete from patient.contact where file_number=%d;
        """ % file_number
                
        cursor = self.conn.cursor()
        cursor.execute(query)
        self.conn.commit()
        
        for e in data:
            query = """
            insert into patient.contact (file_number, contact_type, info) 
            values (%d, '%s', '%s')
            """ % (file_number, str(e[0]), str(e[1]))
        
            cursor = self.conn.cursor()
            cursor.execute(query)
            self.conn.commit()
        
    def getContacts(self, file_number):
        """ list of contacts"""
        
        query = """
        select contact_type, info from patient.contact
        where file_number=%d
        """ % file_number
        
        cursor = self.conn.cursor()
        cursor.execute(query)
        
        return cursor.fetchall()
    
    def saveAddress(self, file_number, data):
        """ save addresses"""
        
        query = """
        delete from patient.address where file_number=%d;
        """ % file_number
                
        cursor = self.conn.cursor()
        cursor.execute(query)
        self.conn.commit()
        
        for e in data:
            query = """
            insert into patient.address (file_number, description, lines, code) 
            values (%d, '%s', '%s', '%s')
            """ % (file_number, str(e[0]), str(e[1]), str(e[2]))
        
            cursor = self.conn.cursor()
            cursor.execute(query)
            self.conn.commit()
    
    def getAddresses(self, file_number):
        """ get list of addresses"""
        
        query = """
        select description, lines, code from patient.address
        where file_number=%d
        """ % file_number
        
        cursor = self.conn.cursor()
        cursor.execute(query)
        
        return cursor.dictfetchall()
    
    def getVisits(self, file_number):
        """ return dict of visits """
        
        query = """
        select visit_date, note from patient.visit
        where file_number=%d
        """ % file_number
        
        cursor = self.conn.cursor()
        cursor.execute(query)

        visits = {}
        for e in cursor.fetchall():
            visits[e[0]] = e[1]
        return visits
        
    def saveVisits(self, file_number, data):
        """ save modified visits"""
        

        for k, v in data.items():
            if k.find('-NEW') != -1:
                query = """
                insert into patient.visit (file_number, visit_date, note)
                values(%d, '%s', '%s')
                """ % (file_number, str(k[:-4]), str(v))
                print query
                cursor = self.conn.cursor()
                cursor.execute(query)
                self.conn.commit()
            
            else:
                query = """
                update patient.visit set note='%s'
                where (file_number=%d and visit_date='%s')
                """ % (str(v), file_number, str(k))
                print query
                cursor = self.conn.cursor()
                cursor.execute(query)
                self.conn.commit()

        
        
        
        
        
CONN = Connect()
