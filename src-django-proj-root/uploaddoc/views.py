from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage

from uploaddoc.models import UploadDoc
from uploaddoc.forms import UploadDocForm


def list(request):
    documents = UploadDoc.objects.all()
    return render(request, 'uploaddoc/uploaddoc_list.html', {'documents': documents})


def simple_upload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        return render(request, 'uploaddoc/uploaddoc_simple_upload.html', {
            'uploaded_file_url': uploaded_file_url
        })
    return render(request, 'uploaddoc/uploaddoc_simple_upload.html')


def model_form_upload(request):
    if request.method == 'POST':
        form = UploadDocForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('uploaddoc-list')
    else:
        form = UploadDocForm()
    return render(request, 'uploaddoc/uploaddoc_model_form_upload.html', {
        'form': form
    })
