path = "/home/mohie/Desktop/cpp/ModernCPP_Tests_applications/Contact-APP/HELPERS/Phonebook.csv"

path = "/home/mohie/Desktop/cpp/ModernCPP_Tests_applications/Contact-APP/HELPERS"
import os
import csv
import json
def searchfile(value_to_be_search : str ):
    new_path = f"{path}/file_python.txt"
    buffer= input("enter: ")
    with open(new_path,"w") as txtfile:
        txtfile.write(buffer)

    with open(new_path, "r") as txtfile:
        print(txtfile.read())

    with open(new_path) as mohy:
        buffer = mohy.read()
        if(value_to_be_search in buffer):
            print("it's found")
            index = buffer.find(value_to_be_search)
            print(f"it was found in {index}")


def readcsv():
    with open(path,"r") as files:
         # print(file.read())
        print(files.readline())


def main():
    # searchfile('mohy')
    for file in os.listdir(path):
        if file.endswith("csv"):
            print(file)
            full_path = os.path.join(path,file)
            with open(full_path) as csvfile :
                csvlist = csv.DictReader(csvfile)
                for i, row in enumerate(csvlist,start = 19):
                    print(f"number :{i} : {row["FirstName"]}")
                

  




if __name__ == "__main__":
    main()
