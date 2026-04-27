from django.contrib import admin
from .models import Student, FeePayment


# ------------------ STUDENT ADMIN ------------------

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):

    list_display = [
        'id',
        'full_name',
        'email',
        'phone',
        'course',
        'batch',
        'admission_status'
    ]

    search_fields = [
        'first_name',
        'last_name',
        'email',
        'phone'
    ]

    list_filter = [
        'course',
        'batch',
        'admission_status'
    ]

    #  FULL NAME DISPLAY
    def full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"

    full_name.short_description = "Name"


# ------------------ FEE PAYMENT ADMIN ------------------

@admin.register(FeePayment)
class FeePaymentAdmin(admin.ModelAdmin):

    list_display = [
        'id',
        'student',
        'amount',
        'payment_mode',
        'payment_date'
    ]

    search_fields = [
        'student__first_name',
        'student__last_name'
    ]

    list_filter = [
        'payment_mode',
        'payment_date'
    ]