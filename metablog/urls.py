from django.conf.urls.defaults import patterns, url
from cinekine.metablog.feeds import PostFeed, AtomPostFeed

urlpatterns = patterns(
    '',
    # View by permalink
    url(r'^article/(?P<post_slug>[a-zA-Z0-9\^-]+)/$', 'cinekine.metablog.views.article',
        name='metablog_article'),
    # View archived posts by date
    url(r'^archive/(?P<year>[0-9]+)/(?P<month>[0-9]+)/$', 'cinekine.metablog.views.home', {'category_slug': None},
        name='metablog_archive_year_month'),
    # View archived posts by date
    url(r'^archive/(?P<year>[0-9]+)/$', 'cinekine.metablog.views.home', {'category_slug': None, 'month': 0},
        name='metablog_archive_year'),
    # View by Category
    url(r'^category/(?P<category_slug>[a-zA-Z0-9\^-]+)/rss/$', PostFeed(),
        name="rss-category-latest"),
    url(r'^category/(?P<category_slug>[a-zA-Z0-9\^-]+)/atom/$', AtomPostFeed(), name='atom-category-latest'),
    url(r'^category/(?P<category_slug>[a-zA-Z0-9\^-]+)/$', 'cinekine.metablog.views.home', {'year': 0, 'month': 0},
        name='metablog_category'),
    # Default Home page
    url(r'^rss/$', PostFeed(), {'category_slug': None}, name="rss-latest"),
    url(r'^atom/$', AtomPostFeed(), {'category_slug': None}, name='atom-latest'),
    url(r'^$', 'cinekine.metablog.views.home', {'category_slug': None, 'year': 0, 'month': 0},
        name='metablog_home'),
)
