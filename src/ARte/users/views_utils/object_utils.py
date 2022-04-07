def build_model_data(model, type=''):
    model_data = None

    if type=='marker':
        model_data = {
            "source": model.source,
            "uploaded_at": model.uploaded_at,
            "author": model.author,
            "patt": model.patt,
            "title": model.title,
        }
    
    if type=='object':
        model_data = {
            "source": model.source,
            "uploaded_at": model.uploaded_at,
            "author": model.author,
            "scale": model.scale,
            "position": model.position,
            "rotation": model.rotation,
            "title": model.title,
        }

    if type=='artwork':
        model_data = {
            "marker": model.marker,
            "marker_author": model.marker.author,
            "augmented": model.augmented,
            "augmented_author": model.augmented.author,
            "title": model.title,
            "description": model.description,
            "existent_marker": model.marker.id,
            "existent_object": model.augmented.id,
        }
    
    return model_data