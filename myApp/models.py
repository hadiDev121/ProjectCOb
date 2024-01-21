# myApp/models.py
from django.db import models

class UploadedPDF(models.Model):
    pdf_file = models.FileField()

    def __str__(self):
        return f"{self.pdf_file}"
