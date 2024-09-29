from django.db import models

class UploadedPDF(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True, default='mynotes')  # Add this line
    cid = models.CharField(max_length=255, unique=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title if self.title else f"PDF {self.id}"
