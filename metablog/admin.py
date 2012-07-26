from django import forms
from django.contrib import admin

# used for rich textareas
from ckeditor.widgets import CKEditorWidget

from models import Tag, Post, Category, Slide, SlideShow, SlideShowSlide
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


admin.site.register(Post, PostAdmin)

################################################################################


admin.site.register(Category)

admin.site.register(Slide)
admin.site.register(SlideShow)
admin.site.register(SlideShowSlide)

#class PhotoAdmin(AdminImageMixin, admin.ModelAdmin):
#    pass

#admin.site.register(Photo, PhotoAdmin)
