from django.db import models
from django.core.validators import RegexValidator, EmailValidator


class Student(models.Model):
    first_name = models.CharField(max_length=50)
    f_name = models.CharField(max_length=50)

    email = models.EmailField(unique=True)

    mobile = models.CharField(
        max_length=10,
        validators=[
            RegexValidator(
                regex=r'^[6-9]\d{9}$',   
                message="Enter valid 10-digit mobile number"
            )
        ]
    )

    roll = models.CharField(
        max_length=7,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^\d{7}$',   
                message="Roll number must be exactly 7 digits"
            )
        ]
    )

    branch = models.CharField(max_length=50)
    year = models.CharField(max_length=20)
    semester = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.first_name} {self.f_name} ({self.roll})"
    

class Document(models.Model):
    student = models.ForeignKey('Student', on_delete=models.CASCADE)

    aadhar = models.FileField(upload_to='documents/', null=True, blank=True)
    caste = models.FileField(upload_to='documents/', null=True, blank=True)
    tenth = models.FileField(upload_to='documents/', null=True, blank=True)
    plus2 = models.FileField(upload_to='documents/', null=True, blank=True)
    income = models.FileField(upload_to='documents/', null=True, blank=True)

    mother_aadhar = models.FileField(upload_to='documents/', null=True, blank=True)
    father_aadhar = models.FileField(upload_to='documents/', null=True, blank=True)

    photo = models.ImageField(upload_to='photos/', null=True, blank=True)
    dmc = models.FileField(upload_to='documents/', null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    



class AdminUser(models.Model):
    name = models.CharField(max_length=100)

    

    phone = models.CharField(
        max_length=10,
        validators=[
            RegexValidator(
                regex=r'^[6-9]\d{9}$',
                message="Enter valid 10-digit phone number"
            )
        ]
    )

    admin_id = models.CharField(max_length=50, unique=True)

    password = models.CharField(max_length=50)

    def __str__(self):
        return self.admin_id
    
class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name