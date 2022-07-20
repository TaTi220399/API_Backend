import requests
import socket
import sqlite3
from sqlite3 import Error
import json 

class Humster():
    def __init__(self, category, weight, age, diet):
        self.category = category
        self.weight = weight
        self.age = age
        self.diet = diet
    def printInfo(self):
        print("Humster's category:", self.category)
        print("Humster's weight:", self.weight)
        print("Humster's age:", self.age)
        print("Humster's diet:", self.diet)

def create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
        print("Connection to SQLite DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")
    return connection

def save_JSON(data, humsters, path, JSONname):
    with open(path + JSONname) as json_file:
        data = json.load(json_file)

    if len(humsters) != 0:
        for humster in humsters:
            data['humster']['category'].append(humster.category)
            data['humster']['weight'].append(humster.weight)
            data['humster']['age'].append(humster.age)
            data['humster']['diet'].append(humster.diet)

    with open(path + "data_file.json", "w") as write_file:
        json.dump(data, write_file)

def get_data():
    ans = input('\n\nWhat you want?\nI can...\n1. Creat a new humster\n2. Show all hamsters\n3. Finish work\n\n')
    return ans

def creat_newHumster(humsters, cur, conn):
    infoHum = input('Enter the category, weight, age and diet of the hamster, respectively, separated by commas:\n')
    infoHum = infoHum.split(',')
    humster = Humster(infoHum[0], infoHum[1], infoHum[2], infoHum[3])
    humster.printInfo()
    humsters.append(humster)
    sql = "INSERT INTO Humster VALUES ('" + humster.category + "', '" + humster.weight + "', '" + humster.age + "', '" + humster.diet + "')"
    cur.execute(sql)
    conn.commit()
    print('Hamster added successfully\n')

def show_allHumsters(cur):
    result = cur.execute('''SELECT * FROM Humster''')
    for res in result:
        humster = Humster(res[0], res[1], res[2], res[3])
        humster.printInfo()
        print('\n')

path = 'C:/Users/trost/Desktop/Учеба/СИИ/'
DBname = 'DBHumster1.accdb'
JSONname = 'data_file.json'
finish = False

humsters = []
data = {
            'humster' :
            {
                'category' : [],
                'weight' : [],
                'age' : [],
                'diet' : []
                }
            }

conn = create_connection(path+DBname)
cur = conn.cursor()

#Получение данных

while finish != True:
    ans = get_data()
    if ans.lower() == 'creat a new' or ans == '1':
        creat_newHumster(humsters, cur, conn)
    elif ans.lower() == 'show all hamsters' or ans == '2':
        show_allHumsters(cur)
    elif ans.lower() == 'finish work' or ans == '3':
        finish = True
    else:
        print("I don't understand, please repeat your request again")

conn.commit()
conn.close()

#Запись в JSON

save_JSON(data, humsters, path, JSONname)
