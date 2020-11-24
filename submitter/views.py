from django.shortcuts import render, redirect
from django.db import connection
from django.http import HttpResponseRedirect
from .forms import originalDTForm

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