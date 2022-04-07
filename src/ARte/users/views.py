from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import update_session_auth_hash, get_user_model
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.decorators import login_required
from django.http import Http404, JsonResponse
from django.views.decorators.cache import cache_page
from django.views.decorators.http import require_http_methods
from ARte.users.views_utils.artwork_utils import build_element_data, save_artwork, save_exhibit, save_upload
from ARte.users.views_utils.object_utils import build_model_data
from ARte.users.views_utils.password_utils import build_global_vars, validate_username_or_email
from ARte.users.views_utils.element_utils import build_ctx, build_existent_element, save_element
from ARte.users.views_utils.signup_utils import perform_save

from core.models import Exhibit, Marker, Object, Artwork
from .models import Profile
from .services.email_service import EmailService
from .services.user_service import UserService
from .forms import (
    SignupForm,
    RecoverPasswordCodeForm,
    RecoverPasswordForm,
    UploadMarkerForm,
    UploadObjectForm,
    ArtworkForm,
    ExhibitForm,
    ProfileForm,
    PasswordChangeForm
)

import json
import logging
log = logging.getLogger('ej')


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)

        if form.is_valid():
            perform_save(request, form)
            return redirect('home')

    else:
        form = SignupForm()

    return render(request, 'users/signup.jinja2', {'form': form})


User = get_user_model()

def recover_password(request):
    if request.method == 'POST':
        recover_password_form = RecoverPasswordForm(request.POST)

        if recover_password_form.is_valid():
            user_service = UserService()
            username_or_email_is_valid, username_or_email = validate_username_or_email(recover_password_form, user_service)

            if (not username_or_email_is_valid):
                return redirect('invalid_recovering_email_or_username')

            global global_recovering_email
            global global_verification_code
            global_recovering_email, global_verification_code = build_global_vars(user_service, username_or_email)

        return redirect('recover-code')

    recover_password_form = RecoverPasswordForm()
    return render(request, 'users/recover-password.jinja2', {'form': recover_password_form})


def build_message_and_send_to_user(email):
    message = f'You have requested a new password. This is your verification code: {global_verification_code}\nCopy it and put into the field.'
    email_service = EmailService(message)
    multipart_message = email_service.build_multipart_message(email)
    email_service.send_email_to_recover_password(multipart_message)


def recover_code(request):
    if request.method == 'POST':
        form = RecoverPasswordCodeForm(request.POST)

        if form.is_valid():
            code = form.cleaned_data.get('verification_code')

            log.warning('Inserido: %s', code)
            log.warning('Correto: %s', global_verification_code)

            if(code == global_verification_code):
                global recover_password_user
                recover_password_user = User.objects.get(email=global_recovering_email)
                return redirect('recover-edit-password')

            return redirect('wrong-verification-code')
        return redirect('home')
    
    form = RecoverPasswordCodeForm()
    return render(request, 'users/recover-password-code.jinja2', {'form': form})

def recover_edit_password(request):
    if request.method == 'POST':
        form = SetPasswordForm(recover_password_user, data=request.POST)

        if form.is_valid():
            form.save()
            return redirect('login')

    else:
        form = SetPasswordForm(recover_password_user)

    return render(request, 'users/recover-edit-password.jinja2', {'form': form})

@require_http_methods(["GET"])
def wrong_verification_code(request):
    return render(request, 'users/wrong-verification-code.jinja2')

@require_http_methods(["GET"])
def invalid_recovering_email_or_username(request):
    return render(request, 'users/invalid-recovering-email.jinja2')


@login_required
@require_http_methods(["GET"])
def profile(request):
    user = request.GET.get('user')
    
    if user:
        profile = Profile.objects.get(user=user)
    else:
        profile = Profile.objects.select_related().get(user=request.user)

    ctx = build_ctx(profile, user)

    return render(request, 'users/profile.jinja2', ctx)

@cache_page(60 * 60)
def get_element(request, form, form_class, form_type, source, author, existent_element):
    element = None
    log.warning(form)

    if(source and author):
        element = save_element(form_type, form_class, source, author)
    elif(existent_element):
        element = build_existent_element(form_type, existent_element, request)

    return element

@cache_page(60 * 60)
def get_marker(request, form):
    marker_src = form.cleaned_data['marker']
    marker_author = form.cleaned_data['marker_author']
    existent_marker = form.cleaned_data['existent_marker']

    return get_element(request, form, UploadMarkerForm, Marker, source=marker_src, author=marker_author, existent_element=existent_marker)

@cache_page(60 * 60)
def get_augmented(request, form):
    object_src = form.cleaned_data['augmented']
    object_author = form.cleaned_data['augmented_author']
    existent_object = form.cleaned_data['existent_object']

    return get_element(request, form, UploadObjectForm, Object, source=object_src, author=object_author, existent_element=existent_object)

@login_required
def create_artwork(request):
    if request.method == 'POST':
        form = ArtworkForm(request.POST, request.FILES)

        if form.is_valid():

            marker = get_marker(request,form)
            augmented = get_augmented(request, form)

            if marker and augmented:
                save_artwork(form, request, marker, augmented)
            
            return redirect('home')
    else:
        form = ArtworkForm()

    marker_list = Marker.objects.all()
    object_list = Object.objects.all()

    return render(
        request,
        'users/artwork-create.jinja2',
        {
            'form': form,
            'marker_list': marker_list,
            'object_list': object_list,
        }
    )

@login_required
def create_exhibit(request):
    if request.method == 'POST':
        form = ExhibitForm(request.POST)
        if form.is_valid():
            save_exhibit(form, request)
            return redirect('home')

    else:
        form = ExhibitForm()

    artworks = Artwork.objects.all()

    return render(
        request,
        'users/exhibit-create.jinja2',
        {
            'form': form,
            'artworks': artworks,
        }
    )

@require_http_methods(["GET"])
def download_exhibit(request):
    exhibit_id = request.GET.get('id')
    exhibit = Exhibit.objects.get(id=exhibit_id)
    artworks = list(exhibit.artworks.all())

    marker_names = []
    object_names = []
    patt_names = []

    all_data = []

    for artwork in artworks:
        marker_names.append(artwork.marker.source.name)
        object_names.append(artwork.augmented.source.name)
        patt_names.append(str(artwork.marker.patt))

    for marker_name in marker_names:
        data = {
            "link": marker_name
        }

        all_data.append(data)

    for object_name in object_names:
        data = {
            "link": object_name
        }

        all_data.append(data)

    for patt_name in patt_names:
        data = {
            "link": patt_name
        }

        all_data.append(data)

    return JsonResponse(all_data)


@cache_page(60 * 2)
@require_http_methods(["GET"])
def element_get(request):
    if request.GET.get('marker_id', None):
        element_type = 'marker'
    elif request.GET.get('object_id', None):
        element_type = 'object'
    elif request.GET.get('artwork_id', None):
        element_type = 'artwork'

    element_type_id = element_type + '_id'
    element = get_object_or_404(Artwork, pk=request.GET[element_type_id])

    data = build_element_data(element_type, element)
    serialized = json.dumps(data)

    return JsonResponse(serialized)

def upload_elements(request, form_class, form_type, route):
    if request.method == 'POST':
        form = form_class(request.POST, request.FILES)
        if form.is_valid():
            save_upload(form, request)
            return redirect('home')
    else:
        form = form_class()

    return render(request,'users/upload.jinja2',
        {
            'form_type': form_type,
            'form': form,
            'route': route,
            'edit': False
        }
    )

@login_required
def marker_upload(request):
    return upload_elements(request, UploadMarkerForm, 'marker', 'marker-upload')

@login_required
def object_upload(request):
    return upload_elements(request, UploadObjectForm, 'object', 'object-upload')

def edit_elements(request, form_class, route, model, model_data):
    user = Profile.objects.get(user=request.user)
    if(not model or model.owner != user):
        raise Http404

    if(request.method == "POST"):
        form = form_class(request.POST, request.FILES, instance = model)
        form.full_clean()

        if form.is_valid():
            form.save()
            return redirect('profile')
        
        log.warning(form.errors)

    return render(
        request, route,
        {
            'form': form_class(initial=model_data),
            'model': model,
        }
    )

@login_required
def edit_object(request):
    index = request.GET.get("id", "-1")
    model = Object.objects.get(id=index)
    model_data = build_model_data(model, type='object')

    return edit_elements(request, UploadObjectForm, route='users/edit-object.jinja2', model=model, model_data=model_data)

@login_required
def edit_marker(request):
    index = request.GET.get("id", "-1")
    model = Marker.objects.get(id=index)
    model_data = build_model_data(model, type='marker')

    return edit_elements(request, UploadMarkerForm, route='users/edit-marker.jinja2', model=model, model_data=model_data)


@login_required
def edit_artwork(request):
    index = request.GET.get("id","-1")
    model = Artwork.objects.filter(id=index)
    if(not model or model.first().author != Profile.objects.get(user=request.user)):
        raise Http404

    if(request.method == "POST"):
        form = ArtworkForm(request.POST, request.FILES)

        form.full_clean()
        if form.is_valid():
            model_data={
                "marker": get_marker(request,form),
                "augmented": get_augmented(request, form),
                "title": form.cleaned_data["title"],
                "description": form.cleaned_data["description"],
            }

            log.warning(model_data['augmented'])
            model.update(**model_data)
            return redirect('profile')

    model = model.first()
    model_data = build_model_data(model, type='artwork')

    return render(
        request,
        'users/artwork-edit.jinja2',
        {
            'form': ArtworkForm(initial=model_data),
            'marker_list': Marker.objects.all(),
            'object_list': Object.objects.all(),
            'selected_marker': model.marker.id,
            'selected_object': model.augmented.id
        }
    )


@login_required
def edit_exhibit(request):
    index = request.GET.get("id","-1")
    model = Exhibit.objects.filter(id=index)
    user = Profile.objects.get(user=request.user)
    if(not model or model.first().owner != user):
        raise Http404

    if(request.method == "POST"):
        form = ExhibitForm(request.POST)

        form.full_clean()
        if form.is_valid():
            ids = form.cleaned_data['artworks'].split(',')
            artworks = Artwork.objects.filter(id__in=ids)

            model_data={
                "name":form.cleaned_data["name"],
                "slug": form.cleaned_data["slug"],
            }
            model.update(**model_data)
            model = model.first()
            model.artworks.set(artworks)

            return redirect('profile')

    model = model.first()
    model_artworks = ""
    for artwork in model.artworks.all():
        model_artworks += str(artwork.id) + ","

    model_artworks = model_artworks[:-1]

    model_data = {
        "name": model.name,
        "slug": model.slug,
        "artworks": model_artworks
    }

    artworks = Artwork.objects.filter(author=request.user.profile)
    return render(
        request,
        'users/exhibit-edit.jinja2',
        {
            'form': ExhibitForm(initial=model_data),
            'artworks': artworks,
            'selected_artworks': model_artworks,
        }
    )

@login_required
def edit_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('profile')

        profile = Profile.objects.get(user=request.user)
        ctx={
            'form_password': PasswordChangeForm(request.user),
            'form_profile': ProfileForm(instance=profile)
        }
        return render(request,'users/profile-edit.jinja2',ctx)
    return Http404

@login_required
def edit_profile(request):
    profile = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)

        if form.is_valid():
            profile = form.save(commit=False)
            user = profile.user
            user.email = form.cleaned_data['email']
            user.username = form.cleaned_data['username']
            user.save(force_update=True)
            profile.save()

            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)

    return render(
        request,
        'users/profile-edit.jinja2',
        {
            'form_profile': form,
            'form_password': PasswordChangeForm(request.user),
        }
    )

@login_required
@require_http_methods(["GET"])
def delete(request):
    content_type = request.GET.get('content_type', None)
   
    if content_type == 'marker':
        delete_content(Marker, request.user, request.GET.get('id', -1))
    elif content_type == 'object':
        delete_content(Object, request.user, request.GET.get('id', -1))
    elif content_type == 'artwork':
        delete_content(Artwork, request.user, request.GET.get('id', -1))
    elif content_type == 'exhibit':
        delete_content(Exhibit, request.user, request.GET.get('id', -1))
    return redirect('profile')

def delete_content(model, user, instance_id):
    qs = model.objects.filter(id=instance_id)
   
    if qs:
        instance = qs[0] 
        if user.has_perm('users.moderator'):
            delete_content_Moderator(instance,user)
        else:
            isArtwork = isinstance(instance, Artwork)
            if isArtwork:
                hasPermission = (instance.author == user.profile)
            else:
                hasPermission = (instance.owner == user.profile)
        
            isInstanceSameTypeofModel = isinstance(instance, model)
            if isInstanceSameTypeofModel and hasPermission:
                instance.delete()
        

def delete_content_Moderator(instance,user):
    isInstanceSameTypeofModel = isinstance(instance, model)
    isObject = isinstance(instance, Object)
    isMarker = isinstance(instance, Marker)
    isArtwork = isinstance(instance, Artwork)


    if isInstanceSameTypeofModel or not instance.in_use:
        instance.delete()
    elif instance.in_use:
        if isObject:
            artworkIn = Artwork.objects.filter(augmented=instance)
            artworkIn.delete()
            instance.delete()
        elif isMarker:
            artworkIn = Artwork.objects.filter(marker=instance)
            artworkIn.delete()
            instance.delete()
        elif isArtwork:
            instance.delete()

@require_http_methods(["GET"])
def related_content(request):
    element_id = request.GET.get('id')
    element_type = request.GET.get('type')
    element = None
    ctx = {}

    if element_type == 'object':
        element = Object.objects.get(id=element_id)

        artworks = element.artworks_list
        exhibits = element.exhibits_list

        ctx = {'artworks': artworks, 'exhibits': exhibits, "seeall:":False}
    elif element_type == 'marker':
        element = Marker.objects.get(id=element_id)

        artworks = element.artworks_list
        exhibits = element.exhibits_list

        ctx = {'artworks': artworks, 'exhibits': exhibits, "seeall:":False}
    elif element_type == 'artwork':
        element = Artwork.objects.get(id=element_id)

        exhibits = element.exhibits_list

        ctx = {'exhibits': exhibits, "seeall:":False}

    return render(request, 'core/collection.jinja2', ctx)

@login_required
@require_http_methods(["GET"])
def mod_delete(request):
    content_type = request.GET.get('content_type', None)
    if content_type == 'marker':
        delete_content(Marker, request.user, request.GET.get('instance_id', -1))
    elif content_type == 'object':
        delete_content(Object, request.user, request.GET.get('instance_id', -1))
    elif content_type == 'artwork':
        delete_content(Artwork, request.user, request.GET.get('instance_id', -1))
    elif content_type == 'exhibit':
        delete_content(Exhibit, request.user, request.GET.get('id', -1))
    return redirect('moderator-page')


def mod(request):
    ctx = {
        "objects" : Object.objects.all(),
        "markers" : Marker.objects.all(),
        "artworks": Artwork.objects.all(),
        "exhibits": Exhibit.objects.all(),
        "permission" : request.user.has_perm('users.moderator'),
    }
    return render(request, 'users/moderator-page.jinja2', ctx)

def permission_denied (request):
    return render(request, 'users/permission-denied.jinja2')