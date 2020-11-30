from rest_framework.response import Response
from rest_framework.decorators import api_view

# db connection
from django.db import connection

# json 
import json

# time 
from datetime import date

# NEW USER REGISTERING
@api_view(['POST'])
def register(request):
    """
    Register new user
    
    - Parameter
    ID, password, name, gender, address, birth, phone, role(unchangable)

    - Error List
    RequestError        : invalid request data
    DuplicateIDError    : already exists ID name in database
    DBQueryError        : error occured on db query
    """

    # parsing request
    try:
        userid = request.data['userid']
        password = request.data['password']
        name = request.data['name']
        address = request.data['address']
        gender = request.data['gender']
        phone = request.data['phone']
        birth = request.data['birth']
        role = request.data['role']
    except:
        return Response(status=400, data={'state': 'fail', 'code': 'RequestError'})

    # DB connection
    cursor = connection.cursor()
    
    # check duplicate ID
    query = "SELECT COUNT(*) FROM MEMBER WHERE ID = '%s'"%(userid)
    cursor.execute(query)
    response = cursor.fetchall()

    # response error msg with fail sign (DuplicateIDError)
    if (response[0][0] == 1):
        connection.rollback()
        return Response(status=400, data={'state': 'fail', 'code': 'DuplicateIDError'})

    # INSERT new account info into DB
    try:
        query = """INSERT INTO MEMBER
                (ID, PASSWORD, NAME, ADDR, GENDER, PHONENUM, BIRTHDATE, ROLE) 
                VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')
                """%(userid, password, name, address, gender, phone, birth, role)
        cursor.execute(query)
        response = cursor.fetchall()
    except Exception as e:
        connection.rollback()
        return Response(status=400, data={'state': 'fail', 'code': 'DBQueryError : ' + str(e)})

    # connection close
    connection.commit()
    connection.close()
    
    # return success response
    return Response({'state': 'success'})

# NEW TASK CREATE
@api_view(['POST'])
def createTask(request):
    """
    Create new task

    - Parameter
    name, description, minuploadcycle, tdtname, tdtschema

    - Error List
    RequestError            : invalid request data
    DuplicateTaskNameError  : already exists task name in database
    DuplicateTDTNameError   : already exists TDT name in database
    DBQueryError            : error occured on db query
    """

    # parsing request
    try:
        name = request.data['name']
        description = request.data['description']
        minuploadcycle = request.data['minuploadcycle']
        tdtname = request.data['tdtname']
        tdtschema = request.data['tdtschema']
    except:
        return Response(status=400, data={'state': 'fail', 'code': 'RequestError'})

    # DB connection
    cursor = connection.cursor()

    # check duplicate task name
    query = "SELECT COUNT(*) FROM TASK WHERE TASKNAME = '%s'"%(name)
    cursor.execute(query)
    response = cursor.fetchall()

    # response error msg with fail sign (DuplicateTaskNameError)
    if (response[0][0] == 1):
        connection.rollback()
        return Response(status=400, data={'state': 'fail', 'code': 'DuplicateTaskNameError'})

    # check duplicate TDT name
    query = "SELECT COUNT(*) FROM TASKDATATABLE WHERE TDTNAME = '%s'"%(tdtname)
    cursor.execute(query)
    response = cursor.fetchall()

    # response error msg with fail sign (DuplicateTDTNameError)
    if (response[0][0] == 1):
        connection.rollback()
        return Response(status=400, data={'state': 'fail', 'code': 'DuplicateTaskNameError'})

    # INSERT new task info into DB
    try:
        query = """INSERT INTO TASK
                (TASKNAME, MINUPLOADCYCLE, EXPLANATION) 
                VALUES ('%s', '%s', '%s')
                """%(name, minuploadcycle, description)
        cursor.execute(query)
        response = cursor.fetchall()
    except Exception as e:
        connection.rollback()
        return Response(status=400, data={'state': 'fail', 'code': 'DBQueryError : ' + str(e)})

    # INSERT new task data table info into DB
    query = " SELECT ID FROM TASK WHERE TASKNAME = '%s'"%(name)
    cursor.execute(query)
    response = cursor.fetchall()
    taskID = response[0][0]

    try:
        query = """INSERT INTO TASKDATATABLE
                (TDTNAME, TDTSCHEMA, TASKID) 
                VALUES ('%s', '%s', '%s')
                """%(tdtname, tdtschema, taskID)
        cursor.execute(query)
        response = cursor.fetchall()
    except Exception as e:
        connection.rollback()
        return Response(status=400, data={'state': 'fail', 'code': 'DBQueryError : ' + str(e)})

    # CREATE new task data table
    try:
        query = tdtschema
        cursor.execute(query)
        response = cursor.fetchall()
    except Exception as e:
        connection.rollback()
        return Response(status=400, data={'state': 'fail', 'code': 'DBQueryError : ' + str(e)})

    # connection close
    connection.commit()
    connection.close()
    
    # return success response
    return Response({'state': 'success'})

# ACCOUNT login IN CHECK
@api_view(['POST'])
def login(request):
    """
    User login
    
    - Parameter
    ID, password

    - Error List
    RequestError            : invalid request data
    NoMatchedIDError        : no matched id exists in DB
    InvalidPasswordError    : password is not correst
    DBQueryError            : error occured on db query
    """

    # parsing request
    try:
        userid = request.data['userid']
        password = request.data['password']
    except:
        return Response(status=400, data={'state': 'fail', 'code': 'RequestError'})

    # DB connection
    cursor = connection.cursor()
    
    # check if ID exists
    query = "SELECT COUNT(*) FROM MEMBER WHERE ID = '%s'"%(userid)
    cursor.execute(query)
    response = cursor.fetchall()

    # response error msg with fail sign (NoMatchedIDError)
    if (response[0][0] == 0):
        connection.rollback()
        return Response(status=400, data={'state': 'fail', 'code': 'NoMatchedIDError'})

    # check if password valid
    query = "SELECT PASSWORD FROM MEMBER WHERE ID = '%s'"%(userid)
    cursor.execute(query)
    response = cursor.fetchall()

    # response error msg with fail sign (InvalidPasswordError)
    if (response[0][0] != password):
        connection.rollback()
        return Response(status=401, data={'state': 'fail', 'code': 'InvalidPasswordError'})

    # save at session
    query = "SELECT ROLE FROM MEMBER WHERE ID = '%s'"%(userid)
    cursor.execute(query)
    response = cursor.fetchall()
    role = response[0][0]

    request.session.loginInfo = {
        'userid': userid,
        'role': role
    }

    # connection close
    connection.commit()
    connection.close()
    
    # return success response
    return Response({'state': 'success', 'role': role})

# GET CURRENT USER INFO
@api_view(['GET'])
def getinfo(request):
    if request.session.get('loginInfo', False):
        return Response({ info: request.session.loginInfo })
    else:
        return Response(status=401, data={'code': 'No login session'})

# USER LOGGOUT
@api_view(['POST'])
def logout(request):
    if request.session.get('loginInfo'):
        del(request.session['loginInfo'])
    
    return Response({'status': 'success'})

# MEMBER STATISTICS
@api_view(['POST'])
def searchmember(request):
    """
    Search member from DB with search conditions
    
    - Parameter
    ID, gender, ageFrom, ageTo, role, task

    - Error List
    RequestError        : invalid request data
    DBQueryError        : error occured on db query
    """

    # parsing request
    try:
        userid = request.data['userid']
        gender = request.data['gender']
        ageFrom = request.data['ageFrom']
        ageTo = request.data['ageTo']
        role = request.data['role']
        task = request.data['task']
    except:
        return Response(status=400, data={'state': 'fail', 'code': 'RequestError'})

    # DB connection
    cursor = connection.cursor()

    # Get search information
    try:
        query = f""" SELECT ID, GENDER, BIRTHDATE, ROLE
                FROM MEMBER
                WHERE ID LIKE '%{userid}%'
                """
        if gender != '':
            query += f" AND GENDER = '{gender}'"
        if ageFrom != '':
            query += " AND BIRTHDATE >= '" + str(date.today().year - int(ageTo) + 1) + "-01-01'"
        if ageTo != '':
            query += " AND BIRTHDATE <= '" + str(date.today().year - int(ageFrom) + 1) + "-12-31'"
        if role != '':
            query += f" AND ROLE = '{role}'"
        if role == 'S' and task != '':
            query += f" AND ID IN (SELECT MEMID FROM APPLY WHERE TASKID = {task})"
        elif role == 'E' and task != '':
            query += f""" AND ID IN (SELECT EVALID FROM PARSEDINFO
                    WHERE ID IN (SELECT PARSEDID FROM ORIGINALINFO
                    WHERE TYPENUM IN (SELECT SERIALNUM FROM ORIGINALDATATYPE WHERE TASKID = {task})
                    )
                    )                    
                    """
        cursor.execute(query)
        response = cursor.fetchall()
    except Exception as e:
        connection.rollback()
        return Response(status=400, data={'state': 'fail', 'code': 'DBQueryError : ' + str(e)})

    # Search result array
    res = []
    for iter in response:
        res.append([iter[0], iter[1], str(date.today().year - iter[2].year + 1), iter[3]])

    # connection close
    connection.commit()
    connection.close()
    
    # return success response
    return Response({"state": "success", "result" : res })

# MEMBER INFO
@api_view(['POST'])
def memberinfo(request):
    """
    Return member's info
      * Submitter : return participating task, task participate info
      * Evaluator : return lists of parsing data sequence file 
    
    - Parameter
    ID, role

    - Error List
    RequestError        : invalid request data
    DBQueryError        : error occured on db query
    """

    # parsing request
    try:
        userid = request.data['userid']
        role = request.data['role']
    except:
        return Response(status=400, data={'state': 'fail', 'code': 'RequestError'})

    # DB connection
    cursor = connection.cursor()

    # Get user information by role
    try:
        if role == 'S':
            query = f""" SELECT OD.TASKID, OI.INFONUM, OI.NTH, PI.FILEADDR, PI.PNP, PI.SCORE
                    FROM ORIGINALINFO as OI, ORIGINALDATATYPE as OD, PARSEDINFO as PI
                    WHERE OI.MEMID = '{userid}' AND OI.TYPENUM = OD.SERIALNUM AND OI.PARSEDID = PI.ID
                    """
        elif role == 'E':
            query = f""" SELECT * FROM PARSEDINFO WHERE EVALID = '{userid}'
                    """
            
        cursor.execute(query)
        response = cursor.fetchall()
    except Exception as e:
        connection.rollback()
        return Response(status=400, data={'state': 'fail', 'code': 'DBQueryError : ' + str(e)})

    print(response)
    # Search result array
    res = []
    for iter in response:
        res.append(iter)

    # connection close
    connection.commit()
    connection.close()
    
    # return success response
    return Response({'state': 'success', 'role': role, 'result': res})