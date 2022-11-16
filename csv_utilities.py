import logging
import logging_utility

import random

import config


# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import pandas as pd
import matplotlib.pyplot as plt

# TODO: Refactoring to CLASS?: to have as inner property or in constructor
#  the filaname, delimiter, dataframe... This would make sense to instantiate the csv reader
#   in the constructor


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    logging.info(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


def read_csv(file_name,delimiter):
    # See: https://realpython.com/python-csv/
    #      > It is possible to use the csv library, however, for csv parsing is more convenient to use pandas
    # In case the csv file does not have a header, then add after delimiter
    # a list with the header names: names=['Username','Identifier','First name','Last name'}
    # dataframe = pd.read_csv(file_name, delimiter=',')
    # https://www.analyticsvidhya.com/blog/2021/04/delimiters-in-pandas-read_csv-function/
    # It seems quote character is not supported by panda, then import using csv module and then load to panda:
    #       https://stackoverflow.com/questions/26595819/double-quoted-elements-in-csv-cant-read-with-pandas
    dataframe = pd.read_csv(file_name, delimiter=delimiter)

    # logging.info(dataframe.toString())
    return dataframe

def read_row(dataframe,row_index):
    row_result=dataframe.loc[row_index]
    logging.info('-------------------------------------------')
    logging.info(f'Display line at index={row_index} :  {row_result}')
    return row_result

def read_column(dataframe,column_name):
    column_result=dataframe[column_name]
    logging.info('-------------------------------------------')
    logging.info(f'Display column with name: {column_name}:\n\r{column_result}')
    return column_result

def read_two_columns(dataframe,column_name1, column_name2):
    column_result=dataframe[[column_name1,column_name2]]
    logging.info('-------------------------------------------')
    logging.info(f'Display columns {column_name1}-{column_name2}:\n\r{column_result}')
    return column_result

def show_info_of_data(dataframe):
    logging.info('-------------------------------------------')
    info_of_data=dataframe.info()
    logging.info(f'Info of data: {info_of_data}')

def filter_lastname(dataframe, lastname):
    logging.info('-------------------------------------------')
    columnname='Lastname'
    # IMPORTANT Limitation of Pandas:
    #    -> It seems it is not possible to have spaces in columns
    #    -> At dataframe.columnname, columnname cannot be a string!
    filtered_user=dataframe[dataframe.Lastname==lastname]
    logging.info(f'Filtered user for {lastname}:\n\r{filtered_user}')

def list_header_columns(dataframe):
    logging.info('---------------------------------------------')
    header_columns=dataframe.columns
    logging.info(f'Header columns: {header_columns.to_list()}')
    # Index 0 is for the first column
    return header_columns

def count_rows(dataframe):
    logging.info('-----------------------------------------------')
    count_rows=len(dataframe)
    logging.info(f'CSV file has {count_rows} rows')
    return count_rows

def show_all_rows_columns(dataframe):
    logging.info('------------------------------------------------')
    rows_columns=dataframe.to_string();
    logging.info(f'Showing all rows and columns of csv file:\n\r{rows_columns}')
    return rows_columns

def shape_of_file(dataframe):
    logging.info('------------------------------------------------')
    shape=dataframe.shape
    logging.info(f'CSV file has as shape (rows, columns): {shape}')
    # Row containing header is not included
    return shape

def add_row(dataframe):
    # https: // www.statology.org / pandas - add - row - to - dataframe /
    # Read for delete row: https://towardsdatascience.com/delete-rows-and-columns-from-a-dataframe-using-pandas-drop-d2533cf7b4bd
    username='aznarin'
    identifier='1234'
    firstname='Jose Mari'
    lastname='Aznar'
    amountOfAccesses=38383
    row_to_add=[username,amountOfAccesses,identifier,firstname,lastname]
    # row_to_add = [username, identifier, firstname, lastname]
    dataframe.loc[len(dataframe.index)]=row_to_add

def add_new_column(dataframe, newcolumnname):
    logging.info('-----------------------------------------')
    # https: // www.geeksforgeeks.org / python - pandas - dataframe - insert /
    # DataFrameName.insert(loc, column, value, allow_duplicates = False)
    #       loc: integer is the position at which the new column should be inserted
    #       column: string containing the name of the column
    #       value: value to be inserted -> list. If provided only one value, then same
    #                   value is inserted for all rows
    #       allow duplicates: boolean
    dataframe.insert(1,newcolumnname,0,True)
    logging.info(f'OK: new column: {newcolumnname} inserted')


def persist_dataframe(dataframe, filepath):
    # https://towardsdatascience.com/stop-persisting-pandas-data-frames-in-csvs-f369a6440af5
    # https: // towardsdatascience.com / how - to - export - pandas - dataframe - to - csv - 2038e43
    # d9c03
    logging.info('-----------------------------------------------')
    dataframe.to_csv(filepath, index=False)
    #    Possible parameters: index=False, encoding='utf-8',
    logging.info(f'OK: Dataframe persisted at filepath: {filepath}')

def update_column(dataframe, nameOfColumn):
    # https://www.easytweaks.com/update-values-dataframe-pandas-python/
    logging.info('------------------------------------------------')
    logging.info(' This function looks all rows that have less than 10 accesses'
          'and updates amountOfAccesses with a random int')
    users_with_less_than_10_accesses = dataframe['amountOfAccesses']<10
    dataframe.loc[users_with_less_than_10_accesses,'amountOfAccesses']=random.randrange(5,300)

    logging.info(f'OK:Edited column {nameOfColumn} ')

def update_value(dataframe, rowIndex, nameOfColumn, valueToUpdate):
    logging.info('-----------------------------------------------')
    # https: // re - thought.com / how - to - change - or -update - a - cell - value - in -python - pandas - dataframe /
    #   it seems it is not possible to update using .loc, you need to use at!
        # row_result = dataframe.loc[rowIndex]
        # previousValue = row_result[nameOfColumn]
        # row_result[nameOfColumn]=valueToUpdate
        # dataframe.loc[rowIndex][nameOfColumn] = valueToUpdate
    # This works by using .at:
    previousValue=dataframe.at[rowIndex,nameOfColumn]
    dataframe.at[rowIndex,nameOfColumn]=valueToUpdate
    updatedCellValueCheck=dataframe.loc[rowIndex][nameOfColumn]
    logging.info(f'OK Updated value:  Previous value for rowIndex={rowIndex}, columnName={nameOfColumn} -> Value={previousValue} -> Updated value={updatedCellValueCheck} ')
    return dataframe

def plot(dataframe):
    logging.info('-----------------------------------------------')
    dataframe.plot()
    plt.show()
    logging.info('Plotting dataframe')


# Press the green button in the gutter to run the script.
# if __name__ == '__main__':
def main_method():
    try:
        print_hi('PyCharm')
        # logger=configure_logging('log.txt')
        logger=logging_utility.configure_logging(config.log_file)
        logger.info("Testing the logger")
        # file_name = 'username2.csv'
        file_name=config.file_name
        # file_name2=config.file_name2
        dataframe=read_csv(file_name,config.delimiter)

        # read_row(dataframe,3)
        show_info_of_data(dataframe)
        read_column(dataframe, 'Username')
        read_two_columns(dataframe,'Identifier','Lastname')
        filter_lastname(dataframe,'Johnson')
        columns=list_header_columns(dataframe)
        logging.info(f'Column at index 2 is: {columns[2]}')
        count_rows(dataframe)
        shape_of_file(dataframe)
        add_row(dataframe)
        show_info_of_data(dataframe)
        filter_lastname(dataframe, 'Aznar')
        show_all_rows_columns(dataframe)
        # add_new_column(dataframe,'amountOfAccesses')
        update_column(dataframe, 'amountOfAccesses')
        dataframe=update_value(dataframe, 5, "Username", 'Pelusso')
        # plot(dataframe)
        persist_dataframe(dataframe,file_name)
        show_all_rows_columns(dataframe)
        logging.info('Script finished OK')
    except Exception as e:
        logging.exception(e)

# main_method()