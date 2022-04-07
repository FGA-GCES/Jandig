from django.contrib.auth import login, authenticate

def perform_save(request, form):
    form.save()
    username = form.cleaned_data.get('username')
    raw_password = form.cleaned_data.get('password1')
    user = authenticate(username=username, password=raw_password)
    login(request, user)