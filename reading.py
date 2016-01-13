# Functions for reading tables and databases

import glob
from database import *

# a table is a dict of {str:list of str}.
# The keys are column names and the values are the values
# in the column, from top row to bottom row.

# A database is a dict of {str:table},
# where the keys are table names and values are the tables.


# Write the read_table and read_database functions below

def read_table(filename):
    '''The function returns a Table object.'''
    table = Table()
    table.file_to_table(filename)
    return table


def read_database():
    '''This function reads each file and returns a Database object
    representing all of the data in all of the csv files.'''
    file_list = glob.glob('*.csv')
    db = Database()
    db.set_dbdict(file_list)
    return db
