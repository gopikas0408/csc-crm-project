from django.urls import path
from . import views
from .views import admission_form, fee_management, generate_pdf, export_excel, student_detail

urlpatterns = [
    path('', admission_form, name='admission'),

    #  Fee Management
    path('fee/', fee_management, name='fee'),

    #  PDF
    path('pdf/<int:id>/', generate_pdf, name='pdf'),

    #  Excel
    path('export-excel/', views.export_excel, name='export_excel'),

    #  Student Detail
    path('student/<int:id>/', student_detail, name='student_detail'),
]