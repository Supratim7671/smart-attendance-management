from django.db import models

# Create your models here.
class staffs(models.Model):
    staffid = models.AutoField(primary_key=True)
    password = models.CharField(blank=False,default='', max_length=500)
    email = models.CharField(blank=False, max_length=500)
    role = models.CharField(blank=False, default="admin", max_length=500)
    def __str__(self):
        return str(self.staffid)


class branch(models.Model):
    branchid=models.AutoField(primary_key=True)
    branchname=models.CharField(blank=False,default='',max_length=500)
    year=models.IntegerField(blank=False,default=0)
    def __str__(self):
        return str(self.branchname)


class subject(models.Model):
    subjectid=models.AutoField(primary_key=True)
    subjectname=models.CharField(blank=False,default='',max_length=500)
    branchid=models.ForeignKey(branch,on_delete=models.CASCADE)
    #intmarks=models.IntegerField(blank=False,default=0)
    #extmarks=models.IntegerField(blank=False,default=0)
    def __str__(self):
        return str(self.subjectname)

class marks(models.Model):
    marksid=models.AutoField(primary_key=True)
    intmarks= models.IntegerField(blank=False, default=0)
    extmarks= models.IntegerField(blank=False, default=0)
    msubjectid=models.ForeignKey(subject,on_delete=models.CASCADE,default='')
    msstudentid=models.ForeignKey(staffs,on_delete=models.CASCADE,default='')


class faculty(models.Model):
    facultyid=models.ForeignKey(staffs,on_delete=models.CASCADE)
    fname=models.CharField(blank=False,default='',max_length=500)
    fbranchid=models.ForeignKey(branch,default='',on_delete=models.CASCADE)
    #fsubjectid=models.ForeignKey(subject,default='',on_delete=models.CASCADE)
    fpost = models.CharField(blank=False, default=0, max_length=200)
    #fage = models.IntegerField(blank=False, default=0)
    fmobile = models.IntegerField(blank=False, default=0)
    #femail = models.CharField(blank=False, default='', max_length=500)
    faddress = models.CharField(blank=False, default='', max_length=500)
    #fcity = models.CharField(blank=False, default='', max_length=500)
    #fstate = models.CharField(blank=False, default='', max_length=500)
    def __str__(self):
        return str(self.fname)


class student(models.Model):
    studentid = models.ForeignKey(staffs, on_delete=models.CASCADE)
    sroll = models.IntegerField(blank=False, default=0)
    sname = models.CharField(blank=False, default='', max_length=500)
    syear = models.CharField(blank=False, default='', max_length=500)
    sbranchid = models.ForeignKey(branch,default='', on_delete=models.CASCADE)
    #ssubjectid = models.ForeignKey(subject,default='',on_delete=models.CASCADE)
    ssubjectid=models.ManyToManyField(subject,default='',blank=True)
    # spost = models.CharField(blank=False, default=0, max_length=200)
    # sage = models.IntegerField(blank=False, default=0)
    smobile = models.IntegerField(blank=False, default=0)
    # femail = models.CharField(blank=False, default='', max_length=500)
    saddress = models.CharField(blank=False, default='', max_length=500)

    # scity = models.CharField(blank=False, default='', max_length=500)
    # sstate = models.CharField(blank=False, default='', max_length=500)




class attendance(models.Model):
    aid=models.AutoField(primary_key=True)
    asbranchid=models.ForeignKey(branch,on_delete=models.CASCADE)
    assubjectid=models.ForeignKey(subject,on_delete=models.CASCADE,default='')
    date=models.DateField(blank=False)
    period=models.IntegerField(blank=False,default=0)
    modeofclass=models.CharField(blank=False,default='L',max_length=500)#L,P,T


class attendancerecord(models.Model):
    rid=models.AutoField(primary_key=True)
    aid=models.ForeignKey(attendance,on_delete=models.CASCADE)
    studentid=models.ForeignKey(staffs,on_delete=models.CASCADE)
    status=models.CharField(blank=False,default='',max_length=500)

