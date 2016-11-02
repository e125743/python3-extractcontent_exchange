import mysql.connector
import os
import sys 
 
def showUser(userName):
 
    connector = mysql.connector.connect(
            user='root',
            password=os.environ['PASSWORD'],
            host='localhost',
            database='debugger')

    cursor = connector.cursor()
    cursor.execute("select * from test where name = '" +userName + "'")
    #print(cursor.fetchall())
    users = cursor.fetchall()

    if len(users) == 0:
        print("row is null")
        sys.stdout.write("Do you input %s or not?(Y/N)" % userName)
        flag = input()
        if flag == 'Y':
            cursor.execute("insert into test(name) values('" +userName + "')")
            print("Input a %s" % userName)
    else:
        for row in users:
            print("ID:" + str(row[0]) + "  NAME:" + row[1])

    connector.commit()
    cursor.close
    connector.close
 
if __name__ == "__main__":
    argvs = sys.argv
    argc = len(argvs)

    if (argc < 2):
        print('Usage: # python %s UserName:Input the UserName which you want to search.' % argvs[0])
        quit()

    for i in range(1,argc):
        showUser(argvs[i])
