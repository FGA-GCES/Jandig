from ARte.core.models import Artwork, Exhibit


def save_artwork(form, request, marker, augmented):
    artwork_title = form.cleaned_data['title']
    artwork_desc = form.cleaned_data['description']
    Artwork(
        author=request.user.profile,
        marker=marker,
        augmented=augmented,
        title=artwork_title,
        description=artwork_desc
    ).save()

def save_exhibit(form, request):
    ids = form.cleaned_data['artworks'].split(',')
    artworks = Artwork.objects.filter(id__in=ids)
    exhibit = Exhibit(
                        owner=request.user.profile,
                        name=form.cleaned_data['name'],
                        slug=form.cleaned_data['slug'],
                    )
    exhibit.save()
    exhibit.artworks.set(artworks)


def build_element_data(element_type, element):
    data = None

    if element_type == 'artwork':
        data = {
	        'id_marker' : element.marker.id,
	        'id_object' : element.augmented.id,
            'type': element_type,
            'author': element.author.user.username,
            'owner_id': element.author.user.id,
            'exhibits': element.exhibits_count,
            'created_at': element.created_at.strftime('%d %b, %Y'),
            'marker': element.marker.source.url,
            'augmented': element.augmented.source.url,
            'augmented_size': element.augmented.source.size,
            'title': element.title,
            'description': element.description,
        }
    else:
        data = {
            'id' : element.id,
            'type': element_type,
            'author': element.author,
            'owner': element.owner.user.username,
            'owner_id': element.owner_id,
            'artworks': element.artworks_count,
            'exhibits': element.exhibits_count,
            'source': element.source.url,
            'size': element.source.size,
            'uploaded_at': element.uploaded_at.strftime('%d %b, %Y'),
        }
    
    return data