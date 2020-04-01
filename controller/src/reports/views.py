# Bunch of imports for different things I tried. Will clean up later.
import io
from django.shortcuts import render
from django.urls import path
from django.conf.urls import url
from django.template.loader import get_template
from django.http import HttpResponseRedirect, FileResponse
from . import views
from weasyprint import HTML, css
from django_weasyprint import WeasyTemplateResponseMixin

# Create your views here.
def reports_page(request):
  return render(request, 'reports-page.html')

# Function will create two PDF's. One in the downloads folder from the buffer that is empty.
# A second report (the "real" report will appear under the 'src' folder. Will fix later.)
def generate_pdf(request):
  buffer = io.BytesIO()
  buffer.seek(0)
  HTML('http://localhost:8000/reports').write_pdf('./reports_test.pdf')
  return FileResponse(buffer, as_attachment=True, filename='reports_test.pdf')
