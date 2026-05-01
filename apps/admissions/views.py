from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse
from django.core.mail import send_mail, EmailMessage
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
            student = form.save()

            full_name = f"{student.first_name} {student.last_name}"

            messages.success(request, "🎉 Admission submitted successfully!")

            # -------- STUDENT EMAIL --------
            if student.email and settings.EMAIL_HOST_USER:
                try:
                    send_mail(
                        subject='CSC Admission Successful',
                        message=f"""
Hi {full_name},

Your admission has been successfully completed!

Course: {student.course}
Phone: {student.phone}

Welcome to CSC 🚀
""",
                        from_email=settings.EMAIL_HOST_USER,
                        recipient_list=[student.email],
                        fail_silently=True
                    )
                except Exception as e:
                    print("Student Email Error:", e)

            # -------- ADMIN EMAIL --------
            if settings.EMAIL_HOST_USER:
                try:
                    send_mail(
                        subject='🚨 New Admission',
                        message=f"""
New Admission:

Name: {full_name}
Email: {student.email}
Phone: {student.phone}
Course: {student.course}
""",
                        from_email=settings.EMAIL_HOST_USER,
                        recipient_list=[settings.ADMIN_EMAIL],
                        fail_silently=True
                    )
                except Exception as e:
                    print("Admin Email Error:", e)

            return redirect('fee')

    return render(request, 'admissions/form.html', {'form': form})


# ===================== FEE MANAGEMENT =====================
def fee_management(request):

    query = request.GET.get('q')
    filter_type = request.GET.get('filter')

    payments = FeePayment.objects.select_related('student').all().order_by('-id')

    if query:
        payments = payments.filter(
            Q(student__first_name__icontains=query) |
            Q(student__last_name__icontains=query)
        )

    total_amount = payments.aggregate(total=Sum('amount'))['total'] or 0

    students = Student.objects.all()

    if filter_type == "pending":
        students = [s for s in students if s.balance() > 0]

    elif filter_type == "paid":
        students = [s for s in students if s.balance() == 0]

    total_pending = sum([s.balance() for s in students])

    form = FeePaymentForm()

    if request.method == 'POST':
        form = FeePaymentForm(request.POST)
        action = request.POST.get('action')

        if form.is_valid():
            payment = form.save()

            full_name = f"{payment.student.first_name} {payment.student.last_name}"

            # -------- PDF --------
            buffer = BytesIO()
            p = canvas.Canvas(buffer)

            p.drawString(200, 800, "CSC TRAINING INSTITUTE")
            p.drawString(100, 750, f"Name: {full_name}")
            p.drawString(100, 730, f"Amount: ₹{payment.amount}")
            p.drawString(100, 710, f"Mode: {payment.payment_mode}")
            p.drawString(100, 690, f"Date: {payment.payment_date}")

            p.save()
            buffer.seek(0)

            # -------- STUDENT EMAIL --------
            if payment.student.email and settings.EMAIL_HOST_USER:
                try:
                    email = EmailMessage(
                        subject="CSC Fee Receipt",
                        body=f"""
Hi {full_name},

Payment of ₹{payment.amount} successful.

Thank you!
""",
                        from_email=settings.EMAIL_HOST_USER,
                        to=[payment.student.email],
                    )
                    email.attach('receipt.pdf', buffer.read(), 'application/pdf')
                    email.send(fail_silently=True)
                except Exception as e:
                    print("Payment Email Error:", e)

            # -------- ADMIN EMAIL --------
            if settings.EMAIL_HOST_USER:
                try:
                    send_mail(
                        subject='💰 New Payment Received',
                        message=f"""
Payment Alert:

Name: {full_name}
Amount: ₹{payment.amount}
Mode: {payment.payment_mode}
""",
                        from_email=settings.EMAIL_HOST_USER,
                        recipient_list=[settings.ADMIN_EMAIL],
                        fail_silently=True
                    )
                except Exception as e:
                    print("Admin Payment Email Error:", e)

            if action == 'pdf':
                return redirect('pdf', payment.id)

            return redirect('fee')

    return render(request, 'admissions/fee.html', {
        'form': form,
        'payments': payments,
        'students': students,
        'total_amount': total_amount,
        'total_pending': total_pending,
        'query': query,
        'filter_type': filter_type
    })


# ===================== PDF =====================
def generate_pdf(request, id):
    payment = get_object_or_404(FeePayment, id=id)

    full_name = f"{payment.student.first_name} {payment.student.last_name}"

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="receipt.pdf"'

    p = canvas.Canvas(response)

    p.drawString(200, 800, "CSC TRAINING")
    p.drawString(100, 750, f"Name: {full_name}")
    p.drawString(100, 730, f"Course: {payment.student.course}")
    p.drawString(100, 710, f"Amount: ₹{payment.amount}")
    p.drawString(100, 690, f"Mode: {payment.payment_mode}")
    p.drawString(100, 670, f"Date: {payment.payment_date}")

    p.save()
    return response


# ===================== STUDENT DETAIL =====================
def student_detail(request, id):
    student = get_object_or_404(Student, id=id)

    payments = student.payments.all()

    return render(request, 'admissions/student_detail.html', {
        'student': student,
        'payments': payments,
        'total_paid': student.total_paid(),
        'balance': student.balance()
    })


# ===================== EXCEL =====================
def export_excel(request):
    payments = FeePayment.objects.select_related('student').all()

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Fee Report"

    ws.append(['Name', 'Course', 'Phone', 'Amount', 'Mode'])

    for p in payments:
        ws.append([
            p.student.first_name,
            p.student.course,
            p.student.phone,
            p.amount,
            p.payment_mode
        ])

    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="report.xlsx"'

    wb.save(response)
    return response