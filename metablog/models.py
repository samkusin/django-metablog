"""@package docstring
Django Model for the Metablog Application.

Association between tags and posts.
"""

from django.db import models
from django.contrib.auth.models import User


class Tag(models.Model):
    """Tags are used for searching and organizing blog posts.
    """
    name = models.CharField(max_length=24)
    slug = models.SlugField(max_length=24)

    def __unicode__(self):
        return self.name


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
    post_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    status = models.SmallIntegerField(choices=STATUS_CHOICES, db_index=True)
    prev_post = models.OneToOneField('self', related_name='next', null=True, blank=True)
    next_post = models.OneToOneField('self', related_name='prev', null=True, blank=True)
    tags = models.ManyToManyField(Tag)
    text = models.TextField()
    atj_word_count = models.SmallIntegerField(verbose_name='After the Jump word count', default=150)

    def __unicode__(self):
        return self.title

    # Django overrides
    @models.permalink
    def get_absolute_url(self):
        return ('metablog_article', [self.slug])


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
