from django import forms
from django.contrib import admin

# used for rich textareas
from ckeditor.widgets import CKEditorWidget

from models import Tag, Post, Category, Slide, SlideShow, SlideShowSlide, Link

from sorl.thumbnail.admin import AdminImageMixin

################################################################################


class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        "slug": ("name",)
    }

admin.site.register(Tag, TagAdmin)

################################################################################


class PostAdminForm(forms.ModelForm):

    class Meta:
        model = Post

    def __init__(self, *args, **kwargs):
        super(PostAdminForm, self).__init__(*args, **kwargs)
        self.fields['text'].widget = CKEditorWidget(config_name='edit_post')


class PostAdmin(admin.ModelAdmin):
    form = PostAdminForm
    prepopulated_fields = {
        "slug": ("title",)
    }

    list_display = (
        'title', 'author', 'post_date', 'status', 'tag_list'
    )

    ordering = (
        'post_date',
    )

    def tag_list(self, obj):
        tag_str = ''
        for tag in obj.tags.all():
            tag_str += tag.name + ', '

        if len(tag_str) < 2:
            return ''
        return tag_str[:-2]

    tag_list.short_description = 'Tags'

admin.site.register(Post, PostAdmin)


################################################################################

class CategoryAdmin(admin.ModelAdmin):

    list_display = (
        'long_name',
        'tag',
    )


admin.site.register(Category, CategoryAdmin)


admin.site.register(Slide)
admin.site.register(SlideShow)
admin.site.register(SlideShowSlide)


################################################################################

class LinkAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'url', 'tag', 'rank'
    )
    ordering = ( 'tag', 'rank', )

admin.site.register(Link, LinkAdmin)

#class PhotoAdmin(AdminImageMixin, admin.ModelAdmin):
#    pass

#admin.site.register(Photo, PhotoAdmin)
