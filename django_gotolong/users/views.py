from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import redirect, render
from django.urls import reverse
from django.http import HttpResponseRedirect

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from django.views.generic.list import ListView


class UsersListView(ListView):
    model = User
    queryset = User.objects.all()
    # Why does it go to auth/user_list.html ?


@login_required
def index(request):
    return render(request, 'auth/user_list.html')


def sign_up(request):
    context = {}
    form = UserCreationForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            user = form.save()
            # login(request,user)
            # return render(request, 'auth/user_list.html')
            return HttpResponseRedirect(reverse("user-list"))
    context['form'] = form
    return render(request, 'registration/sign_up.html', context)
