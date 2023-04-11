#this simply starts the csv file for the login so that it isnt empty 
import csv

header= ["name","gmail","password"]

with open("data.csv", "a", newline='') as csv_file:
                    writer = csv.DictWriter(csv_file, fieldnames=header)
                    writer.writeheader
                    writer.writerow({"name":".","gmail":".","password":"."})




