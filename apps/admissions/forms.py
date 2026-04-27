from django import forms
from .models import Student, FeePayment


# -------- Student Form --------

class StudentForm(forms.ModelForm):

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

    STATUS_CHOICES = [
        ('Enquiry', 'Enquiry'),
        ('Confirmed', 'Confirmed'),
        ('Enrolled', 'Enrolled'),
        ('Dropped', 'Dropped'),
    ]

    course = forms.ChoiceField(
        choices=COURSE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    gender = forms.ChoiceField(
        choices=GENDER_CHOICES,
        widget=forms.RadioSelect
    )

    admission_status = forms.ChoiceField(
        choices=STATUS_CHOICES,
        required=False,
        widget=forms.HiddenInput()   # hidden 
    )

    class Meta:
        model = Student
        fields = [
            'first_name','last_name',
            'email','phone','dob','gender',
            'address','guardian_name','guardian_phone',
            'course','batch','admission_status',
            'total_fee'
        ]

        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),

            'dob': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),

            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2
            }),

            'guardian_name': forms.TextInput(attrs={'class': 'form-control'}),
            'guardian_phone': forms.TextInput(attrs={'class': 'form-control'}),

            'total_fee': forms.NumberInput(attrs={
                'class': 'form-control',
                'readonly': 'readonly'   #  auto fee 
            }),
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

    payment_date = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control'
        })
    )

    reference_id = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    remarks = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3
        })
    )

    class Meta:
        model = FeePayment
        fields = [
            'student',
            'amount',
            'payment_mode',
            'payment_date',
            'reference_id',
            'remarks'
        ]

        widgets = {
            'student': forms.Select(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
        }