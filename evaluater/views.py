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

        TASK_SCORE = []
        for i in range(len(par_info)) :
            task_num = str(par_info[i][0]).split('_')[2]
            print(task_num)
            cursor = connection.cursor()
            strSql = '''SELECT EVALSCORE FROM TASK WHERE ID = %d''' % (int(task_num))
            result = cursor.execute(strSql)
            t_score = cursor.fetchall()[0][0]

            TASK_SCORE.append(int(t_score))

        connection.commit()
        connection.close()



        #before quality eval
        not_eval =[]
        #get evlauated
        eval = []
        cnt =0
        for parsed in par_info :

            if parsed[1] == None :
                row = {'FILEADDR' : parsed[0],'PNP' :parsed[1],'QUALITY':parsed[2],'SCORE': parsed[3],'ID':parsed[4],'TASK_SCORE' : TASK_SCORE[cnt]}
                not_eval.append(row)

            else :
                row = {'FILEADDR': parsed[0], 'PNP': parsed[1], 'QUALITY': int(parsed[2]), 'SCORE': parsed[3],'ID':parsed[4],'TASK_SCORE' : TASK_SCORE[cnt]}
                eval.append(row)
            cnt +=1
    except Exception as e :
        connection.rollback()
        print(e)

    return render(request,'evaluater/evaluateMain.html',{"not_eval" : not_eval,"eval" :eval})

def evaluating(request) :
    user = request.session.get('user')
    if user is None:
        return render(request, 'evaluater/wrongAccess.html')
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

            cursor = connection.cursor()
            strSql = '''SELECT COLUMN_NAME,COLUMN_TYPE
                                FROM INFORMATION_SCHEMA.COLUMNS
                                WHERE TABLE_NAME='%s';''' % (tdt_name)

            result = cursor.execute(strSql)
            col_names_fetch = cursor.fetchall()
            col_names = []

            for i in range(len(col_names_fetch)):
                col_names.append(col_names_fetch[i][0])


            insert_string = "("
            for i in range(len(col_names)) :
                if i == len(col_names) -1 :
                    insert_string = insert_string +  str(col_names[i])
                else :
                    insert_string = insert_string +  str(col_names[i]) + ","
            insert_string = insert_string + ")"
            for i in range(len(datas)) :
                datas_string = ""
                for j in range(len(datas[i])) :


                    if j == len(datas[i]) -1 :
                        datas_string = datas_string + "'"+str(datas[i][j])+ "'"
                    else :
                        datas_string = datas_string + "'" +str(datas[i][j]) + "'"+ ","

                datas_string = datas_string + "," + "'"+submitter_id +"'"
                cursor = connection.cursor()
                strSql = '''INSERT INTO %s%s VALUES(%s)'''%(tdt_name,insert_string,datas_string)

                result = cursor.execute(strSql)




        cursor = connection.cursor()
        strSql = '''SELECT TOTALTUPLE FROM PARSEDINFO WHERE ID = %d''' % (int(request.POST['ID']))
        result = cursor.execute(strSql)
        total_tuple = cursor.fetchall()[0][0]


        cursor = connection.cursor()
        strSql = '''SELECT DUPLICATETUPLE, NULLRATIO FROM PARSEDINFO WHERE ID = %d''' % (int(request.POST['ID']))
        result = cursor.execute(strSql)
        du_null_fetch = cursor.fetchall()
        du = 100 - int(100 * (int(du_null_fetch[0][0]) / total_tuple))
        null_ratio = 100 - int(float(du_null_fetch[0][1]) * 100)
        tuple_score = int(total_tuple)
        if total_tuple > 100:
            tuple_score = 100
        quality_score = 10 * int(request.POST['quality'])
        score = int((du + null_ratio + tuple_score + quality_score) / 40)

        cursor = connection.cursor()
        strSql = '''UPDATE PARSEDINFO SET SCORE = '%d' WHERE ID = '%d' AND EVALID = '%s';''' % (score, int(request.POST['ID']), user)
        result = cursor.execute(strSql)

        submitter_id = request.POST['FILEADDR'].split('_')[1]
        cursor = connection.cursor()
        strSql = '''SELECT FILEADDR,PNP FROM PARSEDINFO '''
        result = cursor.execute(strSql)
        data_all = cursor.fetchall()
        cnt = 0

        for i in range(len(data_all)):
            split_fileaddr = data_all[i][0].split('_')
            if submitter_id in split_fileaddr and data_all[i][1] != None:
                cnt += 1

        cursor = connection.cursor()
        strSql = '''SELECT EVALSCORE FROM MEMBER WHERE ID = "%s"''' % (submitter_id)
        result = cursor.execute(strSql)
        score_before = cursor.fetchall()[0][0]

        if score_before == None :
            score_before = 0
        else :
            score_before = int(score_before)

        score_new = int((score_before*(cnt-1) + score)/cnt)

        cursor = connection.cursor()
        strSql = '''UPDATE MEMBER SET EVALSCORE = %d WHERE ID = "%s"''' % (score_new,submitter_id)
        result = cursor.execute(strSql)

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

