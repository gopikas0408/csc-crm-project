from django.db import models
from django.db.models import Sum
from django.core.validators import RegexValidator


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

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    email = models.EmailField(blank=True, null=True)

    phone = models.CharField(
        max_length=10,
        validators=[RegexValidator(r'^\d{10}$', 'Enter valid 10 digit number')]
    )

    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)

    dob = models.DateField(null=True, blank=True)
    address = models.TextField(blank=True, null=True)

    guardian_name = models.CharField(max_length=100, blank=True, null=True)

    guardian_phone = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        validators=[RegexValidator(r'^\d{10}$', 'Enter valid 10 digit number')]
    )

    course = models.CharField(max_length=100, choices=COURSE_CHOICES)

    batch = models.CharField(
        max_length=100,
        choices=BATCH_CHOICES,
        null=True,
        blank=True
    )

    total_fee = models.IntegerField(default=0)

    admission_status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Enquiry'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    # -------- AUTO FEE --------
    def save(self, *args, **kwargs):

        fee_map = {
            "Python Developer": 20000,
            "Java Developer": 22000,
            "Web Development": 18000,
            "Data Analyst": 25000,
            "Data Scientist": 30000,
            "AI & ML": 35000,
        }

        self.total_fee = fee_map.get(self.course, 0)

        super().save(*args, **kwargs)

    # -------- TOTAL PAID --------
    def total_paid(self):
        total = self.payments.aggregate(total=Sum('amount'))['total']
        return total or 0

    # -------- BALANCE --------
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

    reference_id = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    remarks = models.TextField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student} - ₹{self.amount}"