from django.shortcuts import render, redirect
import os
from django.http import HttpResponseRedirect
from django.urls import reverse
import logging
from django.contrib import messages
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
                        WHERE TASK.ID = TASKID and (ACCEPTED = 'P' or ACCEPTED IS NULL) AND MEMBER.ID = '%s'
                        ORDER BY TASK.ID ASC'''%(user)
        result = cursor.execute(strSql)
        parTask = cursor.fetchall()

        strSql = '''SELECT T.TASKNAME
                         FROM TASK T
                         WHERE T.TASKNAME NOT IN(
                         SELECT TASKNAME
                                         FROM MEMBER, APPLY, TASK
                                         WHERE TASK.ID = TASKID and (ACCEPTED = 'P' or ACCEPTED IS NULL) AND MEMBER.ID = '%s'
                                         ORDER BY TASK.ID ASC)
                         ORDER BY ID ASC'''%(user)

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



def upload_csv(request):

    taskId = 'SAMPLE_1'
    context = {}

    try:
        cursor = connection.cursor()
        strSql = '''SELECT NAME, SCHEMAINFO
                         FROM ORIGINALDATATYPE, TASK
                         WHERE TASKNAME = '%s'
                         ORDER BY SERIALNUM ASC'''%(taskId)

        result = cursor.execute(strSql)
        originalDataType = cursor.fetchall()

        connection.commit()
        connection.close()

        for data in originalDataType:
            row = {'NAME': data[0], 'SCHEMA': data[1]}
            context.append(row)

    except:
        connection.rollback()
        print("Failed to get originalDataType")

    if "GET" == request.method:
        return render(request, "submitter/UploadFileEx.html",context)
    # if not GET, then proceed
    try:
        csv_file = request.FILES["csv_file"]
        if not csv_file.name.endswith('.csv'):
            messages.error(request,'File is not CSV type')
            return HttpResponseRedirect(reverse("submitter:uploadTest"))
        #if file is too large, return
        if csv_file.multiple_chunks():
            messages.error(request,"Uploaded file is too big (%.2f MB)." % (csv_file.size/(1000*1000),))
            return HttpResponseRedirect(reverse("submitter:uploadTest"))

        file_data = csv_file.read().decode("utf-8")
        print(file_data)

        lines = file_data.split("\n")
		#loop over the lines and save them in db. If error , store as string and then display
        for line in lines:
            fields = line.split(",")
            data_dict = {}
            data_dict["생활권"] = fields[0]
            data_dict["지역"] = fields[1]
            data_dict["아파트"] = fields[2]
            data_dict["세대수"] = fields[3]


			#try:
			#	form = EventsForm(data_dict)
			#	if form.is_valid():
			#		form.save()
			#	else:
			#		logging.getLogger("error_logger").error(form.errors.as_json())
			#except Exception as e:
			#	logging.getLogger("error_logger").error(repr(e))
				#pass

    except Exception as e:
        logging.getLogger("error_logger").error("Unable to upload file. "+repr(e))
        messages.error(request,"Unable to upload file. "+repr(e))

    return HttpResponseRedirect(reverse("submitter:uploadTest"))
