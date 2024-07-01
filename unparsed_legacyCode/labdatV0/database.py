import sqlite3, os
import tools as t

class Request:
    def __init__(self):
        return
    
class Database:
    path = r'Z:\database'

    def __init__(self, name: str='data', path: str = path):
        self.path   = f'{path}\\{name}.db'
        self.name   = name

        try: os.mkdir(path)
        except: 1
    
    def Open(self):
        self.con    = sqlite3.connect( self.path )
        self.cur    = self.con.cursor()
    
    def Close(self): self.con.close()

    def Request(self, request, data=None, commit=False, fetch=False, description=False, openDB = True):
        if openDB: self.Open()

        if data:    response = self.cur.executemany(request, t.Class2SQL(data))
        else:       response = self.cur.execute(request)

        if commit: self.con.commit()

        if fetch and description:   response = (response.fetchall(), response.description)
        elif fetch:                 response = response.fetchall()
        elif description:           response = response.description
        else: response = None

        if openDB: self.Close()
        return response

    def NewTable(self, table: str, data): self.Request(f"create table if not exists '{table}' ({t.CommaString(t.Keys(data))} primary key)")

    def Insert(self, table: str, data):
        if type(data) is list: first   = data[0]
        else: first   = data
        
        self.NewTable(table, first)
        self.Request(f"INSERT or REPLACE INTO '{table}' VALUES ({t.Q(first)});", data= data, commit= True)

    def Tables(self): return t.Flatten( self.Request("SELECT name FROM sqlite_master WHERE type='table';", fetch= True) )
    def Columns(self, table: str): return [d[0] for d in self.Request(f'SELECT * FROM {table}', description=True)]
    def Function(self, table:str, column: str, fun: str): return t.Flatten(self.Request(f'SELECT {fun}({column}) FROM {table}', fetch=True))

    def Get(self, table: str, column = '*', filter = None, order = None, join = None, group = None, group_filter = None, listRows = False):
        request = f"SELECT {column} FROM '{table}'"
        if join:            request += AddArgument('INNER JOIN', join)
        if filter:          request += AddArgument('WHERE', filter, connector= ' AND ')
        if group:           request += AddArgument('GROUP BY', group)
        if group_filter:    request += AddArgument('HAVING', group_filter)
        if order:           request += AddArgument('ORDER BY', order)
        request += ';'

        # print(request)
        response = self.Request(request, fetch=True, description=True)
        header = [d[0] for d in response[1]]

        if listRows:    return {h:[r[i] for r in response[0]] for i,h in enumerate(header)}
        else:           return [{h:r[i] for i,h in enumerate(header)} for r in response[0]]
    
def AddArgument(var, val, connector=', ', enclose = False):
    if type(val) is list: val = f"{ connector.join(val) }"
    if enclose: val = f'({val})'
    return f' {var} {val}'

def Contains(substr): return f"GLOB '*{substr}*'"


    