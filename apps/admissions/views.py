from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse
from django.conf import settings
from django.db.models import Sum, Q

from .models import Student, FeePayment
from .forms import StudentForm, FeePaymentForm

from reportlab.pdfgen import canvas
import openpyxl
from io import BytesIO


# ===================== ADMISSION =====================
def admission_form(request):
    form = StudentForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, "Admission submitted successfully!")
            return redirect('fee')   # 🔥 NO EMAIL → NO ERROR

    return render(request, 'admissions/form.html', {'form': form})


# ===================== FEE MANAGEMENT =====================
def fee_management(request):

    payments = FeePayment.objects.select_related('student').all().order_by('-id')
    total_amount = payments.aggregate(total=Sum('amount'))['total'] or 0
    students = Student.objects.all()
    total_pending = sum([s.balance() for s in students])

    form = FeePaymentForm()

    if request.method == 'POST':
        form = FeePaymentForm(request.POST)

        if form.is_valid():
            payment = form.save()

            # -------- PDF ONLY --------
            buffer = BytesIO()
            p = canvas.Canvas(buffer)

            p.drawString(200, 800, "CSC TRAINING INSTITUTE")
            p.drawString(100, 750, f"Name: {payment.student.first_name}")
            p.drawString(100, 730, f"Amount: ₹{payment.amount}")

            p.save()
            buffer.seek(0)

            return redirect('fee')   # 🔥 NO EMAIL

    return render(request, 'admissions/fee.html', {
        'form': form,
        'payments': payments,
        'students': students,
        'total_amount': total_amount,
        'total_pending': total_pending,
    })


# ===================== STUDENT DETAIL =====================
def student_detail(request, id):
    student = get_object_or_404(Student, id=id)

    return render(request, 'admissions/student_detail.html', {
        'student': student,
        'payments': student.payments.all(),
        'total_paid': student.total_paid(),
        'balance': student.balance()
    })