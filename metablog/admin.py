from django.contrib import admin

# used for rich textareas
from wysihtml5.admin import AdminWysihtml5TextFieldMixin
#from django_summernote.admin import SummernoteModelAdmin
from wysihtml5.fields import Wysihtml5TextField
from wysihtml5.widgets import Wysihtml5TextareaWidget

from models import Tag, Post, Category, Slide, SlideShow, SlideShowSlide, Link
#from sorl.thumbnail.admin import AdminImageMixin

################################################################################


class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        "slug": ("name",)
    }

admin.site.register(Tag, TagAdmin)

################################################################################


class PostAdmin(admin.ModelAdmin):
    change_form_template = 'metablog/admin/change_form.html'
    prepopulated_fields = {
        "slug": ("title",)
    }

    list_display = (
        'title', 'author', 'post_date', 'status', 'tag_list'
    )

    ordering = (
        'post_date',
    )

    formfield_overrides = {
        Wysihtml5TextField: {'widget': Wysihtml5TextareaWidget(attrs={'rows':20})}
    }

    def tag_list(self, obj):
        tag_str = ''
        for tag in obj.tags.all():
            tag_str += tag.name + ', '

        if len(tag_str) < 2:
            return ''
        return tag_str[:-2]

    tag_list.short_description = 'Tags'
    """
    def formfield_for_dbfield(self, db_field, **kwargs):
        if isinstance(db_field, Wysihtml5TextField):
            return db_field.formfield(widget=Wysihtml5TextareaWidget(attrs={'rows':50}))
        sup = super(PostAdmin, self)
        return sup.formfield_for_dbfield(db_field, **kwargs)
    """

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
