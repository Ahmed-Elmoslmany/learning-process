import csv
import os

class Csv():
    def __init__(self, filename, fields, data):
        self.filename = f'{filename}.csv'
        self.fields = fields
        self.data = data
        

    def generate(self):
        try:
            with open(self.filename, 'w') as csvfile:
                csvwriter = csv.writer(csvfile)

                csvwriter.writerow(self.fields)
                csvwriter.writerows(self.data)
                return True
        except:
            return False
        

    def get_file_path(self):
        return f'{os.getcwd()}/{self.filename}'

