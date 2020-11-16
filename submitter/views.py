from django.shortcuts import render
from django.db import connection
# 제출자로 로그인했을 경우 초기 페이지로 보내주는 view
def showSubmitMain(request):

    #cur_user = request.User

    #if cur_user.is_authenticated:

    #    user = User.objects.get(user = request.user)

    user = 'khjoh'

    try:
        cursor = connection.cursor()
        strSql = '''SELECT TASKNAME, ACCEPTED
                        FROM MEMBER, APPLY, TASK
                        WHERE TASK.ID = TASKID and MEMBER.ID = MEMID and (ACCEPTED = 'P' or ACCEPTED IS NULL)
                        ORDER BY TASK.ID ASC'''
        result = cursor.execute(strSql)
        parTask = cursor.fetchall()

        strSql = '''SELECT T.TASKNAME
                         FROM TASK T
                         WHERE T.TASKNAME NOT IN(
                         SELECT TASKNAME
                                         FROM MEMBER, APPLY, TASK
                                         WHERE TASK.ID = TASKID and MEMBER.ID = MEMID and (ACCEPTED = 'P' or ACCEPTED IS NULL)
                                         ORDER BY TASK.ID ASC)
                         ORDER BY ID ASC'''

        result = cursor.execute(strSql)
        nonParTask = cursor.fetchall()

        connection.commit()
        connection.close()

        parDatas = []
        nonParDatas = []
        for data in parTask:
            row = {'TaskName': data[0], 'status': data[1]}
            parDatas.append(row)
            print(parDatas)

        for data in nonParTask:
            row = {'TaskName': data[0]}
            nonParDatas.append(row)
            print(nonParDatas)


    except:
        connection.rollback()
        print("Failed to get Data")

    return render(request, 'submitter/SubmitMain.html', {'parTasks':parDatas, 'nonParTasks':nonParDatas })
