from django.db import connection
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.urls import reverse


def evaluateMain(request) :
    user = 'khjoh'
    try :
        cursor = connection.cursor()
        strSql = "SELECT FILEADDR,PNP,QUALITY,SCORE,ID  FROM PARSEDINFO WHERE PARSEDINFO.EVALID ='%s'"%(user)
        result = cursor.execute(strSql)
        #fileaddr,pnp,quality,score
        par_info = cursor.fetchall()
        connection.commit()
        connection.close()



        #before quality eval
        not_eval =[]
        #get evlauated
        eval = []
        for parsed in par_info :

            if parsed[1] == None :
                row = {'FILEADDR' : parsed[0],'PNP' :parsed[1],'QUALITY':parsed[2],'SCORE':parsed[3],'ID':parsed[4]}
                not_eval.append(row)
            else :
                row = {'FILEADDR': parsed[0], 'PNP': parsed[1], 'QUALITY': parsed[2], 'SCORE': parsed[3],'ID':parsed[4]}
                eval.append(row)

    except :
        connection.rollback()
        print("Failed to get Data")
    print('ev',eval)
    print('nev', not_eval)
    return render(request,'evaluater/evaluateMain.html',{"not_eval" : not_eval,"eval" :eval})

def evaluating(request) :
    user = 'khjoh'
    try :
        cursor = connection.cursor()
        strSql = '''UPDATE PARSEDINFO SET PNP = '%s',QUALITY = '%d' WHERE ID = '%d' AND EVALID = '%s';''' %(request.POST['PNP'],int(request.POST['quality']),int(request.POST['ID']),user)
        result = cursor.execute(strSql)
        connection.commit()
        connection.close()
    except Exception as e:
        print(e)
        connection.rollback()
        print("Fail")

    return HttpResponseRedirect(reverse('evaluater:evaluateMain'))

