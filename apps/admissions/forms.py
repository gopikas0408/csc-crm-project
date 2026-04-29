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
        choices=[('', 'Select Gender')] + GENDER_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
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
        
        #--------VALIDATIONS--------
        
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Student.objects.filter(email=email).exists():
            raise forms.ValidationError("A student with this email already exists.")
        return email
    
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not phone:
            raise forms.ValidationError("Phone number is required.")
        if not phone.isdigit():
            raise forms.ValidationError("Phone number must contain only digits.")
        if len(phone) < 10:
            raise forms.ValidationError("Phone number must be at least 10 digits long.")
        return phone

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
        
        #--------VALIDATIONS--------
        
    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount is None:
            raise forms.ValidationError("Amount is required.")
        if amount <= 0:
            raise forms.ValidationError("Amount must be greater than 0")
        return amount