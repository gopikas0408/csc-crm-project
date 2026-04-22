
from django.contrib import admin
from .models import Student, FeePayment


# Student Admin
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'email', 'phone', 'course']
    search_fields = ['name', 'email']
    list_filter = ['course']


# Fee Admin
@admin.register(FeePayment)
class FeePaymentAdmin(admin.ModelAdmin):
    list_display = ['id', 'student', 'amount', 'payment_mode', 'payment_date']
    search_fields = ['student__name']
    list_filter = ['payment_mode', 'payment_date']