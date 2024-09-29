# notes/urls.py

from django.urls import path
from . import views
from .views import upload_note

urlpatterns = [
    path('', views.index, name='index'),  # Home page
    path('mint/', views.mint_note_form, name='mint_note'),  # Mint a new note view
    path('mint-note/', views.mint_note_form, name='mint_note_form'),  # Form for minting a note
    path('noteLedger/<int:token_id>/', views.get_note, name='get_note'),
    # path('upload_note/', views.upload_note, name='upload_note'),
    # path('upload_note/', views.upload_note, name='upload_note'),
    path('upload_note/', upload_note, name='upload_note'),
    path('list_pdfs/', views.list_pdfs, name='list_pdfs'),
    path('pdf/<str:cid>/', views.view_pdf, name='view_pdf'),
    path('view_pdf/', views.view_pdf_list, name='view_pdf_list'),  # Show all PDFs
    path('view_pdf/<int:pdf_id>/', views.view_pdf, name='view_pdf'),
]

