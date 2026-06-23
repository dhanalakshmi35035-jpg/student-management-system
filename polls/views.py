from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Question, Choice,Student
from .forms import StudentForm, AttendanceForm, MarkForm,FeeForm
from .models import Attendance,Mark,Fee
from django.http import HttpResponse
from reportlab.pdfgen import canvas
import os
from django.conf import settings
from reportlab.lib.utils import ImageReader
from reportlab.platypus import Image

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {
        'latest_question_list': latest_question_list,
    }
    return render(request, 'polls/index.html', context)

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    try:
        selected_choice = question.choice_set.get(
            pk=request.POST['choice']
        )
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })

    selected_choice.votes += 1
    selected_choice.save()

    return HttpResponseRedirect(
        reverse('results', args=(question.id,))
    )
from django.shortcuts import render

def home(request):
    return render(request, 'polls/home.html')
def about(request):
    return render(request, 'polls/about.html')
def student_list(request):




   query = request.GET.get('q')


   if query:
    students = Student.objects.filter(name__icontains=query)
   else:
    students = Student.objects.all()

   return render(
    request,
    'polls/student_list.html',
    {'students': students}
)


def user_login(request):

    if request.method == "POST":

        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return HttpResponse("Login Failed")

    return render(request, 'polls/login.html')


def dashboard(request):
    total_students = Student.objects.count()
    total_attendance = Attendance.objects.count()
    total_marks = Mark.objects.count()
    total_fees = Fee.objects.count()

    present_count = Attendance.objects.filter(status='Present').count()
    absent_count = Attendance.objects.filter(status='Absent').count()
    leave_count = Attendance.objects.filter(status='Leave').count()  
    
    
    context = {
        'total_students': total_students,
        'total_attendance': total_attendance,
        'present_count': present_count,
        'absent_count': absent_count,
        'leave_count': leave_count,
        'total_marks': total_marks,
        'total_fees': total_fees,
    
    }

    return render(request, 'polls/dashboard.html', context)    
def user_logout(request):
    logout(request)
    return redirect('login')

from .forms import StudentForm

def add_student(request):

    if request.method == "POST":
        form = StudentForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('student_list')

    else:
        form = StudentForm()

    return render(request, 'polls/add_student.html', {'form': form})

def edit_student(request, student_id):

    student = get_object_or_404(Student, id=student_id)

    if request.method == "POST":
        form = StudentForm(request.POST, instance=student)

        if form.is_valid():
            form.save()
            return redirect('student_list')

    else:
        form = StudentForm(instance=student)

    return render(request, 'polls/edit_student.html', {'form': form})
def delete_student(request, student_id):

    student = get_object_or_404(Student, id=student_id)

    student.delete()

    return HttpResponseRedirect(reverse('student_list'))
def mark_attendance(request):

    if request.method == "POST":
        form = AttendanceForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('student_list')

    else:
        form = AttendanceForm()

    return render(request, 'polls/mark_attendance.html', {'form': form})

def attendance_list(request):

    attendance_records = Attendance.objects.all()

    return render(
        request,
        'polls/attendance_list.html',
        {'attendance_records': attendance_records}
    )



def add_marks(request):

    if request.method == "POST":
        form = MarkForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('marks_list')

    else:
        form = MarkForm()

    return render(request, 'polls/add_marks.html', {'form': form})


def marks_list(request):
    marks = Mark.objects.all()

    return render(
        request,
        'polls/marks_list.html',
        {'marks': marks}
    )
def add_fee(request):

    if request.method == "POST":
        form = FeeForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('fee_list')

    else:
        form = FeeForm()

    return render(request, 'polls/add_fee.html', {'form': form})


def fee_list(request):
    fees = Fee.objects.all()

    return render(
        request,
        'polls/fee_list.html',
        {'fees': fees}
    )
def generate_pdf(request):

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="student_report.pdf"'

    p = canvas.Canvas(response)

    p.drawString(100, 800, "Student Management System Report")

    p.drawString(100, 770, f"Total Students: {Student.objects.count()}")

    p.drawString(100, 740, f"Attendance Records: {Attendance.objects.count()}")

    p.drawString(100, 710, f"Marks Records: {Mark.objects.count()}")

    p.drawString(100, 680, f"Fee Records: {Fee.objects.count()}")

    p.showPage()
    p.save()

    return response
def student_pdf(request, id):

    student = get_object_or_404(Student, id=id)

    attendance = Attendance.objects.filter(student=student)
    marks = Mark.objects.filter(student=student).first()
    fee = Fee.objects.filter(student=student).first()


    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{student.name}_report.pdf"'


    p = canvas.Canvas(response)
    # College Logo

    logo_path = os.path.join(
      settings.BASE_DIR,
      'static',
      'college_logo.png'

    )

    p.drawImage(
        ImageReader(logo_path),
        260,
        730,
        width=100,
        height=100
    )



    # University Header
    p.setFont("Helvetica-Bold", 16)
    p.drawCentredString(300, 680, "ANNAMALAI UNIVERSITY")

    p.setFont("Helvetica-Bold", 14)
    p.drawCentredString(300, 650, "Student Management System")

    p.setFont("Helvetica-Bold", 12)
    p.drawCentredString(300, 620, "Student Detailed Report")
    # Student Details

    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, 650, "Student Details")


    p.drawString(50, 620, f"Name : {student.name}")
    p.drawString(50, 590, f"Roll No : {student.roll_no}")
    p.drawString(50, 560, f"Department : {student.department}")
    p.drawString(50, 530, f"Email : {student.email}")


    # Marks Details

    p.drawString(50, 480, "Marks Details")


    if marks:
       
        p.drawString(50, 450, f"Sensors : {marks.Sensors}")
        p.drawString(50, 420, f"IndustrialInstrumentation : {marks.IndustrialInstrumentation}")
        p.drawString(50, 390, f"ProcessControl : {marks.ProcessControl}")
        p.drawString(50, 360, f"Total : {marks.total()}")
        p.drawString(50, 330, f"Average : {marks.average():.2f}")


    # Attendance

        p.drawString(50, 280, "Attendance Details")

        y = 250

    for att in attendance:
        p.drawString(100, y, f"{att.date} - {att.status}")
        y -= 25


    # Fee

        # Fee Details

        y = y - 20

        

    if fee:

          p.drawString(100, y-50, f"Total Fee : {fee.total_fee}")
          p.drawString(100, y-80, f"Paid Fee : {fee.paid_fee}")
          p.drawString(100, y-110, f"Balance : {fee.balance()}")


          p.showPage()
          p.save()

    return response