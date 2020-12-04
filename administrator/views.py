from rest_framework.response import Response
from rest_framework.decorators import api_view

from django.shortcuts import render
# db connection
from django.db import connection

# json
import json

# time
from datetime import date

user = 'admin'

# ===================== JH ======================

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
                (TASKNAME, MINUPLOADCYCLE, EXPLANATION, EVALSCORE)
                VALUES ('%s', '%s', '%s', 9)
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

    request.session['loginInfo'] = {
        'userid': userid,
        'role': role
    }
    request.session.modified = True

    # connection close
    connection.commit()
    connection.close()

    # return success response
    return Response({'state': 'success', 'role': role})

# GET CURRENT USER INFO
@api_view(['GET'])
def getinfo(request):
    print(request.session)

    try:
        return Response({'info': request.session['loginInfo'] })
    except:
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
        if ageTo != '':
            query += " AND BIRTHDATE >= '" + str(date.today().year - int(ageTo) + 1) + "-01-01'"
        if ageFrom != '':
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

# NEW ORIGINAL DATA TYPE
@api_view(['POST'])
def addODT(request):
    """
    Add new original data type

    - Parameter
    taskname, typename(->NAME), ODTschema(->SCHEMATYPE), mappingschema(->MAPPINGSCHEMA)

    - Error List
    RequestError            : invalid request data
    DuplicateTaskNameError  : already exists task name in database
    DuplicateTDTNameError   : already exists TDT name in database
    DBQueryError            : error occured on db query
    """

    # parsing request
    try:
        taskname = request.data['taskname']
        typename = request.data['typename']
        ODTschema = request.data['ODTschema']
        mappingschema = request.data['mappingschema']
    except:
        return Response(status=400, data={'state': 'fail', 'code': 'RequestError'})

    # DB connection
    cursor = connection.cursor()

    # get task id
    query = f" SELECT ID FROM TASK WHERE TASKNAME = '{taskname}'"
    cursor.execute(query)
    response = cursor.fetchall()
    taskid = response[0][0]

    # INSERT new task info into DB
    try:
        query = f"""INSERT INTO ORIGINALDATATYPE
                (SCHEMATYPE, MAPPINGSCHEMA, NAME, TASKID)
                VALUES ('{ODTschema}', '{mappingschema}', '{typename}', '{taskid}')
                """
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

# GET USER DETAILED INFO
@api_view(['POST'])
def userinfo(request):
    """
    Return user's detailed info to modify

    - Parameter
    ID

    - Error List
    RequestError            : invalid request data
    NoMatchedIDError        : no matched id exists in DB
    DBQueryError            : error occured on db query
    """

    # parsing request
    try:
        userid = request.data['userid']
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

    query = f"SELECT * FROM MEMBER WHERE ID = '{userid}'"
    cursor.execute(query)
    response = cursor.fetchall()

    # connection close
    connection.commit()
    connection.close()

    # return success response
    return Response({'state': 'success', 'info': response[0]})

# EDIT USER INFO
@api_view(['POST'])
def modifyuser(request):
    """
    Modify user infomation

    - Parameter
    ID, name, gender, address, birth, phone,

    - Error List
    RequestError        : invalid request data
    DuplicateIDError    : already exists ID name in database
    DBQueryError        : error occured on db query
    """

    # parsing request
    try:
        userid = request.data['userid']
        name = request.data['name']
        address = request.data['address']
        gender = request.data['gender']
        phone = request.data['phone']
        birth = request.data['birth']
    except:
        return Response(status=400, data={'state': 'fail', 'code': 'RequestError'})

    # DB connection
    cursor = connection.cursor()

    # INSERT new account info into DB
    try:
        query = f"""UPDATE MEMBER
                SET NAME='{name}', ADDR='{address}', GENDER='{gender}', PHONENUM='{phone}', BIRTHDATE='{birth}'
                WHERE ID='{userid}'
                """
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

# DELETE USER
@api_view(['POST'])
def deleteuser(request):
    """
    Delete user's id

    - Parameter
    ID

    - Error List
    RequestError            : invalid request data
    NoMatchedIDError        : no matched id exists in DB
    DBQueryError            : error occured on db query
    """

    # parsing request
    try:
        userid = request.data['userid']
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

    query = f"DELETE FROM MEMBER WHERE ID = '{userid}'"
    cursor.execute(query)
    response = cursor.fetchall()

    # connection close
    connection.commit()
    connection.close()

    # return success response
    return Response({'state': 'success'})

# ===================== HJ ======================

# 관리자로 로그인했을 경우 초기 페이지로 보내주는 view
@api_view(['POST'])
def adminMain(request):
    return Response({'state': 'success','user':user})

#TASK ADMINISTRATIION
@api_view(['POST'])
def taskAdministration(request):
    return Response({'state': 'success','user':user})

#TASK STATISTICS
@api_view(['POST'])
def taskStatistics(request):
    try:
        userid = request.data['userid']
        role = request.data['role']
    except:
        return Response(status=400, data={'state': 'fail', 'code': 'RequestError'})

    try:
        cursor = connection.cursor()

        #the total number of files submitted for each task
        strSql = '''SELECT T.TASKNAME, COUNT(PI.ID)
                        FROM MEMBER M, APPLY A, TASK T, ORIGINALDATATYPE ODT, ORIGINALINFO OI, PARSEDINFO PI
                        WHERE M.ID = A.MEMID AND A.TASKID = T.ID AND T.ID = ODT.TASKID AND  ODT.SERIALNUM = OI.TYPENUM AND OI.PARSEDID = PI.ID AND (A.ACCEPTED = 'P' or A.ACCEPTED IS NULL or A.ACCEPTED = 'NP')
                        ORDER BY T.TASKNAME ASC'''
        result = cursor.execute(strSql)
        submittedFile = cursor.fetchall()

        #the number of tuples passed and stored in the task data table for each task
        strSql = '''SELECT T.TASKNAME, COUNT(PI.ID)
                        FROM MEMBER M, APPLY A, TASK T, ORIGINALDATATYPE ODT, ORIGINALINFO OI, PARSEDINFO PI
                        WHERE M.ID = A.MEMID AND A.TASKID = T.ID AND T.ID = ODT.TASKID AND  ODT.SERIALNUM = OI.TYPENUM AND OI.PARSEDID = PI.ID AND (A.ACCEPTED = 'P')
                        ORDER BY T.TASKNAME ASC'''
        result = cursor.execute(strSql)
        storedTuple = cursor.fetchall()

        #the total number of files submitted for each original data type
        strSql = '''SELECT ODT.SCHEMAINFO, COUNT(PI.ID)
                        FROM MEMBER M, APPLY A, TASK T, ORIGINALDATATYPE ODT, ORIGINALINFO OI, PARSEDINFO PI
                        WHERE M.ID = A.MEMID AND A.TASKID = T.ID AND T.ID = ODT.TASKID AND ODT.SERIALNUM = OI.TYPENUM AND OI.PARSEDID = PI.ID AND (A.ACCEPTED = 'P' or A.ACCEPTED IS NULL or A.ACCEPTED = 'NP')
                        ORDER BY ODT.SCHEMAINFO ASC'''
        result = cursor.execute(strSql)
        originalSubmittedFile = cursor.fetchall()


        #the number of tuples passed and stored in the task data table for each original data type
        strSql = '''SELECT ODT.SCHEMAINFO, COUNT(PI.ID)
                        FROM MEMBER M, APPLY A, TASK T, ORIGINALDATATYPE ODT, ORIGINALINFO OI, PARSEDINFO PI
                        WHERE M.ID = A.MEMID AND A.TASKID = T.ID AND T.ID = ODT.TASKID AND  ODT.SERIALNUM = OI.TYPENUM AND OI.PARSEDID = PI.ID AND (A.ACCEPTED = 'P')
                        ORDER BY ODT.SCHEMAINFO ASC'''
        result = cursor.execute(strSql)
        orignalStoredTuple = cursor.fetchall()

        #the list of submitters participating in each task
        strSql = '''SELECT T.TASKNAME, M.ID, M.NAME
                        FROM TASK T, APPLY A, MEMBER M
                        WHERE T.ID = A.TASKID AND A.MEMID = M.ID AND (A.ACCEPTED = 'P' or A.ACCEPTED IS NULL or A.ACCEPTED = 'NP')
                        ORDER BY T.TASKNAME ASC'''
        result = cursor.execute(strSql)
        participatingSubmitter = cursor.fetchall()



        file_task=[]
        tuple_task=[]
        file_original=[]
        tuple_original=[]
        submitter_now=[]

        for singleFile in submittedFile:
            row = {'TaskName': singleFile[0], 'count':singleFile[1]}
            file_task.append(row)

        for singleTuple in storedTuple:
            row = {'TaskName': singleTuple[0], 'count':singleTuple[1]}
            tuple_task.append(row)


        for originalFile in originalSubmittedFile:
            row = {'OriginalName': originalFile[0],  'count':originalFile[1]}
            file_original.append(row)

        for originalTuple in orignalStoredTuple:
            row = {'OriginalName': originalTuple[0], 'count':originalTuple[1]}
            tuple_original.append(row)

        for nowSubmitter in participatingSubmitter:
            row = {'TaskName': nowSubmitter[0], 'SubmitterID':nowSubmitter[1], 'SubmitterName':nowSubmitter[2]}
            submitter_now.append(row)


    except Exception as e:
        connection.rollback()
        return Response(status=400, data={'state': 'fail', 'code': 'DBQueryError : ' + str(e)})

    connection.commit()
    connection.close()

    return Response({'state': 'success', 'file_task':file_task, 'tuple_task':tuple_task, 'file_original':file_original,
    'tuple_original':tuple_original, 'submitter_now':submitter_now})

#SHOW THE LIST OF TASKS THAT EACH SUBMITTER IS PARTICIPATING
@api_view(['POST'])
def taskNow(request, name):
    try:
        taskname = request.data['taskname']
        submittername = request.data['submittername']
    except:
        return Response(status=400, data={'state': 'fail', 'code': 'RequestError'})

    try:
        cursor = connection.cursor()

        #the list of tasks that each submitter is participating in
        strSql = '''SELECT M.NAME, T.TASKNAME
                        FROM TASK T, APPLY A, MEMBER M
                        WHERE T.ID = A.TASKID AND A.MEMID = M.ID AND (A.ACCEPTED = 'P' or A.ACCEPTED IS NULL or A.ACCEPTED = 'NP') AND M.NAME = '%s'
                        ORDER BY M.NAME ASC'''%(submittername)

        result = cursor.execute(strSql)
        participatingTask = cursor.fetchall()

        task_now=[]

        for nowTask in participatingTask:
            row = {'SubmitterName': nowTask[0], 'TaskName':nowTask[1]}
            task_now.append(row)

    except Exception as e:
        connection.rollback()
        return Response(status=400, data={'state': 'fail', 'code': 'DBQueryError : ' + str(e)})

    connection.commit()
    connection.close()

    return Response({'state': 'success', 'name': name, 'task_now':task_now})


# ===================== HM ======================
#main page in managing task, show current task list
@api_view(['POST'])
def manageMain(request):

    #get current existing tasks' info
    try:
        # DB connection
        cursor = connection.cursor()

        #GET CURRENT EXISTING TASK
        strSql = '''SELECT ID, TASKNAME, EXPLANATION
                    FROM TASK
                    ORDER BY TASKNAME'''

        result = cursor.execute(strSql)
        existingTask = cursor.fetchall()

        task_list = []

        for task in existingTask:
            row = {'TaskID':task[0], 'TaskName':task[1], 'Explanation': task[3]}
            task_list.append(row)

    except Exception as e:
        connection.rollback()
        return Response(status=400, data={'state':'fail', 'code':'DBQueryError : ' + str(e)})

    # DB disconnect
    connection.commit()
    connection.close()

    return Response({'state':'success', 'task_list':task_list})

@api_view(['POST'])
def getWaitingMember(request):


    try:
        # DB connection
        cursor = connection.cursor()

        #GET members
        strSql = '''SELECT M.ID, M.NAME, M.EVALSCORE
                    FROM MEMBER M, APPLY A
                    WHERE A.MEMID = M.ID
                    '''

        result = cursor.execute(strSql)
        waitingMem = cursor.fetchall()

        waitingMemList = []

        for member in waitingMem:
            row = {'ID': member[0], 'Name': member[1], 'EVALSCORE': member[2]}
            waitingMemList.append(row)

    except Exception as e:
        connection.rollback()
        return Response(status=400, data={'state':'fail', 'code':'DBQueryError : ' + str(e)})

    # DB disconnect
    connection.commit()
    connection.close()

    return Response({'state':'success', 'waitingMemList':waitingMemList})



#add submitter to task by admin acceptance
@api_view(['POST'])
def addParticipant(request):

    #parse data
    try:
        member_id = request.data['member_id']
        taskname = request.data['taskname']
    except:
        return Response(status=400, data={'state': 'fail', 'code': 'RequestError'})

    #DB connection
    cursor = connection.cursor()

    # get task id
    query = f" SELECT ID FROM TASK WHERE TASKNAME = '{taskname}'"
    cursor.execute(query)
    response = cursor.fetchall()
    taskid = response[0][0]

    # Accept submitter to task
    try:
        query = f"""UPDATE APPLY
                    SET ACCEPTED='P'
                    WHERE ID='{member_id}' AND TASKID='{taskid}'
                    """
        cursor.execute(query)
        response = cursor.fetchall()
    except Exception as e:
        connection.rollback()
        return Response(status=400, data={'state': 'fail', 'code': 'DBQueryError : ' + str(e)})

    connection.commit()
    connection.close()

    return Response({'state':'success'})


@api_view(['POST'])
def getWaitingODT(request):


    try:
        # DB connection
        cursor = connection.cursor()

        #GET CURRENT EXISTING TASK
        strSql = '''SELECT SCHEMAINFO, SCHEMATYPE
                    FROM APPLIED_DATATYPE
                    '''

        result = cursor.execute(strSql)
        waitingODT = cursor.fetchall()

        waitingODTList = []

        for ODT in waitingODT:
            row = {'SCHEMAINFO': ODT[0], 'SCHEMATYPE': ODT[1]}
            waitingODTList.append(row)

    except Exception as e:
        connection.rollback()
        return Response(status=400, data={'state':'fail', 'code':'DBQueryError : ' + str(e)})

    # DB disconnect
    connection.commit()
    connection.close()

    return Response({'state':'success', 'waitingMemList':waitingODTList})


#add submitter requested original datatype by admin(different function from addODT)
@api_view(['POST'])
def addDatatype(request):

    # parse request
    try:

        taskname = request.data['taskname']
        datatypename = request.data['datatypename']
        mappingschema = request.data['mappingschema']

    except:
        return Response(status=400, data={'state': 'fail', 'code': 'RequestError'})

    # DB connection
    cursor = connection.cursor()

    # get task id
    query = f" SELECT ID FROM TASK WHERE TASKNAME = '{taskname}'"
    cursor.execute(query)
    response = cursor.fetchall()
    taskid = response[0][0]

    # get applynum(pk for applied_datatype)
    query = f" SELECT APPLYNUM FROM APPLIED_DATATYPE WHERE TASKID = '{taskid}'AND DATATYPE_NAME = '{datatypename}' "
    cursor.execute(query)
    response = cursor.fetchall()
    applynum = response[0][0]

    #get ODT infomations
    strSql = """SELECT DATATYPE_NAME, SCHEMAINFO,
                FROM APPLIED_DATATYPE
                WHERE APPLYNUM= '%s' """%(applynum)
    result = cursor.execute(strSql)
    ODTinfo = cursor.fetchall()

    typename= ODTinfo[0]
    ODTschema =ODTinfo[1]


    #add ODT to task
    try:
        query = f"""INSERT INTO ORIGINALDATATYPE
                    (SCHEMATYPE, MAPPINGSCHEMA, NAME, TASKID)
                    VALUES ('{ODTschema}', '{mappingschema}', '{typename}', '{taskid}')
                    """
        cursor.execute(query)
        response = cursor.fetchall()
    except Exception as e:
        connection.rollback()
        return Response(status=400, data={'state': 'fail', 'code': 'DBQueryError : ' + str(e)})

    #delete ODT from waiting list
    query = f"DELETE FROM APPLIED_DATATYPE WHERE APPLYNUM = '{applynum}'"
    cursor.execute(query)
    response = cursor.fetchall()

    # connection close
    connection.commit()
    connection.close()

    # return success response
    return Response({'state': 'success'})


#set pass value for task
@api_view(['POST'])
def setPassval(request):
    # parse request
    try:
        taskname = request.data['taskname']
        passval = request.data['passval']

    except:
        return Response(status=400, data={'state': 'fail', 'code': 'RequestError'})

    #DB connection
    cursor = connection.cursor()

    # get task id
    query = f" SELECT ID FROM TASK WHERE TASKNAME = '{taskname}'"
    cursor.execute(query)
    response = cursor.fetchall()
    taskid = response[0][0]

    # Set pass value for task
    try:
        query = f"""UPDATE TASK
                    SET EVALSCORE='{passval}'
                    WHERE ID='{taskid}'
                    """
        cursor.execute(query)
        response = cursor.fetchall()
    except Exception as e:
        connection.rollback()
        return Response(status=400, data={'state': 'fail', 'code': 'DBQueryError : ' + str(e)})

    connection.commit()
    connection.close()

    return Response({'state': 'success'})
