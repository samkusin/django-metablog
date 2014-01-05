"""@package docstring
Django Model for the Metablog Application.

Association between tags and posts.
"""

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.sitemaps import ping_google
from django.conf import settings

from wysihtml5.fields import Wysihtml5TextField


class Tag(models.Model):
    """Tags are used for searching and organizing blog posts.
    """
    name = models.CharField(max_length=24)
    slug = models.SlugField(max_length=24)

    def __unicode__(self):
        return self.name

    # Django Overrides
    @models.permalink
    def get_absolute_url(self):
        return ('metablog_category', [self.slug])


################################################################################

class Post(models.Model):
    """A single blog post.
    """
    DRAFT = 0
    HIDDEN = 1
    PUBLISHED = 2
    CLOSED = 4
    EXCLUSIVE = 5
    STATUS_CHOICES = (
        (DRAFT, 'Draft'),
        (HIDDEN, 'Hidden'),
        (PUBLISHED, 'Published'),
        (CLOSED, 'Closed'),
        (EXCLUSIVE, 'Exclusive')
    )
    author = models.ForeignKey(User)
    title = models.CharField(max_length=128)
    slug = models.SlugField()
    create_date = models.DateTimeField(auto_now_add=True, null=True)
    post_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    status = models.SmallIntegerField(choices=STATUS_CHOICES, db_index=True)
    prev_post = models.OneToOneField('self', related_name='next', null=True, blank=True)
    next_post = models.OneToOneField('self', related_name='prev', null=True, blank=True)
    tags = models.ManyToManyField(Tag)
    text = Wysihtml5TextField()
    atj_word_count = models.SmallIntegerField(verbose_name='After the Jump word count', default=150)
    description = models.CharField(max_length=150, default="")

    NORMAL = 1
    PREFERRED = 2
    HIGHLIGHTED = 3
    PRIORITY_CHOICES = (
        (NORMAL, 'Normal'),
        (PREFERRED, 'Preferred'),
        (HIGHLIGHTED, 'Highlighted'),
    )
    search_priority = models.SmallIntegerField(choices=PRIORITY_CHOICES, default=NORMAL)
    pings = models.SmallIntegerField(editable=False, default=0)

    _original_status = None

    def __init__(self, *args, **kwargs):
        super(Post, self).__init__(*args, **kwargs)
        self._original_status = self.status

    def __unicode__(self):
        return self.title

    # Django overrides
    @models.permalink
    def get_absolute_url(self):
        return ('metablog_article', [self.slug])

    def save(self, *args, **kwargs):
        if self._original_status != self.status:
            # need to update post time if we've officially published an article.
            if self.status == Post.PUBLISHED or self.status == Post.EXCLUSIVE:
                self.post_date = timezone.now()
                if not settings.DEBUG and settings.CK_METABLOG_PING_GOOGLE:
                    ping_google()
                    self.pings += 1

        if self.create_date is None:
            self.create_date = self.post_date

        super(Post, self).save(*args, **kwargs)
        self._original_status = self.status

    @staticmethod
    def query(statuses, tags=None, year=0, month=0):
        """
        Standard query function for posts.  Multiple views would call this
        method to retrieve a query set.
        """
        if tags != None and len(tags) > 0:
            posts = Post.objects.filter(
                tags__in=tags
            ).filter(
                status__in=statuses
            )
        else:
            posts = Post.objects.filter(
                status__in=statuses
            )

        if year != 0:
            posts = posts.filter(
                post_date__year=year
            )
        if month != 0:
            posts = posts.filter(
                post_date__month=month
            )

        return posts.order_by("-post_date")


################################################################################

class Category(models.Model):
    """A tag that is used to group articles into a collection.

    Used mainly for UI purposes.  Typically there will be fewer categories than tags,
    since all categories must have a corresponding Tag.
    """
    tag = models.OneToOneField(Tag)
    long_name = models.CharField(max_length=32)

    class Meta:
        verbose_name_plural = 'categories'

    def __unicode__(self):
        return self.long_name

    # Django Overrides
    @models.permalink
    def get_absolute_url(self):
        return ('metablog_category', [self.tag.slug])


################################################################################

class Slide(models.Model):
    """A meta-post, meant for single page or element view.  For example, such a post could be
    embedded in a tab slider, a gallery, or any element.

    Slides are layered content, containing a background and a post.
    """
    post = models.ForeignKey(Post, blank=True, null=True, on_delete=models.SET_NULL)
    image = models.ImageField(upload_to="images", blank=True, null=True)
    thumbnail_text = models.CharField(max_length=32)

    MEDIA_NONE = 0
    MEDIA_IMAGE = 1
    MEDIA_VIDEO = 2
    MEDIA_CHOICES = (
        (MEDIA_NONE, 'None'),
        (MEDIA_IMAGE, 'Image'),
        (MEDIA_VIDEO, 'Video'),
    )
    media_type = models.SmallIntegerField(choices=MEDIA_CHOICES)
    media_url = models.URLField(null=True, blank=True)

    def __unicode__(self):
        return self.thumbnail_text


class SlideShow(models.Model):
    """Groups slides into slideshows.
    """
    slides = models.ManyToManyField(Slide, through='SlideShowSlide')
    name = models.CharField(max_length=32, unique=True)
    title = models.CharField(max_length=128, blank=True)
    date = models.DateField(auto_now_add=True)
    description = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return "%s (%s)" % (self.name, self.date)


class SlideShowSlide(models.Model):
    """
    """
    slide = models.ForeignKey(Slide)
    slideshow = models.ForeignKey(SlideShow)
    order = models.PositiveIntegerField()

    class Meta:
        ordering = ('order',)

    def __unicode__(self):
        return "%s-%s" % (self.slideshow, self.slide)


################################################################################

class Link(models.Model):
    """
    Site name with URL, Categorization (not by Category though.)
    """
    tag = models.ForeignKey(Tag)
    rank = models.SmallIntegerField()
    title = models.CharField(max_length=64)
    url = models.URLField()

    def __unicode__(self):
        return self.title
