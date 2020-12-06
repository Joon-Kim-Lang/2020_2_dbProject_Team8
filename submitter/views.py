from django.shortcuts import render
from django.db import connection
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
        strSql = '''SELECT TASKNAME, ACCEPTED
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
            row = {'TaskName': task[0]}
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
    {'evalscore':evalscore, 'all':tasklist, 'accepted':accepted, 'not_accepted':not_accepted, 'waiting':waiting, 'not_applied':not_applied})

def taskApply(request, taskid):
    cursor = connection.cursor()
    sql = "SELECT TASKNAME from TASK where ID = {}".format(taskid)
    result=cursor.execute(sql)
    result=cursor.fetchall()[0][0]      
    connection.commit()
    connection.close()
    return render(request, 'submitter/taskApply.html', {'taskname':result, 'user':user, 'taskid':taskid})
