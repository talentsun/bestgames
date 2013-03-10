import random, string
from django.contrib.contenttypes.models import ContentType

def get_path(instance, filename):
    ctype = ContentType.objects.get_for_model(instance)
    model = ctype.model
    app = ctype.app_label
    extension = filename.split('.')[-1]
    dir = "site"
    if model == "job":
        dir += "/pdf/job_attachment"
    else:
        dir += "/img/%s" % app
        if model == "image_type_1":
            dir += "/type1/%s" % instance.category
        elif model == "image_type_2":
            dir += "/type2"
        elif model == "restaurant":
            dir += "/logo"
        else:
            dir += "/%s" % model

    chars = string.letters + string.digits
    name = string.join(random.sample(chars, 8), '')

    return "%s/%s.%s" % (dir, name, extension)