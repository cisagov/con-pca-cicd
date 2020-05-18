# Bunch of imports for different things I tried. Will clean up later.
import io
from weasyprint import HTML

from django.core.files.storage import FileSystemStorage
from django.views.generic import TemplateView
from django.shortcuts import render
from django.urls import path
from django.conf.urls import url
from django.template.loader import get_template
from django.http import HttpResponse, FileResponse

from . import views


def reports_page(request):
    return render(request, "reports/reports-page.html")


def generate_pdf(request):
    html = HTML("http://localhost:8000/reports")
    html.write_pdf("/tmp/reports_test.pdf")

    fs = FileSystemStorage("/tmp")
    with fs.open("reports_test.pdf") as pdf:
        response = HttpResponse(pdf, content_type="application/pdf")
        response["Content-Disposition"] = 'attachment; filename="reports_test.pdf"'
        return response
    return response
