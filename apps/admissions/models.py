from django.db import models
from django.db.models import Sum


# ------------------ STUDENT MODEL ------------------

class Student(models.Model):

    COURSE_CHOICES = [
        ('Python Developer', 'Python Developer'),
        ('Java Developer', 'Java Developer'),
        ('Web Development', 'Web Development'),
        ('Data Analyst', 'Data Analyst'),
        ('Data Scientist', 'Data Scientist'),
        ('AI & ML', 'AI & ML'),
    ]

    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
    ]

    BATCH_CHOICES = [
        ('Batch A - Morning', 'Batch A - Morning'),
        ('Batch B - Evening', 'Batch B - Evening'),
    ]

    STATUS_CHOICES = [
        ('Enquiry', 'Enquiry'),
        ('Confirmed', 'Confirmed'),
        ('Enrolled', 'Enrolled'),
        ('Dropped', 'Dropped'),
    ]

    #  NAME SPLIT
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    #  BASIC
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=15)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)

    #  EXTRA
    dob = models.DateField(null=True, blank=True)
    address = models.TextField(blank=True, null=True)

    guardian_name = models.CharField(max_length=100, blank=True, null=True)
    guardian_phone = models.CharField(max_length=15, blank=True, null=True)

    #  COURSE
    course = models.CharField(max_length=100, choices=COURSE_CHOICES)
    batch = models.CharField(max_length=100, choices=BATCH_CHOICES, null=True, blank=True)

    total_fee = models.IntegerField(default=20000)

    admission_status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Enquiry'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    #  AUTO FEE
    def save(self, *args, **kwargs):

        if self.course == "Python Developer":
            self.total_fee = 20000

        elif self.course == "Java Developer":
            self.total_fee = 22000

        elif self.course == "Web Development":
            self.total_fee = 18000

        elif self.course == "Data Analyst":
            self.total_fee = 25000

        elif self.course == "Data Scientist":
            self.total_fee = 30000

        elif self.course == "AI & ML":
            self.total_fee = 35000

        super().save(*args, **kwargs)

    #  TOTAL PAID
    def total_paid(self):
        return self.payments.aggregate(total=Sum('amount'))['total'] or 0

    #  BALANCE
    def balance(self):
        return max(self.total_fee - self.total_paid(), 0)


# ------------------ FEE PAYMENT MODEL ------------------

class FeePayment(models.Model):

    PAYMENT_CHOICES = [
        ('UPI', 'UPI'),
        ('Cash', 'Cash'),
        ('Card', 'Card'),
        ('Net Banking', 'Net Banking'),
    ]

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="payments"
    )

    amount = models.IntegerField()

    payment_mode = models.CharField(
        max_length=50,
        choices=PAYMENT_CHOICES
    )

    payment_date = models.DateField()

    reference_id = models.CharField(max_length=100, blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.first_name} {self.student.last_name} - ₹{self.amount}"