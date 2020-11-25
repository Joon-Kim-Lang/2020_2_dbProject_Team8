from django.shortcuts import render, redirect
from django.db import connection
from django.http import HttpResponseRedirect
from .forms import originalDTForm
from django.urls import reverse
import logging
from django.contrib import messages
import os
import random

# 제출자로 로그인했을 경우 초기 페이지로 보내주는 view
# 로그인한 사용자 정보 얻어오기
user = 'khjoh'

def submitMain(request):

    #cur_user = request.User

    #if cur_user.is_authenticated:

    #    user = User.objects.get(user = request.user)

    try:
        cursor = connection.cursor()
        # get eval score
        strSql = "SELECT EVALSCORE FROM MEMBER WHERE MEMBER.ID = '%s'"%(user)
        result = cursor.execute(strSql)
        evalscore = cursor.fetchall()

        # get all tasks
        strSql = '''SELECT TASKNAME, EXPLANATION FROM TASK'''
        result = cursor.execute(strSql)
        allTask = cursor.fetchall()

        # applied tasks
        strSql = '''SELECT TASKNAME, ACCEPTED, TASK.ID
                        FROM MEMBER, APPLY, TASK
                        WHERE TASK.ID = TASKID and (ACCEPTED = 'P' or ACCEPTED IS NULL or ACCEPTED = 'NP') AND MEMBER.ID = '%s'
                        ORDER BY TASK.ID ASC'''%(user)
        result = cursor.execute(strSql)
        parTask = cursor.fetchall()

        # haven't applied
        strSql = '''SELECT T.TASKNAME, T.ID
                        FROM TASK T
                        WHERE T.TASKNAME NOT IN(
                        SELECT TASKNAME
                                        FROM MEMBER, APPLY, TASK
                                        WHERE TASK.ID = TASKID and (ACCEPTED = 'P' or ACCEPTED IS NULL or ACCEPTED = 'NP') AND MEMBER.ID = '%s'
                                        ORDER BY TASK.ID ASC)
                        ORDER BY ID ASC'''%(user)
        result = cursor.execute(strSql)
        nonParTask = cursor.fetchall()

        connection.commit()
        connection.close()

        accepted=[]
        not_accepted=[]
        waiting=[]
        not_applied=[]
        for task in parTask:
            row = {'TaskName': task[0], 'TaskID':task[2]}
            if task[1] == "P":
                accepted.append(row)
            elif task[1] == "NP":
                not_accepted.append(row)
            else:
                waiting.append(row)

        for task in nonParTask:
            row = {'TaskName': task[0], 'TaskID':task[1]}
            not_applied.append(row)

        tasklist = []
        for task in allTask:
            row = {'TaskName': task[0], 'describe':task[1]}
            tasklist.append(row)

        evalscore=evalscore[0][0]

    except:
        connection.rollback()
        print("Failed to get Data")

    return render(request, 'submitter/submitMain.html',
    {'evalscore':evalscore, 'all':tasklist, 'accepted':accepted, 'not_accepted':not_accepted, 'waiting':waiting, 'not_applied':not_applied, 'user':user})

def wrongAccess(request):
    return render(request, 'submitter/wrongAccess.html')

def taskApply(request, taskid):
    if request.method == "POST":
        cursor = connection.cursor()
        sql = "INSERT INTO APPLY(MEMID, TASKID) VALUES('{}',{})".format(user, taskid)
        result = cursor.execute(sql)
        connection.commit()
        cursor.close()
        connection.close()
        return redirect("submitter:submitMain")

    else:
        cursor = connection.cursor()
        sql = "SELECT TASKNAME from TASK where ID = {}".format(taskid)
        result=cursor.execute(sql)
        result=cursor.fetchall()[0][0]
        connection.commit()
        connection.close()
        return render(request, 'submitter/taskApply.html', {'taskname':result, 'user':user, 'taskid':taskid})

def taskCancel(request, taskid):
    if request.method == "POST":
        cursor = connection.cursor()
        sql = "DELETE FROM APPLY WHERE MEMID = '{}' and TASKID = {}".format(user, taskid)
        result = cursor.execute(sql)
        connection.commit()
        cursor.close()
        connection.close()
        return redirect("submitter:submitMain")
    else:
        return render(request, 'submitter/taskCancel.html')

def datatypeApply(request, taskid):
    def get_info():
        cursor=connection.cursor()

        # get all the original data types for the task
        sql = "SELECT NAME, SCHEMAINFO from ORIGINALDATATYPE where TASKID = {}".format(taskid)
        result = cursor.execute(sql)
        all_datatype = cursor.fetchall()

        # get applied data types but not commited by admin yet
        sql = "SELECT DATATYPE_NAME, SCHEMAINFO, SCHEMATYPE, SUBMITTER, APPLYNUM FROM APPLIED_DATATYPE where TASKID = {}".format(taskid)
        result = cursor.execute(sql)
        all_applied_datatype = cursor.fetchall()

        connection.commit()
        connection.close()

        # fetch result of the query
        all_dt = []
        applied_dt = []

        for dt in all_datatype:
            row={'dtName':dt[0], 'info':dt[1]} #row={'dtName':dt[0], 'info':dt[1], 'type':dt[2]} if is 자료형 added
            all_dt.append(row)

        for dt in all_applied_datatype:
            row={'dtName':dt[0], 'info':dt[1], 'type':dt[2], 'submitter':dt[3], 'applynum':dt[4]}
            applied_dt.append(row)

        return all_dt, applied_dt

    if request.method == "POST":
        form = originalDTForm(request.POST)
        if form.is_valid():
            dtname, schemainfo, schematype = form.data['name'], form.data['schemainfo'], form.data['schematype']
            cursor = connection.cursor()
            sql = "INSERT INTO APPLIED_DATATYPE(DATATYPE_NAME, SUBMITTER, TASKID, SCHEMAINFO, SCHEMATYPE) VALUES('{}','{}',{},'{}','{}')".format(dtname, user, taskid, schemainfo, schematype)
            result = cursor.execute(sql)
            connection.commit()
            cursor.close()
            connection.close()
            return redirect('submitter:datatypeApply', taskid = taskid)

    else:
        form = originalDTForm()
        all_dt, applied_dt = get_info()

    return render(request, 'submitter/datatypeApply.html', {'form':form, 'all_dt':all_dt, 'applied_dt':applied_dt, 'user':user, 'taskid':taskid})

def datatypeCancel(request, taskid):
    if request.method == "POST":
        applynum = request.POST['applynum']
        if request.POST['form_type'] == "show": # just show the cancel screen
            return render(request, 'submitter/datatypeCancel.html', {'applynum':applynum,'taskid':taskid})
        else: # delete the applied datatype from db
            cursor=connection.cursor()
            sql = "DELETE FROM APPLIED_DATATYPE WHERE APPLYNUM = {}".format(applynum)
            result = cursor.execute(sql)
            connection.commit()
            cursor.close()
            connection.close()
            return redirect('submitter:datatypeApply', taskid = taskid)
    else:
        return redirect('submitter:wrongAccess')

def taskSubmit(request,taskid):

    if "GET" == request.method:
        #(수정)태스크Id 받아와야
        context = []

        try:
            cursor = connection.cursor()
            strSql = '''SELECT NAME, SCHEMAINFO, SERIALNUM, SCHEMATYPE
                             FROM ORIGINALDATATYPE, TASK
                             WHERE ID = '%d'
                             ORDER BY SERIALNUM ASC'''%(taskid)

            result = cursor.execute(strSql)
            originalDataType = cursor.fetchall()

            connection.commit()
            connection.close()

            for data in originalDataType:
                row = {'NAME': data[0], 'SCHEMA': data[1], 'SERIALNUM' : data[2], 'TYPE': data[3]}
                context.append(row)
        except:
                connection.rollback()

        return render(request, "submitter/Submitting.html", {'context': context ,'taskId' : taskid})
    # if not GET, then proceed
    try:
        #(수정)어디선가 로그인정보 얻어와야함
        user = 'test'

        csv_file = request.FILES["csv_file"]
        if not csv_file.name.endswith('.csv'):
            messages.error(request,'File is not CSV type')
            return HttpResponseRedirect(reverse("submitter:Submitting"))
        #if file is too large, return
        if csv_file.multiple_chunks():
            messages.error(request,"Uploaded file is too big (%.2f MB)." % (csv_file.size/(1000*1000),))
            return HttpResponseRedirect(reverse("submitter:Submitting"))

        file_data = csv_file.read().decode("utf-8")

        lines = file_data.split("\n")
        csv_list = []
        for i in range(len(lines)):
            csv_list.append(lines[i].split(','))


        #폼에서 입력정보 받아오기
        startDate = request.POST['startDate']
        endDate = request.POST['endDate']
        submitNum = request.POST['submitNum']
        schema = request.POST['originalDataType']
        taskId = int(request.POST['taskId'])

        ORIGINALSCHEMALIST = schema.split(',')
        serialNum  = int(ORIGINALSCHEMALIST[-1])
        ORIGINALSCHEMALIST = ORIGINALSCHEMALIST[:len(ORIGINALSCHEMALIST)-1]

        #매핑시작
        cursor = connection.cursor()
        strSql = '''SELECT TDTSCHEMA
                         FROM TASKDATATABLE
                         WHERE TASKID = '%d'
                         '''%(taskId)

        result = cursor.execute(strSql)
        TDTSCHEMA = cursor.fetchall()

        connection.commit()
        connection.close()

        TDTSCHEMAORDER = []
        for data in TDTSCHEMA:
            row = {'COLUMN': data[0]}
            TDTSCHEMAORDER.append(row)
        #(아래)TDT스키마 정보가 담긴 변수
        TDTSCHEMAORDER[0]['COLUMN']
        TDTSCHEMALIST = TDTSCHEMAORDER[0]['COLUMN'].split(',')

        mappingDict = {}
        mapNum = 0


        for i in range(len(TDTSCHEMALIST)):
            mapNum = ORIGINALSCHEMALIST.index(TDTSCHEMALIST[i])
            mappingDict[i] = mapNum

        #파싱데이터 테이블 생성
        CreatedTableAddress = 'parsed_'+user+'_'+str(taskId)+'_'+submitNum
        CreatedTableQuery = 'CREATE TABLE ' +CreatedTableAddress +'('
        for i in range(len(TDTSCHEMALIST)):
            CreatedTableQuery = CreatedTableQuery + str(TDTSCHEMALIST[i])+' VARCHAR(300)'
            if i == len(TDTSCHEMALIST) -1:
                CreatedTableQuery = CreatedTableQuery+') ENGINE = INNODB;'
            else:
                CreatedTableQuery = CreatedTableQuery+','

        cursor = connection.cursor()
        strSql = CreatedTableQuery
        result = cursor.execute(strSql)
        connection.commit()
        connection.close()
        #PARSEDINFO 테이블에 데이터 추가 후 parsedid 얻어오기
        cursor = connection.cursor()
        strsql ='''insert into PARSEDINFO(FILEADDR)  values('%s');'''%(CreatedTableAddress)
        result = cursor.execute(strsql)
        strsql = '''select ID
                        from PARSEDINFO
                        where FILEADDR = '%s' '''%(CreatedTableAddress)
        result = cursor.execute(strsql)
        parsedId = cursor.fetchall()
        connection.commit()
        connection.close()
        parsedId = int(parsedId[0][0])

        #파싱데이터 테이블에 파일 저장

        cursor = connection.cursor()
        for i in range(1,len(csv_list)):
            if(len(csv_list[i]) < len(TDTSCHEMALIST)):
                break;
            values = ''
            for j in range(len(TDTSCHEMALIST)):
                if(j !=len(TDTSCHEMALIST)-1):
                    values = values + '\"' + csv_list[i][mappingDict[j]] + '\"'+','
                else:
                    values = values + '\"' + csv_list[i][mappingDict[j]][:-1] + '\"'

            strsql = '''insert into %s values(%s);'''%(CreatedTableAddress, values)
            result = cursor.execute(strsql)
            connection.commit()
        connection.close()

        #originalinfo 튜플추가
        cursor = connection.cursor()
        strsql = '''insert into ORIGINALINFO(NTH,STARTDATE,ENDDATE,TYPENUM,MEMID,PARSEDID) values('%d','%s','%s','%d','%s','%d');'''%(int(submitNum),startDate,endDate,serialNum,user,parsedId)
        result = cursor.execute(strsql)
        connection.commit()
        connection.close()
        #정량평가 요소 넣기
        quantityCheck(CreatedTableAddress,parsedId)

        #평가자 랜덤배정
        evalDesignate(parsedId)


    except Exception as e:
        logging.getLogger("error_logger").error("Unable to upload file. "+repr(e))
        messages.error(request,"Unable to upload file. "+repr(e))

    return HttpResponseRedirect(reverse("submitter:submitMain"))


def quantityCheck(tableName, ID):

        try:
            cursor = connection.cursor()
            strSql = "SELECT * FROM %s"%(tableName)
            result = cursor.execute(strSql)
            paresedTable = cursor.fetchall()

            connection.commit()
            connection.close()

            total_tup = len(paresedTable)
            #중복 튜플 수 검사
            tempSet = set(paresedTable)
            dupli_tup = total_tup - len(tempSet)


            #null 개수 검사
            null_num = 0
            for i in range(total_tup):
                for j in range(len(paresedTable[0])):
                    if paresedTable[i][j] in ('\r','\n',''):
                        null_num +=1;

            total_ele = total_tup * len(paresedTable[0])

            null_ratio = round(null_num / total_ele, 5)

            #정성평가 지표 집어넣기
            cursor = connection.cursor()
            strsql = "UPDATE PARSEDINFO SET TOTALTUPLE='%d', DUPLICATETUPLE='%d', NULLRATIO='%f' where ID = '%d';"%(total_tup,dupli_tup,null_ratio,ID)
            result = cursor.execute(strsql)
            connection.commit()
            connection.close()
        except:
            connection.rollback()
            print("Failed to get Data")

        return

def evalDesignate(ID):
    try:
        cursor = connection.cursor()
        strsql = '''select ID
                        from MEMBER
                        where ROLE = 'E' '''
        result = cursor.execute(strsql)
        evaluators = cursor.fetchall()
        connection.commit()
        connection.close()

        eval_count = len(evaluators)
        random_num = random.randint(0,eval_count-1)

        random_evalid = evaluators[random_num][0]

        cursor = connection.cursor()
        strsql = "UPDATE PARSEDINFO SET EVALID='%s' where ID = '%d';"%(random_evalid,ID)
        result = cursor.execute(strsql)
        connection.commit()
        connection.close()


    except:
        connection.rollback()
        print("Failed to get Data")


    return
