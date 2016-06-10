import sys
import csv
from bs4 import BeautifulSoup


def convert_to_csv():
    xml_arg = sys.argv[1]
    fanArray = []
    bsObj = BeautifulSoup(xml_arg)

    for item in bsObj.findAll('fan'):
        fanArray.append({'bill':str(item.get('billnum')),
                         'first_name':str(item.get('first_name')),
                         'last_name':str(item.get('last_name')),
                         'opinion':str(item.get('opinion')),
                         'posdate':str(item.get('posdate')),
                         'representing':str(item.get('representing'))})
        
    keys = fanArray[0].keys()
    with open('new_file.csv', 'w') as file:
        dict_writer = csv.DictWriter(file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(fanArray)

if __name__ == "__main__":
    convert_to_csv()
    print("Success!")
