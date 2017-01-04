import mysql.connector
import os
import sys 
 
def showUser(userName, connector, cusor):
    cursor.execute("select id from test where name = '" +userName + "'")
    #print(cursor.fetchall())
    users = cursor.fetchall()

    if len(users) == 0:
        print("row is null")
        sys.stdout.write("Do you input %s or not?(Y/N)" % userName)
        flag = input()
        if flag == 'Y':
            cursor.execute("insert into test(name) values('" +userName + "')")
            print("Input a \"%s\"" % userName)
    else:
        for row in users:
            print(row[0])

    connector.commit()
    return users
 
if __name__ == "__main__":
    argvs = sys.argv
    argc = len(argvs)
    connector = mysql.connector.connect(
            user='root',
            password=os.environ['PASSWORD'],
            host='localhost',
            database='debugger')
    cursor = connector.cursor()

    if (argc < 2):
        print('Usage: # python3.5 %s UserName1 ... UserNamen:Input UserNames which you want to search.' % argvs[0])
        quit()

    for i in range(1,argc):
        users = showUser(argvs[i], connector, cursor)
        for k in users:
            id = k[0]
        print(type(id))
    cursor.close
    connector.close
