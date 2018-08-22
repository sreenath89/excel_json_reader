import xlrd
import json
import boto3
import requests


def read_excel_file(file_name, sheet_name):
    '''Function to read the excel file contents

    Args:
        file_name  - name of excel file
        sheet_name - name of excel sheet whose data is to be scraped
    Returns:
        Contents from excel sheet saved in a json format
    '''

    # Fetching the contents from excel file
    contents = xlrd.open_workbook('/tmp/' + file_name)

    # Looping through each sheet
    for i in contents._sheet_list:
        # Validating the sheet name to fetch data
        if i.name == sheet_name:

            # Fetch data from the corresponding sheet
            data = contents.sheet_by_index(i.number)

            # Get total no. of columns and rows in the sheet
            total_col_count = data.ncols
            total_row_count = data.nrows

            # Initializing
            key_list = []
            row_list = []
            d = {}

            # Fetching the values from first row to use them as Keys
            for col_index in range(total_col_count):
                key = data.cell(0, col_index).value
                key_list.append(key)

            # Fetching the data from second row onwards and storing
            # them in a dict with values from first row as keys
            for row_index in range(1, total_row_count):
                d = {key_list[col_index]: data.cell(
                    row_index, col_index).value
                     for col_index in range(total_col_count)}
                row_list.append(d)

    # Store the dict data from excel in a json file
    j = json.dumps(row_list)
    return j


def create_json(file_contents):
    '''Function for creating the json file

    Args:
        file_contents - contents to be written into the json file

    Returns:
        Creates a json file with the required contents and save it in /tmp
    '''

    # Create json file for storing the output
    with open('/tmp/iso_output.json', 'w') as f:
        f.write(file_contents)
    return True


def upload_to_s3():
    '''Function to upload the json file contents to S3 bucket'''

    # Connect to AWS S3 and upload the file
    # Pass source file location, S3 bucket name and destination file name
    # (destination file name - to be used within S3)
    s3 = boto3.resource('s3')
    try:
        s3.meta.client.upload_file(
            '/tmp/iso_output.json', 'steeleyetest', 'miclist.json')
    except Exception as e:
        print(e)


def excel_json_handler(event, context):
    '''AWS Lambda Handler function'''

    # Pass the excel file url and name of sheet which is to be used
    excel_source_url = 'https://www.iso20022.org/sites/default/files/ISO10383_MIC/ISO10383_MIC.xls'
    excel_sheet_name = 'MICs List by CC'

    # Fetch data from excel file url and save in local destination
    r = requests.get(excel_source_url)
    excel_file_name = 'ISO10383_MIC.xls'
    with open('/tmp/' + excel_file_name, 'wb') as f:
        f.write(r.content)

    # Read data from excel sheet and convert it into json format
    file_contents = read_excel_file(excel_file_name, excel_sheet_name)
    try:
        create_json(file_contents)
    except Exception as e:
        print(e)
        print('failure')
        return False
    else:
        upload_to_s3()
        print('Success')
        return True
