from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse
from django.core.mail import send_mail, EmailMessage
from django.conf import settings
from django.db.models import Sum, Q
from django.db import transaction

from .models import Student, FeePayment
from .forms import StudentForm, FeePaymentForm

from reportlab.pdfgen import canvas
from io import BytesIO
import openpyxl


# ===================== ADMISSION =====================

def admission_form(request):
    form = StudentForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            try:
                with transaction.atomic():
                    student = form.save()

                    full_name = f"{student.first_name} {student.last_name}"
                    messages.success(request, "Admission submitted successfully!")

                    # EMAIL (safe)
                    if settings.EMAIL_HOST_USER:

                        if student.email:
                            send_mail(
                                'CSC Admission Successful',
                                f'Hi {full_name}, your admission is successful.',
                                settings.EMAIL_HOST_USER,
                                [student.email],
                                fail_silently=True   # avoid crash
                            )

                        if settings.ADMIN_EMAIL:
                            send_mail(
                                'New Admission',
                                f'{full_name} registered successfully.',
                                settings.EMAIL_HOST_USER,
                                [settings.ADMIN_EMAIL],
                                fail_silently=True
                            )

                return redirect('fee')

            except Exception as e:
                messages.error(request, f"Error: {str(e)}")

    return render(request, 'admissions/form.html', {'form': form})


# ===================== FEE MANAGEMENT =====================

def fee_management(request):

    query = request.GET.get('q')
    filter_type = request.GET.get('filter')

    payments = FeePayment.objects.select_related('student').order_by('-id')

    if query:
        payments = payments.filter(
            Q(student__first_name__icontains=query) |
            Q(student__last_name__icontains=query)
        )

    total_amount = payments.aggregate(total=Sum('amount'))['total'] or 0

    students = Student.objects.all()

    # FILTER
    if filter_type == "pending":
        students = [s for s in students if s.balance() > 0]
    elif filter_type == "paid":
        students = [s for s in students if s.balance() == 0]

    total_pending = sum(s.balance() for s in students)

    form = FeePaymentForm()

    if request.method == 'POST':
        form = FeePaymentForm(request.POST)
        action = request.POST.get('action')

        if form.is_valid():
            try:
                with transaction.atomic():

                    payment = form.save()
                    student = payment.student
                    full_name = f"{student.first_name} {student.last_name}"

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

                    pdf_file = buffer.getvalue()

                    # -------- EMAIL --------
                    if student.email and settings.EMAIL_HOST_USER:
                        email = EmailMessage(
                            "CSC Fee Receipt",
                            f"Hi {full_name}, payment ₹{payment.amount} successful.",
                            settings.EMAIL_HOST_USER,
                            [student.email],
                        )
                        email.attach('receipt.pdf', pdf_file, 'application/pdf')
                        email.send(fail_silently=True)

                    if settings.ADMIN_EMAIL:
                        send_mail(
                            'New Payment Received',
                            f'{full_name} paid ₹{payment.amount}',
                            settings.EMAIL_HOST_USER,
                            [settings.ADMIN_EMAIL],
                            fail_silently=True
                        )

                if action == 'pdf':
                    return redirect('pdf', payment.id)

                return redirect('fee')

            except Exception as e:
                messages.error(request, f"Payment Error: {str(e)}")

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

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="receipt.pdf"'

    p = canvas.Canvas(response)

    p.drawString(200, 800, "CSC TRAINING")
    p.drawString(100, 750, f"Name: {payment.student}")
    p.drawString(100, 730, f"Amount: ₹{payment.amount}")

    p.save()
    return response


# ===================== STUDENT DETAIL =====================

def student_detail(request, id):
    student = get_object_or_404(Student, id=id)

    return render(request, 'admissions/student_detail.html', {
        'student': student,
        'payments': student.payments.all(),
        'total_paid': student.total_paid(),
        'balance': student.balance()
    })


# ===================== EXPORT EXCEL =====================

def export_excel(request):
    payments = FeePayment.objects.select_related('student')

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Fee Report"

    ws.append(['Name', 'Course', 'Phone', 'Amount', 'Mode'])

    for p in payments:
        ws.append([
            str(p.student),
            p.student.course,
            p.student.phone,
            p.amount,
            p.payment_mode
        ])

    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="report.xlsx"'

    wb.save(response)
    return response