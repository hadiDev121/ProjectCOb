# myApp/views.py
from django.shortcuts import render, redirect, HttpResponse
from .forms import UploadPDFForm
from .models import UploadedPDF
import os
import fitz  # PyMuPDF
from PIL import Image
from django.http import HttpResponse

def upload(request):
    if request.method == 'POST':
        form = UploadPDFForm(request.POST, request.FILES)
        if form.is_valid():
            pdf_instance = form.save()
            return render(request, 'base.html', {'pdf_instance': pdf_instance}) 
    else:
        form = UploadPDFForm()
        return render(request, 'base.html')
    

def convert(request, pdf_id):
    pdf_instance = UploadedPDF.objects.get(pk=pdf_id)
    pdf_path = pdf_instance.pdf_file.path

    if request.method == 'POST':
        output_folder = request.POST.get('output_folder', '')
    else:
        # Default to a folder named 'output_images' in the same directory as the PDF
        output_folder = os.path.join(os.path.dirname(pdf_path), 'output_images')

    # Convert PDF to images using PyMuPDF
    pdf_document = fitz.open(pdf_path)
    images = []

    for page_number in range(pdf_document.page_count):
        page = pdf_document.load_page(page_number)
        pixmap = page.get_pixmap()
        images.append(pixmap)

    # Save each image to the specified output folder
    os.makedirs(output_folder, exist_ok=True)
    
    for i, pixmap in enumerate(images):
        image = Image.frombytes("RGB", [pixmap.width, pixmap.height], pixmap.samples)
        image_path = os.path.join(output_folder, f'page_{i + 1}.jpeg')
        image.save(image_path)

    pdf_document.close()

    return render(request, 'conversion_success.html', {'pdf_instance': pdf_instance, 'output_folder': output_folder})