from heatmapr import pyodbc


class dbconnection:
    def __init__ (self,metadict):
        self.print_sql=True
        self.exec_sql=True
        self.open_server(metadict)

        
    def open_server (self, metadict):
        s='Driver={%(driver)s};SERVER=%(server)s;DATABASE=%(database)s;uid=%(username)s;pwd=%(password)s' % metadict        
        dbc = pyodbc.connect(s)     # open a database connection
        dbc.autocommit=True
        hnd=dbc.cursor()
        self.dbc=dbc
        self.hnd=hnd
        self.driver=metadict['driver']
        self.server=metadict['server']
        self.database=metadict['database']
        return dbc, hnd


    def run_sql (self, sql):        
        if self.print_sql:
            print sql
  
        if self.exec_sql:            
            self.hnd.execute(sql)
            self.dbc.commit()
