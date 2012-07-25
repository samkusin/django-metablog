from django.template.defaultfilters import slugify

def slugify_unique(value, model, slugfield="slug"):
    """Creates a unique slug given a 'value' string as the template, appending
    a number if necessary to avoid duplication.
    
    https://code.djangoproject.com/wiki/SlugifyUniquely
    """
    suffix = 0
    potential = base = slugify(value)
    while True:
        if suffix:
            potential = "-".join([base, str(suffix)])
        if not model.objects.filter(**{slugfield: potential}).count():
            return potential
        suffix += 1   