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

        # Save to database (optional but recommended)
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
        form_data = request.POST

        try:
            student = Student(
                first_name=request.POST.get('first_name'),
                f_name=request.POST.get('f_name'),
                email=request.POST.get('email'),
                mobile=request.POST.get('mobile'),
                roll=request.POST.get('roll'),
                branch=request.POST.get('branch'),
                year=request.POST.get('year'),           
                semester=request.POST.get('semester')   
            )

            student.full_clean()
            student.save()

            return redirect('thanqu')

        except ValidationError as e:
            error = e.message_dict

    return render(request, 'signup.html', {
        'error': error,
        'form_data': form_data
    })
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
   