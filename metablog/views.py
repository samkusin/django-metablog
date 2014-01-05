################################################################################
#   Views of metablog
#
################################################################################

from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import Http404
from django.conf import settings
from django.core.urlresolvers import reverse

from models import Post, Category, Link, Tag

from datetime import datetime
from datetime import date
from time import mktime

import json


class JsonDatetimeEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, datetime):
            return int(mktime(obj.timetuple()))

        return json.JSONEncoder.default(self, obj)


def create_post_archive(posts):
    """
    Order posts by post date from latest to earliest, returning
    the posts in hierachicial JSON form:
    {
        archives: [
            {
                key: "<year>"
                uri: "<year>/",
                count: <post count>,
                archives: [
                    {
                        key: "<month>",
                        uri: "<year>/<month>"
                        count: <post count>,
                        >
                        articles: [
                            {
                                title: "<title>",
                                uri: "<year>/",
                                date: <datetime>
                                id: <post id, guaranteed to the unique per article>
                            },
                            ...
                        ],
                    },
                    ...
                ],
            },
            ...
        ]
    }
    """
    posts = posts.all().values('id', 'title', 'slug', 'post_date', 'status')

    archive_stack = []
    archive_stack.append([])        # archive list (top-level contains years)

    year = -1
    year_count = 0
    month = -1
    month_count = 0

    for post in posts:
        post_date = post['post_date']

        if year != post_date.year:
            if year != -1:
                # fixup stack - top = articles,
                # fixup stack - top-1 = months
                articles = archive_stack.pop()
                months = archive_stack.pop()
                months[-1]['articles'] = articles
                months[-1]['count'] = month_count
                year_count += month_count
                month_count = 0
                archive_stack[-1][-1]['archives'] = months
                archive_stack[-1][-1]['count'] = year_count
                year_count = 0

            year = post_date.year
            archive = {
                'key': str(year),
                'uri': reverse('metablog_archive_year', kwargs={'year': year}),
                'count': 0,
            }
            archive_stack[-1].append(archive)  # append year to years array (stack top)

            month = -1
            archive_stack.append([])    # append new months array to stack top.

        if month != post_date.month:
            if month != -1:
                # fixup stack - top = articles
                articles = archive_stack.pop()
                archive_stack[-1][-1]['articles'] = articles
                archive_stack[-1][-1]['count'] = month_count
                year_count += month_count
                month_count = 0

            month = post_date.month
            archive = {
                'key': post_date.strftime("%B"),
                'uri': reverse('metablog_archive_year_month', kwargs={'year': year, 'month': month}),
                'count': 0,
            }
            archive_stack[-1].append(archive)  # append month to months array (stack top)

            archive_stack.append([])    # append new articles array to stack top.

        # add article link
        article = {
            'title': post['title'],
            'uri': reverse('metablog_article', kwargs={'post_slug': post['slug']}),
            'date': post_date,
            'id': post['id']
        }
        archive_stack[-1].append(article)
        month_count += 1

    # final fixup.
    if len(archive_stack) == 3:
        # fixup stack - top = articles,
        # fixup stack - top-1 = months
        articles = archive_stack.pop()
        months = archive_stack.pop()
        months[-1]['articles'] = articles
        months[-1]['count'] = month_count
        year_count += month_count
        archive_stack[-1][-1]['archives'] = months
        archive_stack[-1][-1]['count'] = year_count
    else:
        return None

    return {
        'archives': archive_stack.pop()
    }


def common(is_admin):
    categories = Category.objects.all()

    statuses_to_display = [Post.PUBLISHED, Post.EXCLUSIVE, Post.CLOSED]
    if is_admin:
        statuses_to_display.append(Post.DRAFT)
        statuses_to_display.append(Post.HIDDEN)

    archives = create_post_archive(Post.query(statuses=statuses_to_display))
    blogroll = None
    try:
        favorites_tag = Tag.objects.get(slug='favorite-blog')
    except:
        favorites_tag = None

    if favorites_tag:
        blogroll = Link.objects.filter(tag__exact=favorites_tag).order_by('rank')

    return categories, statuses_to_display, archives, blogroll


def cull_posts(all_posts, article_post_index, post_page_count):
    post_count = all_posts.count()

    if post_count > 0:
        if article_post_index < 0:
            article_post_index = 0
        elif article_post_index >= post_count:
            article_post_index = post_count - 1
        article_post_index_end = min(article_post_index + post_page_count, post_count)

        posts = all_posts[article_post_index:article_post_index_end]

        # determine whether we need links to prior or next page posts
        next_post_index = -1
        if article_post_index > 0:
            next_post_index = max(article_post_index - post_page_count, 0)

        prev_post_index = -1
        if article_post_index + post_page_count < post_count:
            prev_post_index = min(article_post_index + post_page_count, post_count - 1)

    else:
        next_post_index = -1
        prev_post_index = -1
        posts = None

    first_post_id = None
    if posts and len(posts) > 0:
        first_post_id = posts[0].id

    return posts, first_post_id, next_post_index, prev_post_index


###############################################################################

def home(request, category_slug):
    """
        Homepage

        @param request Incoming HTTP request
        @param category_slug (optional) Incoming category_slug (used in the request URL.)
    """
    # find category if passed into the request
    categories, statuses_to_display, archives, blogroll = common(request.user.is_authenticated())

    article_post_index = 0
    if 'start' in request.GET:
        article_post_index = int(request.GET['start'])

    search_tags = []
    selected_category = None

    if category_slug:
        print category_slug
        for category in categories:
            if category.tag.slug == category_slug:
                search_tags.append(category.tag)
                selected_category = category

        # check if this is a tag
        if selected_category is None:
            try:
                search_tag = Tag.objects.get(slug=category_slug)
                search_tags.append(search_tag)
            except:
                print "No tag found for given slug '" + category_slug

    all_posts = Post.query(statuses_to_display,
                           search_tags
                           )

    # cap post start and end ranges based on available posts
    posts, first_post_id, next_post_index, prev_post_index = cull_posts(
                    all_posts,
                    article_post_index,
                    settings.CK_METABLOG_PER_PAGE_COUNT)

    context = {
        'page_title': settings.CK_SITE_TITLE,
        'categories': categories,
        'selected_category': selected_category,
        'blog_posts': posts,
        'archives': archives,
        'blogroll': blogroll,
        'first_post_id': first_post_id,
        'next_post_index': next_post_index,
        'prev_post_index': prev_post_index,
        'allow_rss_feed': True,
    }

    # render
    return render_to_response("home.html",
                              context,
                              context_instance=RequestContext(request))


def archive(request, year, month):
    """
        Homepage

        @param request Incoming HTTP request
        @param category_slug (optional) Incoming category_slug (used in the request URL.)
    """
    # find category if passed into the request
    categories, statuses_to_display, archives, blogroll = common(request.user.is_authenticated())

    article_post_index = 0
    if 'start' in request.GET:
        article_post_index = int(request.GET['start'])

    search_tags = []
    selected_category = None

    all_posts = Post.query(statuses_to_display,
                           search_tags,
                           year, month
                           )

    # cap post start and end ranges based on available posts
    posts, first_post_id, next_post_index, prev_post_index = cull_posts(all_posts,
                    article_post_index,
                    settings.CK_METABLOG_PER_PAGE_COUNT)

    archive_month = False
    if not month:
        archive_date = date(int(year), 1, 1)
    else:
        archive_date = date(int(year), int(month), 1)
        archive_month = True

    context = {
        'page_title': settings.CK_SITE_TITLE,
        'categories': categories,
        'selected_category': selected_category,
        'archive_date': archive_date,
        'archive_month': archive_month,
        'blog_posts': posts,
        'archives': archives,
        'blogroll': blogroll,
        'first_post_id': first_post_id,
        'next_post_index': next_post_index,
        'prev_post_index': prev_post_index,
    }

    # render
    return render_to_response("home.html",
                              context,
                              context_instance=RequestContext(request))


def except_404_view(request):
    """
    Standard 404 View
    """
    categories, statuses_to_display, archives, blogroll = common(request.user.is_authenticated)

    context = {
        'page_title': settings.CK_SITE_TITLE,
        'categories': categories,
        'selected_category': None,
        'archives': archives,
        'blogroll': blogroll,
    }

    # render
    return render_to_response("404.html", context, context_instance=RequestContext(request))


def article(request, post_slug):
    """
        Retrieves a single post (a single post view page)
        @param request Incoming HTTP request
        @param category_slug (optional) Incoming category_slug (used in the request URL.)
    """
    if not post_slug:
        raise Http404

    post = get_object_or_404(Post, slug=post_slug)

    categories, statuses_to_display, archives, blogroll = common(request.user.is_authenticated)
    if post.status not in statuses_to_display:
        raise Http404

    first_post_id = None
    if post:
        first_post_id = post.id

    # render
    return render_to_response("post.html",
                                {
                                    'page_title': settings.CK_SITE_TITLE,
                                    'categories': categories,
                                    'selected_category': None,
                                    'blog_post': post,
                                    'archives': archives,
                                    'blogroll': blogroll,
                                    'first_post_id': first_post_id
                                },
                                context_instance=RequestContext(request))
