from datetime import datetime
import csv
import os.path

class Write:

    __file = None

    def write_file(self, test_data, file_name):
        # filename = f"{datetime.now():%Y-%m-%d_%H:%M:%S}.csv"
        self.file_name = file_name
        if os.path.isfile(r"/home/studentas/Documents/python/OpenVPN_speed_test/Test_report/" + self.file_name + ".csv"):
            file_data = self.read_file()
            data = self.merge_lists(file_data, test_data)
        else:
            data = test_data
        try:
            self.__file = open(r"/home/studentas/Documents/python/OpenVPN_speed_test/Test_report/" + self.file_name + ".csv", 'w')
            self.__writer = csv.writer(self.__file)
            self.__writer.writerows(data)
        except Exception as e:
            print("Error writing file",e)

    def read_file(self):
        file_data = []
        try:
            with open(r"/home/studentas/Documents/python/OpenVPN_speed_test/Test_report/" + self.file_name + ".csv", 'r') as csvfile:
                reader = csv.reader(csvfile, skipinitialspace=True)
                for row in reader:
                    file_data.append(row)
                return file_data
        except Exception as e:
            print(e)
            exit()

    def merge_lists(self, file_data, test_data):
        data = []
        data = [a + b for a, b in zip(file_data, test_data)]
        return data