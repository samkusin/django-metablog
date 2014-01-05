################################################################################
# Custom context processors.
# These are referenced from the setting TEMPLATE_CONTEXT_PROCESSORS and used by
# RequestContext.
################################################################################"""

from django.conf import settings
from django.contrib.sites.models import Site

def config(request):
    """
    Exposes certain configuration settings inside a template.
    """
    context_extras = {}
    if settings.CK_LOCAL_JS_LIBRARIES:
        context_extras['ck_local_js_libraries'] = True
    if settings.CK_SITE_TITLE:
        context_extras['ck_site_title'] = settings.CK_SITE_TITLE
    return context_extras

def site(request):
    if hasattr(settings, 'CK_SITE_DOMAIN'):
	   return {'ck_site_domain': settings.CK_SITE_DOMAIN}

    domain = "http://%s" % Site.objects.get_current().domain
    return {'ck_site_domain': domain}
