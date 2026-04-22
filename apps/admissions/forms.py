from django import forms
from .models import Student, FeePayment


# -------- Student Form --------
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


class StudentForm(forms.ModelForm):
    course = forms.ChoiceField(
        choices=COURSE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    gender = forms.ChoiceField(
        choices=GENDER_CHOICES,
        widget=forms.RadioSelect
    )

    class Meta:
        model = Student
        fields = ['name', 'email', 'phone', 'course', 'gender']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
        }


# -------- Fee Payment Form --------
class FeePaymentForm(forms.ModelForm):

    PAYMENT_CHOICES = [
        ('UPI', 'UPI'),
        ('Cash', 'Cash'),
        ('Card', 'Card'),
        ('Net Banking', 'Net Banking'),
    ]

    payment_mode = forms.ChoiceField(
        choices=PAYMENT_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    # 🔥 IMPORTANT (YOU MISSED THIS)
    payment_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )

    reference_id = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    remarks = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
    )

    class Meta:
        model = FeePayment
        fields = [
            'student',
            'amount',
            'payment_mode',
            'payment_date',   # 🔥 ADDED
            'reference_id',
            'remarks'
        ]

        widgets = {
            'student': forms.Select(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
        }