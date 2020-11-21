from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage

from uploaddoc.models import UploadDocModel
from uploaddoc.forms import UploadDocForm


# delete view for details
def delete_view(request, id):
    # dictionary for initial data with
    # field names as keys
    context = {}

    # fetch the object related to passed id
    obj = get_object_or_404(UploadDocModel, uploaddoc_id=id)

    if request.method == "POST":
        # delete object
        obj.delete()
        # after deleting redirect to
        # home page
        return HttpResponseRedirect("/")

    return render(request, "uploaddoc/uploaddoc_delete.html", context)

def list(request):
    documents = UploadDocModel.objects.all().order_by('uploaddoc_fpath')
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
