def build_ctx(profile, user):
    exhibits = profile.exhibits.all()
    markers = profile.marker_set.all()
    objects = profile.object_set.all()
    artworks = profile.artwork_set.all()

    ctx = {
        'exhibits': exhibits,
        'artworks': artworks,
        'markers':markers,
        'objects':objects,
        'profile':True, 
        'button_enable': False if user else True
    }

    return ctx


def save_element(form_type, form_class, source, author):
    instance = form_type(source=source, author=author)
    element = form_class(instance=instance).save(commit=False)
    element.save()
    return element

def build_existent_element(form_type, existent_element, request):
    element = None
    qs = form_type.objects.filter(id=existent_element)
    if qs:
        element = qs[0]
        element.owner = request.user.profile
    return element