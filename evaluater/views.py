from django.db import connection
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse


def wrongAccess(request):
    return render(request, 'evaluater/wrongAccess.html')

def sessionRecord(request):
    user = request.GET['id']
    request.session['user'] = user
    return redirect("evaluater:evaluateMain")

def logout(request):
    user = request.session.get('user')
    if user is None:
        return render(request, 'evaluater/wrongAccess.html')
    request.session.pop('user')
    request.session.flush()
    return render(request, "evaluater/logOut.html")


def evaluateMain(request) :
    user = request.session.get('user')
    if user is None:
        return render(request, 'evaluater/wrongAccess.html')
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
                row = {'FILEADDR' : parsed[0],'PNP' :parsed[1],'QUALITY':parsed[2],'SCORE': parsed[3],'ID':parsed[4]}
                not_eval.append(row)
            else :
                row = {'FILEADDR': parsed[0], 'PNP': parsed[1], 'QUALITY': int(parsed[2]), 'SCORE': parsed[3],'ID':parsed[4]}
                eval.append(row)

    except Exception as e :
        connection.rollback()
        print(e)

    return render(request,'evaluater/evaluateMain.html',{"not_eval" : not_eval,"eval" :eval})

def evaluating(request) :
    try :
        cursor = connection.cursor()
        strSql = '''UPDATE PARSEDINFO SET PNP = '%s',QUALITY = '%d' WHERE ID = '%d' AND EVALID = '%s';''' %(request.POST['PNP'],int(request.POST['quality']),int(request.POST['ID']),user)
        result = cursor.execute(strSql)
        if request.POST['PNP'] == 'P' :
            cursor = connection.cursor()
            strSql = '''SELECT MEMID FROM ORIGINALINFO WHERE PARSEDID = %d'''%(int(request.POST['ID']))
            result = cursor.execute(strSql)
            submitter_id = cursor.fetchall()[0][0]
            cursor = connection.cursor()

            strSql = '''SELECT TOTALTUPLE FROM PARSEDINFO WHERE ID = %d''' % (int(request.POST['ID']))
            result = cursor.execute(strSql)
            total_tuple = cursor.fetchall()[0][0]

            cursor = connection.cursor()
            strSql = '''UPDATE APPLY SET ACCEPTEDTUPLE = ACCEPTEDTUPLE + %d WHERE MEMID = "%s"''' % (int(total_tuple),submitter_id)
            result = cursor.execute(strSql)

            n_task = request.POST['FILEADDR'].split('_')[2]
            cursor = connection.cursor()
            strSql = '''SELECT TDTNAME FROM TASKDATATABLE WHERE TASKID = %d''' % (int(n_task))
            result = cursor.execute(strSql)
            tdt_name = cursor.fetchall()[0][0]

            cursor = connection.cursor()
            strSql = '''SELECT * FROM %s''' %(request.POST['FILEADDR'])
            result = cursor.execute(strSql)
            datas = cursor.fetchall()

            # cursor = connection.cursor()
            # strSql = '''SELECT COLUMN_NAME,COLUMN_TYPE
            #                     FROM INFORMATION_SCHEMA.COLUMNS
            #                     WHERE TABLE_NAME='%s';''' % (a)
            #
            # result = cursor.execute(strSql)

            # cursor = connection.cursor()
            # strSql = '''SELECT COLUMN_NAME,COLUMN_TYPE
            #                     FROM INFORMATION_SCHEMA.COLUMNS
            #                     WHERE TABLE_NAME='%s';''' % (fileaddr)

        #     result = cursor.execute(strSql)
        #
        #     col_names_fetch = cursor.fetchall()
        #     col_names = []
        #
        #     for i in range(len(col_names_fetch)):
        #         col_names.append(col_names_fetch[i][0])
        #
        #     col_names_string = ''
        #     for i in range(len(col_names)) :
        #         col_names_string = col_names_string + col_names[i] + ','
        #         if i == len(col_names) -1 :
        #             col_names_string = col_names_string + col_names[i]
        #
        #     strSql = '''insert into TASKDATATABLE(TDTNAME,TDTSCHEMA,SCHEMATYPE,TASKID) values('%s','%s','%s','%d');''' %(fileaddr,col_names_string,)
        connection.commit()
        connection.close()
    except Exception as e:
        connection.rollback()
        print(e)

    return HttpResponseRedirect(reverse('evaluater:evaluateMain'))

def evalDescription(request, addr) :
    user = request.session.get('user')
    if user is None:
        return render(request, 'evaluater/wrongAccess.html')

    try :
        cursor = connection.cursor()
        strSql = '''SELECT * FROM %s;''' % (addr)

        result = cursor.execute(strSql)
        par_info = cursor.fetchall()
        
        
        cursor = connection.cursor()
        strSql = '''SELECT COLUMN_NAME,COLUMN_TYPE 
                    FROM INFORMATION_SCHEMA.COLUMNS 
                    WHERE TABLE_NAME='%s';''' % (addr)

        result = cursor.execute(strSql)

        col_names_fetch = cursor.fetchall()

        col_names = []


        for i in range(len(col_names_fetch)) :
            col_names.append(col_names_fetch[i][0])
        # par_dict = []
        # for i in range(len(par_info)) :
        #     row = []
        #     for j in range(len(col_names)) :
        #         row.append(par_info[i][j])
        #     par_dict.append(row)




        connection.commit()
        connection.close()
        context = {'COL_INFO' : col_names, 'PAR_INFO' : par_info, 'FILE_NAME' : [addr]}

    except Exception as e:
        connection.rollback()
        print("Failed to get Data, e", e)

    return render(request, 'evaluater/showfile.html', context)

