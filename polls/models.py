from  django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    def __str__(self):
        return self.question_text

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    def __str__(self):
        return self.choice_text

class Student(models.Model):
    name = models.CharField(max_length=100)
    roll_no = models.IntegerField(unique=True)
    department = models.CharField(max_length=50)
    email = models.EmailField()

    def __str__(self):
        return self.name
    
class Attendance(models.Model):

    STATUS_CHOICES = [
        ('Present', 'Present'),
        ('Absent', 'Absent'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)

    class Meta:
        unique_together = ('student', 'date')
    def __str__(self):
        return f"{self.student.name} - {self.date}"    
    
class Mark(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    Sensors = models.IntegerField(
    validators=[MinValueValidator(0), MaxValueValidator(100)]
)

    IndustrialInstrumentation = models.IntegerField(
    validators=[MinValueValidator(0), MaxValueValidator(100)]
)

    ProcessControl = models.IntegerField(
    validators=[MinValueValidator(0), MaxValueValidator(100)]
)

    def total(self):
        return self.Sensors + self.IndustrialInstrumentation + self.ProcessControl 

    def average(self):
        return self.total() / 3

    def __str__(self):
        return self.student.name
    
class Fee(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    total_fee = models.PositiveIntegerField()
    paid_fee = models.PositiveIntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['student'],
                name='unique_student_fee'
            )
        ]

    def balance(self):
        return self.total_fee - self.paid_fee

    def __str__(self):
        return self.student.name    

    def balance(self):
        return self.total_fee - self.paid_fee

    def __str__(self):
        return self.student.name    