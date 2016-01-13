class Table():
    '''A class to represent a SQuEaL table'''

    def __init__(self):
        self.tdict = {}
        

    def file_to_table(self, filename):
        '''Generate a dictionary representation according to the specified file.'''
        with open(filename) as f:
            text_list = [[e.strip() for e in text.strip().split(',')] for text in f]
        col_list = map(list, zip(*text_list))
        self.tdict = {i[0]:i[1:] for i in col_list}


    def table_to_table(self, table):
        '''(Table, Table) -> NoneType
        Populate this table with another table.'''
        for key in table.tdict.keys():
            self.tdict[key] = table.tdict[key][:]


    def dict_to_table(self, table_dict):
        '''same as fuction set_dict
        (Table, dict of {str: list of str}) -> NoneType
        Populate this table with the data in new_dict.
        The input dictionary must be of the form:
            column_name: list_of_values
        '''
        for key in table_dict.keys():
            self.tdict[key] = table_dict[key][:]


    def del_row(self, row):
        '''Delete the specified row from the table.'''
        for key in self.tdict.keys():
            self.tdict[key].pop(row)


    def del_col(self, col_key):
        '''Delete the specified column from the table.'''
        self.tdict.pop(col_key)
    

    def set_dict(self, new_dict):
        '''(Table, dict of {str: list of str}) -> NoneType
        Populate this table with the data in new_dict.
        The input dictionary must be of the form:
            column_name: list_of_values
        '''
        for key in new_dict.keys():
            self.tdict[key] = new_dict[key][:]


    def get_dict(self):
        '''(Table) -> dict of {str: list of str}
        Return the dictionary representation of this table. The dictionary keys
        will be the column names, and the list will contain the values
        for that column.
        '''
        return self.tdict



class Database():
    '''A class to represent a SQuEaL database'''

    def __init__(self):
        self.dbdict = {}

        
    def set_dbdict(self, file_list):
        '''Generate a dictionary according to the specified file lists.'''
        self.dbdict = {}
        for each in file_list:
            table = Table()
            table.file_to_table(each)
            self.dbdict[each[:-4]] = table
            

    def set_dict(self, new_dict):
        '''(Database, dict of {str: Table}) -> NoneType

        Populate this database with the data in new_dict.
        new_dict must have the format:
            table_name: table
        '''
        for key in new_dict.keys():
            self.dbdict[key] = new_dict[key][:]
        

    def get_dict(self):
        '''(Database) -> dict of {str: Table}

        Return the dictionary representation of this database.
        The database keys will be the name of the table, and the value
        with be the table itself.
        '''
        return self.dbdict
