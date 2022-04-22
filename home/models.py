from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver



# Create your models here.
class SessionYearModel(models.Model):
    id = models.AutoField(primary_key=True)
    session_start_year = models.DateField()
    session_end_year = models.DateField()
    objects = models.Manager()



# Overriding the Default Django Auth User and adding One More Field (user_type)
class CustomUser(AbstractUser):
    user_type_data = ((1, "HOD"), (2, "Staff"), (3, "Student"))
    user_type = models.CharField(default=1, choices=user_type_data, max_length=20)



class AdminHOD(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class Staffs(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete = models.CASCADE)
    gender = models.CharField(max_length=50)
    profile_pic = models.FileField()
    institute_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=13)
    dob = models.DateField(max_length=10, blank=True,null=True)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()



class Courses(models.Model):
    id = models.AutoField(primary_key=True)
    course_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    # def __str__(self):
	#     return self.course_name



class Subjects(models.Model):
    id =models.AutoField(primary_key=True)
    subject_name = models.CharField(max_length=255)
    course_id = models.ForeignKey(Courses, on_delete=models.CASCADE, default=1) #need to give defauult course
    staff_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()



class Students(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete = models.CASCADE)
    gender = models.CharField(max_length=50)
    profile_pic = models.FileField()
    institute_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=13)
    dob = models.DateField()
    address = models.TextField()
    course_id = models.ForeignKey(Courses, on_delete=models.DO_NOTHING, default=1)
    session_year_id = models.ForeignKey(SessionYearModel, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class Attendance(models.Model):
    # Subject Attendance
    id = models.AutoField(primary_key=True)
    subject_id = models.ForeignKey(Subjects, on_delete=models.DO_NOTHING)
    attendance_date = models.DateField()
    session_year_id = models.ForeignKey(SessionYearModel, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class AttendanceReport(models.Model):
    # Individual Student Attendance
    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Students, on_delete=models.DO_NOTHING)
    attendance_id = models.ForeignKey(Attendance, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class LeaveReportStudent(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Students, on_delete=models.CASCADE)
    leave_date = models.CharField(max_length=255)
    leave_message = models.TextField()
    leave_status = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class LeaveReportStaff(models.Model):
    id = models.AutoField(primary_key=True)
    staff_id = models.ForeignKey(Staffs, on_delete=models.CASCADE)
    leave_date = models.CharField(max_length=255)
    leave_message = models.TextField()
    leave_status = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class FeedBackStudent(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Students, on_delete=models.CASCADE)
    feedback = models.TextField()
    feedback_reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class FeedBackStaffs(models.Model):
    id = models.AutoField(primary_key=True)
    staff_id = models.ForeignKey(Staffs, on_delete=models.CASCADE)
    feedback = models.TextField()
    feedback_reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()



class NotificationStudent(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Students, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class NotificationStaffs(models.Model):
    id = models.AutoField(primary_key=True)
    stafff_id = models.ForeignKey(Staffs, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class StudentResult(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Students, on_delete=models.CASCADE)
    subject_id = models.ForeignKey(Subjects, on_delete=models.CASCADE)
    subject_exam_marks = models.FloatField(default=0)
    subject_assignment_marks = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


#now creating signal in django so when new user create I will add a new row  in Admin,staff, student with it's id in admin_id column
#creating @receiver(post_save,sender=CoustomUser).So This will Run only when data added in coustomUser

@receiver(post_save,sender=CustomUser)

#Now Creating a Fuction Which Add data into Admin,staff,Student Table
#Taking parameter sender, instance, created here sender is class which call this method instance is current inserted data model created is True/ False,
#True When data inserted 
def create_user_profile(sender,instance,created,**kwargs): 
    #If created is true means data inserted
    #then I will insert data into other table
    if created:
        #if user_type=1 Then I will add row in admin Table with Admin Id
        if instance.user_type==1:
            #Now calling adminHOD.objects.cretae() and passing admin=instance
            #Here instance is CustomUser
            AdminHOD.objects.create(admin=instance)
            #if user_type=2 Then I will add row in staff Table with staff Id
            #Now calling staffs.objects.cretae() and passing admin=instance
            #Here instance is CustomUser
        if instance.user_type==2:
            Staffs.objects.create(admin=instance, phone="", dob="2020-11-11", institute_name="",  gender="", address="",  profile_pic="")
            #if user_type=2 Then I will add row in staff Table with staff Id
            #Now calling students.objects.cretae() and passing admin=instance
            #Here instance is CustomUser
        if instance.user_type==3:
            Students.objects.create(admin=instance, course_id=Courses.objects.get(id=1), phone="", institute_name="", address="", gender="", dob="2020-11-11", session_year_id=SessionYearModel.objects.get(id=1), profile_pic="")

#creating @receiver(post_save,sender=CoustomUser).So This will Run only when data added in coustomUser
#this method will call after create_user_profile() Execution
@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs): 
    #If created is true means data inserted
    #then I will insert data into other table
    #if user_type=1 Then I will add row in admin Table with Admin Id
    if instance.user_type==1:
        #Now calling adminHOD.objects.cretae() and passing admin=instance
        #Here instance is CustomUser
        instance.adminhod.save()
        #if user_type=2 Then I will add row in staff Table with staff Id
        #Now calling staffs.objects.cretae() and passing admin=instance
        #Here instance is CustomUser
    if instance.user_type==2:
        instance.staffs.save()
        #if user_type=2 Then I will add row in staff Table with staff Id
        #Now calling students.objects.cretae() and passing admin=instance
        #Here instance is CustomUser
    if instance.user_type==3:
        instance.students.save()
           