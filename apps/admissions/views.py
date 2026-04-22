from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse

from django.core.mail import send_mail, EmailMessage

from django.db.models import Sum, Q
from .models import Student, FeePayment
from .forms import StudentForm, FeePaymentForm

from reportlab.pdfgen import canvas
import openpyxl
from io import BytesIO


# ------------------ ADMISSION ------------------
def admission_form(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)

        if form.is_valid():
            student = form.save()

            # ✅ SUCCESS MESSAGE
            messages.success(request, "Admission submitted successfully 🎉")

            # 📧 STUDENT EMAIL
            try:
                send_mail(
                    '🎓 Admission Confirmation',
                    f"""
Hi {student.name},

🎉 Your admission is successfully completed.

Course: {student.course}
Phone: {student.phone}

Thank you 💙
""",
                    'gopikas04082005@gmail.com',
                    [student.email],
                    fail_silently=False,
                )
            except Exception as e:
                print("EMAIL ERROR:", e)

            # 📧 ADMIN EMAIL
            try:
                send_mail(
                    '🚨 New Admission Alert',
                    f"""
New Admission Received!

Name: {student.name}
Email: {student.email}
Phone: {student.phone}
Course: {student.course}
""",
                    'gopikas04082005@gmail.com',
                    ['gopikas04082005@gmail.com'],
                    fail_silently=False,
                )
            except Exception as e:
                print("ADMIN EMAIL ERROR:", e)

            # ✅ REDIRECT
            return redirect('/fee/')

        else:
            # 🔥 FIXED LINE (IMPORTANT)
            messages.error(request, "Please correct the errors below.")

    else:
        form = StudentForm()

    return render(request, 'admissions/form.html', {'form': form})


# ------------------ FEE MANAGEMENT ------------------
def fee_management(request):
    query = request.GET.get('q')

    payments = FeePayment.objects.all().order_by('-id')

    if query:
        payments = payments.filter(Q(student__name__icontains=query))

    # 💰 TOTAL
    total_amount = payments.aggregate(total=Sum('amount'))['total'] or 0

    # 🔴 PENDING
    students = Student.objects.all()
    total_pending = 0

    for s in students:
        paid = s.payments.aggregate(total=Sum('amount'))['total'] or 0
        total_pending += (s.total_fee - paid)

    form = FeePaymentForm()

    if request.method == 'POST':
        form = FeePaymentForm(request.POST)
        action = request.POST.get('action')

        if form.is_valid():
            payment = form.save()

            # 🔥 PDF CREATE
            buffer = BytesIO()
            p = canvas.Canvas(buffer)

            p.drawString(200, 800, "CSC TRAINING INSTITUTE")
            p.drawString(100, 750, f"Name: {payment.student.name}")
            p.drawString(100, 730, f"Amount: ₹{payment.amount}")
            p.drawString(100, 710, f"Mode: {payment.payment_mode}")
            p.drawString(100, 690, f"Date: {payment.payment_date}")

            p.save()
            buffer.seek(0)

            # 📧 EMAIL WITH PDF
            try:
                email = EmailMessage(
                    subject="Fee Receipt",
                    body=f"Hi {payment.student.name}, your payment is successful.",
                    from_email='gopikas04082005@gmail.com',
                    to=[payment.student.email],
                )

                email.attach('receipt.pdf', buffer.read(), 'application/pdf')
                email.send()
            except Exception as e:
                print("FEE EMAIL ERROR:", e)

            # 🔥 BUTTON LOGIC
            if action == 'pdf':
                return redirect(f'/pdf/{payment.id}/')

            return redirect('/fee/')

        else:
            print("FEE FORM ERROR:", form.errors)

    return render(request, 'admissions/fee.html', {
        'form': form,
        'payments': payments,
        'total_amount': total_amount,
        'total_pending': total_pending,
        'query': query
    })


# ------------------ PDF DOWNLOAD ------------------
def generate_pdf(request, id):
    payment = get_object_or_404(FeePayment, id=id)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="receipt.pdf"'

    p = canvas.Canvas(response)

    p.drawString(200, 800, "CSC TRAINING")
    p.drawString(100, 750, f"Name: {payment.student.name}")
    p.drawString(100, 730, f"Course: {payment.student.course}")
    p.drawString(100, 710, f"Amount: ₹{payment.amount}")
    p.drawString(100, 690, f"Mode: {payment.payment_mode}")
    p.drawString(100, 670, f"Date: {payment.payment_date}")

    p.save()
    return response


# ------------------ EXCEL EXPORT ------------------
def export_excel(request):
    wb = openpyxl.Workbook()
    ws = wb.active

    ws.append(['Name', 'Course', 'Amount', 'Mode', 'Date'])

    payments = FeePayment.objects.all()

    for p in payments:
        ws.append([
            p.student.name,
            p.student.course,
            p.amount,
            p.payment_mode,
            str(p.payment_date)
        ])

    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="fees.xlsx"'
    wb.save(response)

    return response


# ------------------ STUDENT DETAIL ------------------
def student_detail(request, id):
    student = get_object_or_404(Student, id=id)

    payments = student.payments.all()

    total_paid = payments.aggregate(total=Sum('amount'))['total'] or 0
    balance = student.total_fee - total_paid

    return render(request, 'admissions/student_detail.html', {
        'student': student,
        'payments': payments,
        'total_paid': total_paid,
        'balance': balance
    })