import secrets
import time

from django.core.mail import send_mail
from django.conf import settings
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import render,  redirect
from .models import Student
from .models import Document,AdminUser
from .models import Contact
from django.core.exceptions import ValidationError

def home(request):
    return render(request, 'index.html')


def documents(request):
    return render(request, 'documents.html')



def thanqu(request):
    return render(request, 'thanqu.html')


def admin_login(request):
    return render(request, 'admin_login.html')



def contact(request):

    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

       
        Contact.objects.create(
            name=name,
            email=email,
            message=message
        )

        return redirect('thanqu')   

    return render(request, 'contact.html')



def download(request):
    student_id = request.session.get('student_id')

    if not student_id:
        return redirect('login')

    student = Student.objects.get(id=student_id)
    document = Document.objects.filter(student=student).first()

    return render(request, 'download.html', {'document': document})

def signup(request):
    error = {}
    form_data = {}

    if request.method == "POST":

        form_data = {
            'first_name': request.POST.get('first_name', '').strip(),
            'f_name': request.POST.get('f_name', '').strip(),
            'email': request.POST.get('email', '').strip(),
            'mobile': request.POST.get('mobile', '').strip(),
            'roll': request.POST.get('roll', '').strip(),
            'branch': request.POST.get('branch', '').strip(),
            'year': request.POST.get('year', '').strip(),
            'semester': request.POST.get('semester', '').strip(),
        }

        try:
          
            student = Student(
                first_name=form_data['first_name'],
                f_name=form_data['f_name'],
                email=form_data['email'],
                mobile=form_data['mobile'],
                roll=form_data['roll'],
                branch=form_data['branch'],
                year=form_data['year'],
                semester=form_data['semester']
            )

            
            student.full_clean()

            # Generate 6-digit OTP
            otp = str(secrets.randbelow(900000) + 100000)

            # Store registration data temporarily in session
            request.session['pending_student'] = form_data

            # Store OTP securely as a hash
            request.session['otp_hash'] = make_password(otp)

            # OTP expires after 5 minutes
            request.session['otp_expiry'] = time.time() + 300

            # Reset OTP attempts
            request.session['otp_attempts'] = 0

            request.session.modified = True

            # Send OTP to email
            send_mail(
                subject='SecureDocs - Email Verification OTP',

                message=(
                    f'Hello {form_data["first_name"]},\n\n'
                    f'Your SecureDocs verification OTP is: {otp}\n\n'
                    f'This OTP is valid for 5 minutes.\n\n'
                    f'If you did not request this registration, '
                    f'please ignore this email.'
                ),

                from_email=settings.DEFAULT_FROM_EMAIL,

                recipient_list=[
                    form_data['email']
                ],

                fail_silently=False,
            )

            # Go to OTP verification page
            return redirect('verify_otp')

        except ValidationError as e:

            error = e.message_dict

        except Exception:

            error = {
                'email': [
                    'Unable to send OTP. Please try again.'
                ]
            }

    return render(request, 'signup.html', {
        'error': error,
        'form_data': form_data
    })



def verify_otp(request):

    # Get temporary registration information
    pending_student = request.session.get('pending_student')

    # If no registration is waiting for verification
    if not pending_student:
        return redirect('signup')

    error = ""

    if request.method == "POST":

        entered_otp = request.POST.get('otp', '').strip()

        # Check OTP is entered
        if not entered_otp:

            error = "Please enter the OTP."

        else:

            # Get OTP expiry time
            otp_expiry = request.session.get(
                'otp_expiry',
                0
            )

            # Check OTP expiration
            if time.time() > otp_expiry:

                error = "OTP has expired. Please request a new OTP."

            else:

                # Get number of attempts
                attempts = request.session.get(
                    'otp_attempts',
                    0
                )

                # Maximum 5 attempts
                if attempts >= 5:

                    error = (
                        "Too many incorrect attempts. "
                        "Please request a new OTP."
                    )

                else:

                    # Increase attempt count
                    request.session['otp_attempts'] = attempts + 1

                    otp_hash = request.session.get('otp_hash')

                    # Check OTP
                    if otp_hash and check_password(
                        entered_otp,
                        otp_hash
                    ):

                        try:

                            # NOW create the Student
                            student = Student(
                                first_name=pending_student['first_name'],
                                f_name=pending_student['f_name'],
                                email=pending_student['email'],
                                mobile=pending_student['mobile'],
                                roll=pending_student['roll'],
                                branch=pending_student['branch'],
                                year=pending_student['year'],
                                semester=pending_student['semester']
                            )

                            # Validate again before saving
                            student.full_clean()

                            # Save student to database
                            student.save()

                            # Remove temporary session data
                            request.session.pop(
                                'pending_student',
                                None
                            )

                            request.session.pop(
                                'otp_hash',
                                None
                            )

                            request.session.pop(
                                'otp_expiry',
                                None
                            )

                            request.session.pop(
                                'otp_attempts',
                                None
                            )

                            # Registration successful
                            return redirect('thanqu')

                        except ValidationError:

                            error = (
                                "Registration information is "
                                "no longer valid."
                            )

                    else:

                        remaining = 4 - attempts

                        if remaining > 0:
                            error = (
                                f"Invalid OTP. "
                                f"You have {remaining} "
                                f"attempt(s) remaining."
                            )
                        else:
                            error = (
                                "Invalid OTP. "
                                "Please request a new OTP."
                            )

    return render(
        request,
        'verify_otp.html',
        {
            'error': error,
            'email': pending_student.get('email')
        }
    )


def resend_otp(request):

    pending_student = request.session.get('pending_student')

    if not pending_student:
        return redirect('signup')

    if request.method == "POST":

        # Generate new 6-digit OTP
        otp = str(secrets.randbelow(900000) + 100000)

        # Save new OTP
        request.session['otp_hash'] = make_password(otp)

        # New 5-minute expiry
        request.session['otp_expiry'] = time.time() + 300

        # Reset attempts
        request.session['otp_attempts'] = 0

        request.session.modified = True

        try:

            send_mail(
                subject='SecureDocs - New OTP',
                message=(
                    f'Hello {pending_student["first_name"]},\n\n'
                    f'Your new SecureDocs verification OTP is: {otp}\n\n'
                    f'This OTP will expire in 5 minutes.'
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[pending_student['email']],
                fail_silently=False,
            )

            return redirect('verify_otp')

        except Exception:
            return render(request, 'verify_otp.html', {
                'error': 'Unable to send OTP. Please try again.',
                'email': pending_student.get('email')
            })

    return redirect('verify_otp')

def login(request):
    error = ""

    if request.method == "POST":
        first_name = request.POST.get('first_name', '').strip()
        roll = request.POST.get('roll', '').strip()
        email = request.POST.get('email', '').strip()

        if not first_name or not roll or not email:
            error = "All fields are required"
            return render(request, 'login.html', {'error': error})

        try:
            student = Student.objects.get(
                first_name__iexact=first_name,
                roll__iexact=roll,
                email__iexact=email
            )

            request.session['student_id'] = student.id
            return redirect('documents')

        except Student.DoesNotExist:
            error = "Invalid details"

    return render(request, 'login.html', {'error': error})

def upload(request):
    student_id = request.session.get('student_id')

    if not student_id:
        return redirect('login')

    student = Student.objects.get(id=student_id)


    document = Document.objects.filter(student=student).first()

    if request.method == "POST":

        aadhar = request.FILES.get('aadhar')
        caste = request.FILES.get('caste')
        tenth = request.FILES.get('tenth')
        plus2 = request.FILES.get('plus2')
        income = request.FILES.get('income')
        mother = request.FILES.get('mother')
        father = request.FILES.get('father')
        photo = request.FILES.get('photo')
        dmc = request.FILES.get('dmc')

    
        if document:
            if aadhar: document.aadhar = aadhar
            if caste: document.caste = caste
            if tenth: document.tenth = tenth
            if plus2: document.plus2 = plus2
            if income: document.income = income
            if mother: document.mother_aadhar = mother
            if father: document.father_aadhar = father
            if photo: document.photo = photo
            if dmc: document.dmc = dmc

            document.save()

        
        else:
            Document.objects.create(
                student=student,
                aadhar=aadhar,
                caste=caste,
                tenth=tenth,
                plus2=plus2,
                income=income,
                mother_aadhar=mother,
                father_aadhar=father,
                photo=photo,
                dmc=dmc
            )

        return redirect('thanqu')

    return render(request, 'upload.html', {'document': document})



def dashboard(request):
    return render(request, 'dashboard.html')



def register_admin(request):
    error = {}
    form_data = {}

    if request.method == "POST":
        form_data = request.POST 

        try:
            admin = AdminUser(
                name=request.POST.get('name'),

                phone=request.POST.get('phone'),
                admin_id=request.POST.get('admin_id'),
                password=request.POST.get('password')
            )

            admin.full_clean()   
            admin.save()
            print("✅ Admin Registered Successfully")


            return redirect('admin_login')

        except ValidationError as e:
            error = e.message_dict   

    return render(request, 'register_admin.html', {
        'error': error,
        'form_data': form_data
    })




def admin_login(request):
    error = False

    if request.method == "POST":
        admin_id = request.POST.get('admin_id')
        password = request.POST.get('password')

        user = AdminUser.objects.filter(
            admin_id=admin_id,
            password=password
        ).first()

        if user:
            return redirect('prvdown')  # search page
        else:
            error = True

    return render(request, 'admin_login.html', {'error': error})

from django.shortcuts import render
from .models import Student, Document


def prvdown(request):
    roll = request.POST.get('roll')
    year = request.POST.get('year')
    branch = request.POST.get('branch')
    semester = request.POST.get('semester')

    students = Student.objects.all()

    # Apply filters
    if roll:
        students = students.filter(roll=roll)

    if branch:
        students = students.filter(branch=branch)

    if year:
        students = students.filter(year=year)

    if semester:
        students = students.filter(semester=semester)

    data = []

    for student in students:
        doc = Document.objects.filter(student=student).first()

        data.append({
            'student': student,
            'document': doc
        })

    return render(request, 'prvdown.html', {'data': data})




def logout(request):
    request.session.flush()
    return redirect('home')


def admin_view(request):
    student = None
    document = None

    if request.method == "POST":
        roll = request.POST.get('roll')

        try:
            student = Student.objects.get(roll=roll)
            document = Document.objects.filter(student=student).first()
        except Student.DoesNotExist:
            student = None

    return render(request, 'admin_view.html', {
        'student': student,
        'document': document
    })
   