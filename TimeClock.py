import datetime as dt
import mysql.connector


mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    passwd='frida14&IPA17',
    database='personal_timeclock'
)
cursor = mydb.cursor()

def dateTime():
    dT = str(dt.datetime.now())
    date = dT[0:10]
    time = dT[11:16]
    dateTime = [date, time]
    return dateTime

def getHours(cmd):
    DT = dateTime()
    total = 0
    query = "SELECT * FROM {0} WHERE date = '{1}'"
    cursor.execute(query.format(cmd, DT[0]))
    row = cursor.fetchall()
    for i in row:
        if i[2] != None:
            Hrs = int(i[2][0:2]) - int(i[1][0:2])
            Min = (60 - int(i[1][3:5]) + int(i[2][3:5]))/60
            if Hrs == 0:
                Min = (int(i[2][3:5]) - int(i[1][3:5]))/60
                total = Min
            elif Hrs == 1:
                total = Min
            else:
                total = Hrs + Min
    query = "UPDATE {0} SET hours = {1} WHERE hours is NULL"
    cursor.execute(query.format(cmd, round(total, 2)))
    mydb.commit()

def getTotal(cmd):
    total = 0
    query = "SELECT * FROM {0}"
    cursor.execute(query.format(cmd))
    rows = cursor.fetchall()
    for row in rows:
        total += float(row[3])
        query = "UPDATE {0} SET total = {1} WHERE clock_out = '{2}'"
        cursor.execute(query.format(cmd, total, row[2]))
        mydb.commit()

def showTotal(table):
    query = "SELECT * FROM {0}"
    cursor.execute(query.format(table))
    rows = cursor.fetchall()
    for row in rows:
        print(row)

print("Welcom to Smart Time Clock")
print("(c) 2018 AGAH Solutions")
print("")
cmd = input("Which table would you like to select?")

while cmd != 'quit':
    split = cmd.split()
    if split[0] == 'show':
        if split[1] == 'tables':
            cursor.execute("SHOW TABLES")
            output = cursor.fetchall()
            for row in output:
                print(row)
            cmd = input("Which table would you like to select?")
        elif split[2] == 'hours':
            showTotal(split[1])
            cmd = input()
    elif split[0] == 'create':
        customer = split[1]
        cmd = input("Would you like to create a new table called '{0}'? [y/n] ".format(split[1]))
        if cmd == 'y':
            query = "CREATE TABLE {0} (date VARCHAR(10), clock_in VARCHAR(10), clock_out VARCHAR(10), hours VARCHAR(10), total VARCHAR(10))"
            cursor.execute(query.format(split[1]))
            mydb.commit()

            confirm = input("Are you clocking in? ")
            if confirm == "y":
                DT = dateTime()
                query = "INSERT INTO {0} (date, clock_in, clock_out, total) VALUES ('{1}', '{2}', {3}, {4})"
                cursor.execute(query.format(split[1], DT[0], DT[1], 'NULL', 'NULL'))
                mydb.commit()
                print("You are on the clock")            
                break
    else:
        DT = dateTime()
        try:
            cursor.execute("SELECT date FROM {0} WHERE clock_out IS NULL".format(cmd))
            output = cursor.fetchall()
            if output[0][0] == DT[0]:
                confirm = input("Are you clocking out? ")
                if confirm == 'y':
                    query = "UPDATE {0} SET clock_out = '{1}' WHERE clock_out IS NULL"
                    cursor.execute(query.format(cmd, DT[1]))
                    mydb.commit()
                    getHours(cmd)
                    getTotal(cmd)
                    print("You are off the clock")
                    break
                else:
                    break
            else:
                confirm = input("Are you clocking in? ")
                if confirm == "y":
                    query = "INSERT INTO {0} (date, clock_in, clock_out, total) VALUES ('{1}', '{2}', {3}, {4})"
                    cursor.execute(query.format(cmd, DT[0], DT[1], 'NULL', 'NULL'))
                    mydb.commit()
                    print("You are on the clock")
                    break
                else:
                    break
        except:
            confirm = input("Are you clocking in? ")
            if confirm == "y":
                query = "INSERT INTO {0} (date, clock_in, clock_out, total) VALUES ('{1}', '{2}', {3}, {4})"
                cursor.execute(query.format(cmd, DT[0], DT[1], 'NULL', 'NULL'))
                mydb.commit()
                print("You are on the clock")
                break
            else:
                break