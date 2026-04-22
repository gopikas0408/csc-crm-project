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

    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    course = models.CharField(max_length=100, choices=COURSE_CHOICES)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)

    total_fee = models.IntegerField(default=0)   # 💰 Total course fee

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    # 🔥 TOTAL PAID (OPTIMIZED)
    def total_paid(self):
        return self.payments.aggregate(total=Sum('amount'))['total'] or 0

    # 🔥 BALANCE
    def balance(self):
        return self.total_fee - self.total_paid()


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

    # ✅ Manual date selection (UI will work properly)
    payment_date = models.DateField()

    reference_id = models.CharField(max_length=100, blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.name} - ₹{self.amount}"