"""@package docstring
Django Model for the Metablog Application.

Association between tags and posts.
"""

from datetime import datetime

from django.db import models
from django.contrib.auth.models import User


class Tag(models.Model):
    """Tags are used for searching and organizing blog posts.
    """
    name = models.CharField(max_length=24)
    slug = models.SlugField(max_length=24)

    def __unicode__(self):
        return self.name


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
    status = models.SmallIntegerField(choices=STATUS_CHOICES)
    prev_post = models.OneToOneField('self', related_name='next', null=True, blank=True)
    next_post = models.OneToOneField('self', related_name='prev', null=True, blank=True)
    tags = models.ManyToManyField(Tag)
    text = models.TextField()

    def __unicode__(self):
        return self.title

    # Django overrides
    @models.permalink
    def get_absolute_url(self):
        return ('view_article', [self.slug])

    # Utilities
    @staticmethod
    def get_posts_within_date_range(latest_post_time, earliest_post_time, tags=None):
        """Returns an array of posts with post time, descending order by post creation time.
                ( time: datetime, post:Post )

        @param latest_post_time The latest time and date for the post search.  Only posts created
            on or before this value are returned.
        @param earliest_post_time The earliest time and date for the post search.  Only posts created
            after (but not *on*) this value are returned.
        @param tags (optional) Filter posts returned with the array of Tags.  This is an 'or' operation
            - posts are tagged with at least one of the Tags specified.
        @return array of posts
        """
        if tags:
            posts = Post.objects.filter(
                    post_date__lte=latest_post_time, post_date__gt=earliest_post_time
                ).filter(
                    tags__in=tags
                )
        else:
            posts = Post.objects.filter(
                    post_date__lte=latest_post_time, post_date__gt=earliest_post_time
                )

        # build result list
        return posts

    @staticmethod
    def get_posts_before_post_index(num_posts, first_post_offset=0, tags=None):
        """Returns an array of posts relative to the specified post offset.  Common use cases
        include retrieving a specified number of posts for a blog page.   Callers can retrieve
        a subset of all posts within the database using this method.

        @param num_posts Maximum number of posts to retrieve.
        @param first_post_index Returns posts starting with the post at this specified offset within
            the database.
        @param tags (optional) Filter posts returned with the array of Tags.  This is an 'or' operation
            - posts are tagged with at least one of the Tags specified.
        @return An array of Posts.
        """
        posts = None

        if tags:
            posts = Post.objects.filter(tags__in=tags)[first_post_offset:num_posts]
        else:
            posts = Post.objects.all()[first_post_offset:num_posts]

        return posts


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
        return ('view_category', [self.tag.slug])

    # Utilities
    def get_posts_within_date_range(self, latest_post_time, earliest_post_time):
        """Return posts within a specific category.

        @param latest_post_time The latest time and date for the post search.  Only posts created
            on or before this value are returned.
        @param earliest_post_time The earliest time and date for the post search.  Only posts created
            after (but not *on*) this value are returned.
        @return array posts
        """
        tags = [self.tag]
        return Post.get_posts_within_date_range(latest_post_time, earliest_post_time, tags)

    def get_posts_before_post_index(self, num_posts, first_post_offset=0):
        """Returns an array of posts relative to the specified post offset
        @param num_posts Maximum number of posts to retrieve.
        @param first_post_index Returns posts starting with the post at this specified offset within
            the database.
        @return An array of Posts.
        """
        tags = [self.tag]
        return Post.get_posts_before_post_index(num_posts, first_post_offset, tags)


################################################################################

class Slide(models.Model):
    """A meta-post, meant for single page or element view.  For example, such a post could be
    embedded in a tab slider, a gallery, or any element.

    Slides are layered content, containing a background and a post.
    """
    post = models.ForeignKey(Post, null=True, on_delete=models.SET_NULL)
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
        return self.post.title


class SlideShow(models.Model):
    """Groups slides into slideshows.
    """
    slides = models.ManyToManyField(Slide)
    name = models.CharField(max_length=32, unique=True)
    date = models.DateField(auto_now_add=True)
    description = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return "%s (%s)" % (self.name, self.date)
