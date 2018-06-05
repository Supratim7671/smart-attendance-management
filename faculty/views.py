from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render,get_object_or_404
from .models import *
from django.contrib import messages
from django.db import transaction
from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from django.core.serializers import json
import json
import time
import hashlib, random, string

# Create your views here.
@csrf_exempt
def index(request):
    return render(request,"login.html")

@csrf_exempt
def stafflogin(request):
    if request.method == "POST":
        if "email" in request.POST and "password" in request.POST:
            email=request.POST.get('email')
            password=request.POST.get('password')
            try:
                user_object = staffs.objects.get(email=email,password=password)
            except Exception as e:
                user_object = None
            if user_object is None:
                messages.add_message(request, messages.ERROR, 'User doesn\'t exist.')
                return HttpResponseRedirect("/")
            else:
                role=user_object.role
                #request.session['loggedin']=True
                request.session['sessionid']=user_object.staffid
                request.session['role']=role
                return HttpResponseRedirect("/home")

        else:
            messages.add_message(request, messages.ERROR, 'Something went wrong')
            return HttpResponseRedirect("/")
    else:
        messages.add_message(request, messages.ERROR, 'Wrong Request Method')
        return HttpResponseRedirect("/")

@csrf_exempt
def home(request):

    if "role" in request.session and request.session["role"] == "student":
        return render(request, "studenthome.html")
    elif "role" in request.session and request.session["role"] == "faculty":
        j = subject.objects.all()
        k = branch.objects.all()
        return render(request, "facultyhome.html",{'j':j,'k':k})
    else:
        messages.add_message(request, messages.ERROR, 'You must login first')
        return HttpResponseRedirect("/")

@csrf_exempt
def addstudent(request):
    if request.method=="POST":
        if not request.session.get('sessionid',None):
            return HttpResponse('login required')
        sessionid=request.session['sessionid']
        email=request.POST.get('email')
        password=request.POST.get('password')
        branches=request.POST.get('branches')
        branchlist=list(branches.split(','))
        role="student"
        try:
            studentobj=staffs(email=email,pasword=password,role=role)
        except Exception as e:
            print("student exception"+str(e))

        studentobj.save()

        try:
            newstudentobj = staffs.objects.get(email=email, password=password, role=role)
        except Exception as e:
            print("New student object in add student method"+str(e))


    return

@csrf_exempt
def addfaculty(request):
    if request.method=='POST':
        if not request.session.get('sessionid',None):
            return HttpResponse("login required")
        sessionid=request.session['sessionid']
        email=request.POST.get('email')
        password=request.POST.get('password')
        role="faculty"
        branches = request.POST.get('branches')
        branchlist = list(branches.split(','))
        try:
            facultyobj=staffs(email=email,password=password,role=role)
        except Exception as e:
            print("faculty exception"+str(e))
        facultyobj.save()
    return
"""
@csrf_exempt
def showfacultydetail(request):
    #print("dszs")

    if request.method == "GET":
        #print("ssdad")
        if not request.session.get('sessionid', None):
            return HttpResponse("Login Required")
        sessionid = request.session['sessionid']
        print(str(sessionid))
        htmlvalue=request.GET.get("html")
        #request_context={}
        #request_context['name']=request.GET.get('name')
        #request_context['post']=request.GET.get('post')
        #request_context['address']=request.GET.get('address')
        #request_context['branch']=request.GET.get('branch')
        #request_context['mobile']=request.GET.get('mobile')
        if htmlvalue=="1":
            html="updatefaculty.html"
            print(html)
        elif htmlvalue=="2":
            html="showfaculty.html"
            #updatefaculty(request_context)
            print(html)
        else:
            html="showfaculty.html"
            print(html)

        try:
            staff_obj=staffs.objects.get(staffid=sessionid)
        except Exception as e:
            print("Update staff"+str(e))
        try:
            faculty_obj=faculty.objects.get(facultyid=sessionid)
        except Exception as e:
            print("Update faculty"+str(e))

        context_faculty_detail={}
        context_faculty_detail['name'] = ''
        context_faculty_detail['branch'] = ''
        context_faculty_detail['post'] = ''
        context_faculty_detail['address'] = ''
        #context_faculty_detail['subject'] = ''
        context_faculty_detail['mobile'] = ''
        context_faculty_detail['email'] = staff_obj.email
        context_faculty_detail['password'] = staff_obj.password

        if faculty_obj:
            context_faculty_detail['name']=faculty_obj.fname
            context_faculty_detail['branch']=str(faculty_obj.fbranchid)
            context_faculty_detail['post']=faculty_obj.fpost
            context_faculty_detail['address']=faculty_obj.faddress
            #context_faculty_detail['subject']=faculty_obj.fsubjectid
            context_faculty_detail['mobile'] = faculty_obj.fmobile
            print(context_faculty_detail)
            print("hello")



            print("Only staff object " + str(context_faculty_detail))

        #print(context_faculty_detail)
        return render(request,html,context_faculty_detail)
    else:
        return HttpResponse("Hello")
"""
@csrf_exempt
def show_student_detail(request):
    if request.method == "POST":
        if not request.session.get('sessionid', None):
            return HttpResponse("Login Required")
        sessionid = request.session['sessionid']
        try:
            staff_obj = staffs.objects.get(staffid=sessionid)
        except Exception as e:
            print("Update faculty" + str(e))
        try:
            student_obj = student.objects.get(studentid=sessionid)
        except Exception as e:
            print("show stuent" + str(e))
        context_student_detail = {}
        context_student_detail['name'] = ''
        context_student_detail['branch'] = ''
        context_student_detail['address'] = ''
        #context_student_detail['subject'] = ''
        context_student_detail['mobile'] = ''

        if staff_obj and not student_obj:
            context_student_detail['email'] = staff_obj.email
            context_student_detail['password'] = staff_obj.password

        if staff_obj and student_obj:
            context_student_detail['email'] = staff_obj.email
            context_student_detail['password'] = staff_obj.password
            context_student_detail['name'] = student_obj.sname
            context_student_detail['branch'] = student_obj.sbranchid
            context_student_detail['address'] = student_obj.saddress
            #context_student_detail['subject'] = student_obj.ssubjectid
            context_student_detail['mobile'] = student_obj.smobile

        return render(request, "ashdkashd.html", context_student_detail)


@csrf_exempt
def updatefaculty(request):

    if request.method=="POST":
        print("Bhagg Madarchod")
        if not request.session.get('sessionid',None):
            return HttpResponse("Login Required")
        sessionid=request.session['sessionid']

        print(sessionid)
        name=request.POST.get('name')
        print("name"+str(name))
        branchs=request.POST.get('branch')
        #print(str(branch))
        #subject=request.POST.get('subject')
        designation=request.POST.get('post')
        print(str(designation))
        address=request.POST.get('address')
        print(str(address))
        mobile=request.POST.get('mobile')
        print(str(mobile))
        print("Sessionid is "+str(sessionid))
        print(request.POST)
        try:
            faculty_obj=faculty.objects.get(facultyid=sessionid)
            if name is not None:
                faculty_obj.fname = name
            if branchs is not None:
                faculty_obj.fbranchid = branch(branch.objects.get(branchname=branchs).branchid)
            '''if subject is not None:
                faculty_obj.fsubjectid = subject
            '''
            if designation is not None:
                faculty_obj.fpost = designation
            if address is not None:
                faculty_obj.faddress = address
            if mobile is not None:
                faculty_obj.fmobile = mobile

            faculty_obj.save()
        except Exception as e:
            print("Update faculty"+str(e))
            #try:
            faculty_obj = faculty(facultyid=staffs(sessionid),
                                  fmobile=mobile,
                                  fname=name,
                                  fbranchid= branch(branch.objects.get(branchname=branchs).branchid),
                                  faddress=address,
                                  fpost=designation
                                  )
            faculty_obj.save()

            #except Exception as e:
            #   print("In faculty obj "+str(e))
        '''
        try:
            if faculty_obj is not None:

                   faculty_obj.save()
        except Exception as e:
            #q=0
            print("Starting Faculty object not present "+str(e))
            try:
                faculty_obj=faculty(facultyid=sessionid,fname=name,fbranch=branch,faddress=address,fpost=designation,fsubject=subject)
            except Exception as e:
                print("In update faculty"+str(e))

            faculty_obj.save()'''
        list = branch.objects.all()

        j = faculty.objects.get(facultyid=sessionid)
        print(str(j.fname) + ' ' + str(j.fpost))
        return render(request, "addfaculty.html", {'list': list, 'j': j})
        #return HttpResponse("successfully updated")

@csrf_exempt
def updatestudent(request):
    if request.method == "POST":
        print("Bhagg Madarchod")
        if not request.session.get('sessionid', None):
            return HttpResponse("Login Required")
        sessionid = request.session['sessionid']

        print(sessionid)
        name = request.POST.get('name')
        print("name" + str(name))
        branchs = request.POST.get('branch')
        # print(str(branch))
        # subject=request.POST.get('subject')
        #esignation = request.POST.get('post')
        #print(str(designation))
        address = request.POST.get('address')
        print(str(address))
        mobile = request.POST.get('mobile')
        print(str(mobile))
        print("Sessionid is " + str(sessionid))
        print(request.POST)
        try:
            student_obj = student.objects.get(studentid=sessionid)
            if name is not None:
                student_obj.sname = name
            if branchs is not None:
                student_obj.sbranchid = branch(branch.objects.get(branchname=branchs).branchid)
            '''if subject is not None:
                faculty_obj.fsubjectid = subject
            
            #if designation is not None:
                #faculty_obj.fpost = designation
                '''
            if address is not None:
                student_obj.saddress = address
            if mobile is not None:
                student_obj.smobile = mobile

            student_obj.save()
        except Exception as e:
            print("Update Student" + str(e))
            # try:
            student_obj = student(studentid=staffs(sessionid),
                                  smobile=mobile,
                                  sname=name,
                                  sbranchid=branch(branch.objects.get(branchname=branchs).branchid),
                                  address=address,

                                  )
            student_obj.save()

            # except Exception as e:
            #   print("In faculty obj "+str(e))
        '''
        try:
            if faculty_obj is not None:

                   faculty_obj.save()
        except Exception as e:
            #q=0
            print("Starting Faculty object not present "+str(e))
            try:
                faculty_obj=faculty(facultyid=sessionid,fname=name,fbranch=branch,faddress=address,fpost=designation,fsubject=subject)
            except Exception as e:
                print("In update faculty"+str(e))

            faculty_obj.save()'''
        list = branch.objects.all()

        j =student.objects.get(studentid=sessionid)
        print(str(j.sname))
        return render(request, "addstudent.html", {'list': list, 'j': j})
        # return HttpResponse("successfully updated")
@csrf_exempt
def facultypassword(request):
    if request.method=='POST':
        if not request.session.get('sessionid',None):
            return HttpResponse("Login Required")
        sessionid=request.session['sessionid']
        print(str(sessionid))
        oldpassword=request.POST.get('oldpassword')
        newpassword=request.POST.get('newpassword')
        cnewpassword=request.POST.get('cnewpassword')
        print(str(sessionid)+ " "+ str(oldpassword)+" "+str(newpassword)+" "+str(cnewpassword))
        try:
            staff_obj=staffs.objects.get(staffid=sessionid)
        except Exception as e:
            print("In faculty password"+str(e))
        dbpassword=staff_obj.password
        if oldpassword==dbpassword and newpassword==cnewpassword:
            staff_obj.password=newpassword
            staff_obj.save()
            return HttpResponse("Password Changed Successfully")
        else:
            return HttpResponse("Password Mismatch")


@csrf_exempt
def studentpassword(request):
    if request.method=='POST':
        if not request.session.get('sessionid',None):
            return HttpResponse("Login Required")
        sessionid=request.session['sessionid']
        oldpassword=request.POST.get('oldpassword')
        newpassword=request.POST.get('newpassword')
        cnewpassword=request.POST.get('cnewpassword')
        try:
            staff_obj=staffs.objects.get(staffid=sessionid)
        except Exception as e:
            print("In student password"+str(e))
        dbpassword=staff_obj.password
        if oldpassword==dbpassword and newpassword==cnewpassword:
            staff_obj.password=newpassword
        else:
            return HttpResponse("Password Mismatch")


        return HttpResponse("Password Changed Successfully")

@csrf_exempt
def updateattendence(request):
    if request.method == 'POST':
        if not request.session.get('sessionid', None):
            return HttpResponse("Login Required")
        sessionid = request.session['sessionid']
        sbranchid = request.POST.get('branchid')
        # studentobj=get_students(sbranchid)
        print(str(request.POST))
        ssubjectid = request.POST.get('subjectid')
        current_date = request.POST.get('date')
        modeofclass = request.POST.get('modeofclass')
        period = request.POST.get('period')
        attendanceid = attendance.objects.get(asbranchid=sbranchid, assubjectid=ssubjectid, date=current_date,
                                              modeofclass=modeofclass, period=period)

        print(request.POST)
        studentobj = student.objects.filter(sbranchid=sbranchid,ssubjectid=ssubjectid)
        statuses=[]
        for s in studentobj:
            try:
                statuses.append(request.POST['status{}'.format(s.studentid)])
            except Exception as e:
                print("In the update attendance column "+ str(e))
                attendancerecordid = attendancerecord.objects.get(aid=attendanceid, studentid=s.studentid)
                statuses.append(attendancerecordid.status)

            '''
            if request.POST['status{}'.format(s.studentid)] is None:
                attendancerecordid=attendancerecord.objects.get(aid=attendanceid,studentid=s.studentid)
                statuses.append(attendancerecordid.status)
            else:
                statuses.append(request.POST['status{}'.format(s.studentid)])
            '''
        #statuses = [request.POST['status{}'.format(s.studentid)] for s in studentobj]
        print("The status list is" + str(statuses))


        with transaction.atomic():

            #attendanceobj.save()
            newattendanceobj = attendance.objects.get(asbranchid=branch.objects.get(branchid=sbranchid),
                                                      assubjectid=subject.objects.get(subjectid=ssubjectid),
                                                      date=current_date, modeofclass=modeofclass,
                                                      period=int(period))
            attendanceid = newattendanceobj.aid

            attendance_record_list = []

            for i in range(0, len(studentobj)):
                studid = studentobj[i].studentid
                status = statuses[i]
                particular_attendance_obj = attendancerecord.objects.get(aid=attendance(attendanceid), studentid=staffs(str(studid)))
                particular_attendance_obj.status=status
                particular_attendance_obj.save()
                #attendance_record_list.append(particular_attendance_obj)
                #attendancerecord.objects.bulk_update(attendance_record_list)


            return HttpResponse("Attendance has been successfully updated")


@csrf_exempt
def get_student(request):
    if request.method=='POST':
        if not request.session.get('sessionid', None):
            return HttpResponse("Login Required")
        sessionid=request.session['sessionid']
        sbranchid=json.loads(request.body.decode('utf-8'))['branchid']
        studentobj = student.objects.filter(sbranchid=sbranchid)
        student_context={}
        student_context=studentobj.__dict__

        return JsonResponse(student_context,safe=False)

@csrf_exempt
def addattendance(request):
    if request.method=='POST':
        if not request.session.get('sessionid', None):
            return HttpResponse("Login Required")
        sessionid = request.session['sessionid']
        sbranchid = request.POST.get('branch')
        #studentobj=get_students(sbranchid)
        print(str(request.POST))
        ssubjectid = request.POST.get('subject')
        current_date=request.POST.get('date')
        modeofclass=request.POST.get('mode')
        period=request.POST.get('period')
        print(request.POST)
        studentobj = student.objects.filter(sbranchid=sbranchid,ssubjectid=ssubjectid)
        print(str(studentobj))
        statuses = [request.POST['status{}'.format(s.studentid)] for s in studentobj]
        print("The status list is"+str(statuses))
        try:
            attendanceobj=attendance(asbranchid=branch.objects.get(branchid=sbranchid),assubjectid=subject.objects.get(subjectid=ssubjectid),date=current_date,modeofclass=modeofclass,period=int(period))

            with transaction.atomic():

                attendanceobj.save()
                newattendanceobj = attendance.objects.get(asbranchid=branch.objects.get(branchid=sbranchid), assubjectid=subject.objects.get(subjectid=ssubjectid),
                                                          date=current_date, modeofclass=modeofclass,
                                                          period=int(period))
                attendanceid = newattendanceobj.aid
                print(str(attendanceid))
                attendance_record_list = []


                for s in range(0, len(studentobj)):
                    studid = studentobj[s].studentid
                    status = statuses[s]
                    print("In the list "+str(staffs(studid))+" "+str(status))
                    particular_attendance_obj = attendancerecord(aid=attendance(attendanceid),
                                                                 studentid=staffs(str(studid)), status=status)
                    attendance_record_list.append(particular_attendance_obj)
                attendancerecord.objects.bulk_create(attendance_record_list)

            return HttpResponse("Attendance has been successfully added")
        except Exception as e:
            print("Add attendance "+str(e))
            return HttpResponse("Attendance has not been successfully added")

@csrf_exempt
def addmarks(request):
    if request.method=='POST':
        if not request.session.get('sessionid', None):
            return HttpResponse("Login Required")
        sessionid = request.session['sessionid']
        msubjectid = request.POST.get('subject')
        mbranchid = request.POST.get('branch')
        studentobj = student.objects.filter(sbranchid=mbranchid, ssubjectid=msubjectid)
        print(studentobj)
        internalmarks = [request.POST['intmarks{}'.format(s.studentid)] for s in studentobj]
        externalmarks = [request.POST['extmarks{}'.format(s.studentid)] for s in studentobj]
        print(str(internalmarks)+"\n"+str(externalmarks))
        try:
            with transaction.atomic():
                markslist=[]

                for s in range(0, len(studentobj)):
                    studid = studentobj[s].studentid
                    intmarks = internalmarks[s]
                    extmarks = externalmarks[s]
                    print("In the list " + str(staffs(studid)) + " " + str(intmarks)+" "+str(extmarks))
                    marks_obj = marks(msstudentid=staffs(str(studid)),msubjectid=subject.objects.get(subjectid=msubjectid), intmarks=intmarks,extmarks=extmarks)
                    markslist.append(marks_obj)
                marks.objects.bulk_create(markslist)
            return HttpResponse("Marks has been successfully added")
        except Exception as e:
            print("The exception is"+str(e))
            return HttpResponse("Marks has not been successfully added")





@csrf_exempt
def seeattendance(request):
    if request.method=='GET':
        if not request.session.get('sessionid', None):
            return HttpResponse("Login Required")
        sessionid = request.session['sessionid']
        print("session id:"+str(sessionid))
        try:
            attendancerecordobj=attendancerecord.objects.filter(studentid=sessionid)
        except Exception as e:
            print("In the see attendance"+str(e))

        context_attendance_record_list=[]
        context_attendance_record_dict={}
        for attendances in attendancerecordobj:
            context_attendance_record={}
            rid=attendances.rid
            attendanceid=attendances.aid
            status = attendances.status
            ssubjectid=attendanceid.assubjectid
            sbranchid=attendanceid.asbranchid
            current_date=attendanceid.date
            period=attendanceid.period

            modeofclass=attendanceid.modeofclass
            print(str(attendanceid)+' '+str(ssubjectid)+' '+str(sbranchid)+' '+str(current_date)+' '+str(period)+' '+str(modeofclass)+' '+str(status))
            context_attendance_record['rid']=rid
            context_attendance_record['attendanceid']=attendanceid
            context_attendance_record['sbranchid']=sbranchid
            context_attendance_record['ssubjectid']=ssubjectid
            context_attendance_record['current_date']=current_date
            context_attendance_record['period']=period
            context_attendance_record['modeofclass']=modeofclass
            context_attendance_record['status']=status
            context_attendance_record_list.append(context_attendance_record)

        return render(request,"seeattendance.html",{'c':context_attendance_record_list})

@csrf_exempt
def addfacultyinfo(request):
    if request.method=='GET':
        if not request.session.get('sessionid', None):
            return HttpResponse("Login Required")
        sessionid = request.session['sessionid']

        list=branch.objects.all()

        try:
            j=faculty.objects.get(facultyid=sessionid)
        except Exception as e:
            a=0

        print(str(j.fname)+' '+str(j.fpost))
        return render(request,"addfaculty.html",{'list':list,'j':j})

@csrf_exempt
def addstudentinfo(request):
    if request.method=='GET':
        if not request.session.get('sessionid', None):
            return HttpResponse("Login Required")
        sessionid = request.session['sessionid']

        list=branch.objects.all()

        try:
            j=student.objects.get(studentid=sessionid)
        except Exception as e:
            a=0

        print(str(j.sname))
        return render(request,"addstudent.html",{'list':list,'j':j})


@csrf_exempt
def changepassword(request):
    return render(request,"chpassword.html")

@csrf_exempt
def uploadattendance(request):
    if request.method =="POST":
        if not request.session.get('sessionid', None):
            return HttpResponse("Login Required")
        sessionid = request.session['sessionid']
        #print(request.POST)
        subjectid=request.POST.get('subjectid')
        branchid=request.POST.get('branchid')
        l=student.objects.filter(sbranchid=branchid,ssubjectid=subjectid)

        return render(request,"uploadattendance.html",{'l':l,'branchid':branchid,'subjectid':subjectid})

@csrf_exempt
def updatef(request):
    return render(request,"updatefaculty.html",)

@csrf_exempt
def listsubject(request):
    l=subject.objects.all()
    return render(request,"allotsubject.html",{'l':l})

@csrf_exempt
def allotsubject(request):
    if request.method == 'POST':
        if not request.session.get('sessionid', None):
            return HttpResponse("Login Required")
        sessionid = request.session['sessionid']
        subjectlist=[]
        subjectlist=request.POST.getlist('subjects')
        try:
            student_object=student.objects.get(studentid=sessionid)
        except Exception as e:
            print("Allot subject "+str(e))
        for subject in subjectlist:
            print(subject)
            student_object.ssubjectid.add(subject)
        student_object.save()

        print("Subject Lists are "+str(subjectlist))
        return HttpResponse("subect alloted")

@csrf_exempt
def updateattendance(request):
    l = attendance.objects.all()
    return render(request,"updateattendance.html",{'l':l})

@csrf_exempt
def updatemarks(request):
    if request.method == "POST":
        if not request.session.get('sessionid', None):
            return HttpResponse("Login Required")
        sessionid = request.session['sessionid']
        # print(request.POST)
        subjectid = request.POST.get('subjectid')
        branchid = request.POST.get('branchid')
        #l = student.objects.filter(sbranchid=branchid, ssubjectid=subjectid)
        m=marks.objects.filter(msubjectid=subjectid)
        markslist=[]
        for i in m:
            studentobj=student.objects.get(studentid=i.msstudentid)
            name=studentobj.sname
            studentid=studentobj.studentid
            intmarks=i.intmarks
            extmarks=i.extmarks
            markslist_dict={}
            markslist_dict['studentid']=studentid
            markslist_dict['msubjectid']=subjectid
            markslist_dict['studentname']=name
            markslist_dict['internalmarks']=intmarks
            markslist_dict['externalmarks']=extmarks
            markslist.append(markslist_dict)

        return render(request, "updatemarks.html", {'markslist':markslist})

@csrf_exempt
def seemarks(request):
    if request.method == "GET":
        if not request.session.get('sessionid', None):
            return HttpResponse("Login Required")
        sessionid = request.session['sessionid']
        studentobj=student.objects.get(studentid=sessionid)
        subjectlist=studentobj.ssubjectid.all()
        print(str(sessionid)+" "+str(studentobj)+" "+str(subjectlist))
        marks_context_list=[]
        #print(str(marks.objects.all()))
        for sub in subjectlist:
            print(sub.subjectid)
            subid=subject.objects.get(subjectid=sub.subjectid).subjectid
            print("The sub "+str(subid))
            try:
                marksobj=marks.objects.get(msstudentid=sessionid,msubjectid=subid)
                print(str(marksobj.msubjectid))
                marks_context = {}
                marks_context['subjectname']=marksobj.msubjectid
                marks_context['internalmarks']=marksobj.intmarks
                marks_context['externalmarks']=marksobj.extmarks
                marks_context_list.append(marks_context)
            except Exception as e:
                print(str(e))
                continue
        print(marks_context_list)
        return render(request, "seemarks.html", {'markslist': marks_context_list})

@csrf_exempt
def modifymarks(request):
    if request.method == "POST":
        if not request.session.get('sessionid', None):
            return HttpResponse("Login Required")
        sessionid = request.session['sessionid']
        studentid=request.POST.get('studentid')
        subjectid=request.POST.get('subjectid')
        internalmarks=request.POST.get('intmarks')
        externalmarks=request.POST.get('extmarks')
        print(str(studentid))
        try:
            marksobj=marks.objects.get(msstudentid=student.objects.get(studentid=studentid).studentid,msubjectid=subjectid)
            marksobj.intmarks=internalmarks
            marksobj.extmarks=externalmarks
            marksobj.save()
        except Exception as e:
            print("exception"+ str(e))

        m = marks.objects.filter(msubjectid=subjectid)
        markslist = []
        for i in m:
            studentobj = student.objects.get(studentid=i.msstudentid)
            name = studentobj.sname
            studentid = studentobj.studentid
            intmarks = i.intmarks
            extmarks = i.extmarks
            markslist_dict = {}
            markslist_dict['studentid'] = studentid
            markslist_dict['msubjectid'] = subjectid
            markslist_dict['studentname'] = name
            markslist_dict['internalmarks'] = intmarks
            markslist_dict['externalmarks'] = extmarks
            markslist.append(markslist_dict)

        return render(request, "updatemarks.html", {'markslist': markslist})


@csrf_exempt
def seeattendancerecord(request):
    if request.method == 'GET':
        if not request.session.get('sessionid', None):
            return HttpResponse("Login Required")
        sessionid = request.session['sessionid']
        attendanceid=request.GET.get('aid')
        print("The attendance id is "+str(attendanceid))
        try:
            #aid=attendance.objects
            recordobj=attendancerecord.objects.filter(aid=attendanceid)
            print(len(recordobj))
        except Exception as e:
            print("no recordobject")
        record_context_list=[]

        for record in recordobj:
            record_context = {}
            studid=record.studentid
            studentname=student.objects.get(studentid=studid).sname
            status=record.status
            record_context['studentid']=int(str(studid))
            record_context['studentname']=studentname
            record_context['status']=status
            record_context['subjectid']=subject.objects.get(subjectname=record.aid.assubjectid).subjectid
            record_context['branchid']=branch.objects.get(branchname=record.aid.asbranchid).branchid

            record_context['date']=record.aid.date.strftime("%Y-%m-%d")
            record_context['period']=record.aid.period
            record_context['modeofclass']=record.aid.modeofclass

            print(record_context)
            record_context_list.append(record_context)
        print(record_context_list)
        return render(request,"seeattendancerecord.html",{'r':record_context_list})

@csrf_exempt
def viewattendance(request):
    if request.method == 'GET':
        if not request.session.get('sessionid', None):
            return HttpResponse("Login Required")
        sessionid = request.session['sessionid']
        print(str(sessionid))
        student_obj = student.objects.get(studentid=sessionid)
        print(str(student_obj.sbranchid))
        branchid = branch.objects.get(branchname=student_obj.sbranchid).branchid

        subjectlist=student_obj.ssubjectid.all()
        print(str(subjectlist))
        context_percentage_list=[]
        for s in subjectlist:
            context_percentage={}
            context_percentage['subjectid']=s.subjectid
            context_percentage['subjectname']=s.subjectname
            context_percentage['percentage']=calculate_percentage(sessionid,s.subjectid,branchid)
            context_percentage_list.append(context_percentage)



        #subjectlist=student_obj.ssubjectid
        print(str(context_percentage_list))
        return render(request,"viewattendance.html",{'s':context_percentage_list})

@csrf_exempt
def viewsubjectattendance(request):
    if request.method == 'GET':
        if not request.session.get('sessionid', None):
            return HttpResponse("Login Required")
        sessionid = request.session['sessionid']
        subjectid=int(str(request.GET.get('subjectid')))

        student_obj=student.objects.get(studentid=sessionid)
        print(str(student_obj.sbranchid))
        branchid=branch.objects.get(branchname=student_obj.sbranchid).branchid
        attendance_obj = attendance.objects.filter(assubjectid=subject(subjectid),asbranchid=branchid)

        context_attendance_obj_list=[]
        for a in attendance_obj:
            context_attendance_obj = {}
            aid=a.aid
            context_attendance_obj['date']=a.date.strftime("%Y-%m-%d")
            context_attendance_obj['period']=a.period
            context_attendance_obj['modeofclass']=a.modeofclass
            attendancerecordobj=attendancerecord.objects.get(aid=aid,studentid=sessionid)
            context_attendance_obj['status']=attendancerecordobj.status
            context_attendance_obj_list.append(context_attendance_obj)
        print(str(context_attendance_obj_list))
        return render(request,"viewsubjectattendance.html",{'c':context_attendance_obj_list})

def calculate_percentage(sid,id,bid):

    sessionid = sid
    subjectid=subject.objects.get(subjectid=id).subjectid
    branchid = branch.objects.get(branchid=bid).branchid
    attendance_obj = attendance.objects.filter(assubjectid=subject(subjectid), asbranchid=branchid)
    countpresent=0
    countabsent=0
    for a in attendance_obj:
        aid=a.aid
        attendancerecordobj= attendancerecord.objects.get(aid=aid,studentid=sessionid)
        if attendancerecordobj.status=='P':
            countpresent=countpresent+1
        elif attendancerecordobj.status=='A':
            countabsent=countabsent+1
    print(str(countpresent)+" "+str(countabsent))
    if countpresent>0:
        percentage=countpresent*100/(countabsent+countpresent)
    else:
        percentage=0

    return percentage

@csrf_exempt
def uploadmarks(request):
    if request.method =="POST":
        if not request.session.get('sessionid', None):
            return HttpResponse("Login Required")
        sessionid = request.session['sessionid']
        #print(request.POST)
        subjectid=request.POST.get('subjectid')

        l=student.objects.filter(ssubjectid=subjectid)
        branchid = request.POST.get('branchid')

        return render(request,"uploadmarks.html",{'l':l,'branchid':branchid,'subjectid':subjectid})

@csrf_exempt
def logout(request):
    del request.session
    return render(request,"login.html")





















