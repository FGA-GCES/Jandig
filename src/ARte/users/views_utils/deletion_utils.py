def define_content_types(cont_type):
    content_types = {
        'marker': Marker,
        'object': Object,
        'artwork': Artwork,
        'exhibit': Exhibit
    }
    return content_types.get(cont_type)