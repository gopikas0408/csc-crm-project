from django.urls import path
from .views import admission_form, fee_management, generate_pdf, export_excel, student_detail

urlpatterns = [
    path('', admission_form, name='admission'),

    # 💰 Fee Management
    path('fee/', fee_management, name='fee'),

    # 📄 PDF
    path('pdf/<int:id>/', generate_pdf, name='pdf'),

    # 📊 Excel
    path('excel/', export_excel, name='excel'),

    # 👤 Student Detail
    path('student/<int:id>/', student_detail, name='student_detail'),
]