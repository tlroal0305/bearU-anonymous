from django.conf import settings

def img_url_context( request ):
  return { "IMG_URL" : settings.S3_ROOT_URL }