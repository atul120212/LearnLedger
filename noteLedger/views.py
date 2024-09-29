# notes/views.py

from django.http import JsonResponse

from .models import UploadedPDF
from .smart_contract import get_note_details, mint_note

def get_note(request, token_id):
    note = get_note_details(token_id)
    return JsonResponse(note)

def mint_note_view(request):
    if request.method == 'POST':
        uri = request.POST['uri']
        royalty = int(request.POST['royalty'])
        sender_address = request.POST['sender_address']
        private_key = request.POST['private_key']
        tx_hash = mint_note(sender_address, private_key, uri, royalty)
        return JsonResponse({'transaction_hash': tx_hash})



from django.shortcuts import get_object_or_404, render

def index(request):
    return render(request, 'index.html')

def mint_note_form(request):
    return render(request, 'mint_note.html')

# notes/views.py

from django.http import JsonResponse, HttpResponse
from .smart_contract import mint_note

def mint_note_view(request):
    if request.method == 'POST':
        uri = request.POST.get('uri')
        royalty = request.POST.get('royalty')
        sender_address = request.POST.get('sender_address')
        private_key = request.POST.get('private_key')

        # Validate input
        if not uri or not royalty or not sender_address or not private_key:
            return JsonResponse({'error': 'All fields are required.'}, status=400)

        try:
            royalty = int(royalty)
        except ValueError:
            return JsonResponse({'error': 'Invalid royalty value.'}, status=400)

        try:
            tx_hash = mint_note(sender_address, private_key, uri, royalty)
            return JsonResponse({'transaction_hash': tx_hash})
        except Exception as e:
            # Handle errors related to the smart contract interaction
            return JsonResponse({'error': str(e)}, status=500)
    
    # If the request method is not POST, return an error response
    return JsonResponse({'error': 'Invalid request method. Use POST.'}, status=405)



from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .pinata_utils import upload_to_pinata
from .models import UploadedPDF  # Import your model
import os

@csrf_exempt
def upload_note(request):
    if request.method == 'POST' and request.FILES.get('file'):
        file = request.FILES['file']

        # Save file temporarily
        file_path = os.path.join('uploads', file.name)
        if not os.path.exists('uploads'):
            os.makedirs('uploads')
            
        with open(file_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        # Upload to Pinata
        try:
            cid = upload_to_pinata(file_path)
            
            # Save the CID and file name in the database
            UploadedPDF.objects.create(cid=cid)

        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)})
        finally:
            os.remove(file_path)

        return JsonResponse({"success": True, "cid": cid})

    return JsonResponse({"success": False, "message": "Invalid request method or missing file"})

def list_pdfs(request):
    pdfs = UploadedPDF.objects.all()  # Fetch all records from the database
    return render(request, 'list_pdfs.html', {'pdfs': pdfs})

def view_pdf_list(request):
    pdfs = UploadedPDF.objects.all()  # Retrieve all PDFs from the database
    return render(request, 'view_pdf_list.html', {'pdfs': pdfs})  # Render a template with all PDFs

def view_pdf(request, pdf_id):
    pdf = get_object_or_404(UploadedPDF, id=pdf_id)
    pdf_url = f'https://gateway.pinata.cloud/ipfs/{pdf.cid}'  # Construct the IPFS URL using the CID
    return render(request, 'view_pdf.html', {'pdf_url': pdf_url, 'title': pdf.title})  # Render the PDF view template