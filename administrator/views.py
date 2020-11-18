from rest_framework.response import Response
from rest_framework.decorators import api_view

# db connection
from django.db import connection

# json 
import json

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
    userid = request.data['userid']
    password = request.data['password']
    name = request.data['name']
    address = request.data['address']
    gender = request.data['gender']
    phone = request.data['phone']
    birth = request.data['birth']
    role = request.data['role']

    # DB connection
    cursor = connection.cursor()
    
    # check duplicate ID
    query = "SELECT COUNT(*) FROM MEMBER WHERE ID = '%s'"%(userid)
    cursor.execute(query)
    response = cursor.fetchall()

    # INSERT new account info into DB
    #   no data in response when success
    #   raise error if query doesn't work
    query = """INSERT INTO MEMBER
                (ID, PASSWORD, NAME, ADDR, GENDER, PHONENUM, BIRTHDATE, ROLE) 
                VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')
                """%(userid, password, name, address, gender, phone, birth, role)
    cursor.execute(query)
    response = cursor.fetchall()

    # connection close
    connection.commit()
    connection.close()
    
    # return success response
    return Response({'state': 'success'})