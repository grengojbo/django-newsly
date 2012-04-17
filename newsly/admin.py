# -*- coding: utf-8 -*-

from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

from newsly.models import *
from newsly.conf import settings

if settings.GRPAPPELLI_TINYMCE:
    NEWSLY_JS = [
        '%s%s' % (settings.STATIC_URL, settings.GRPAPPELLI_TINYMCE_SRC),
        '%s%s' % (settings.STATIC_URL, settings.GRPAPPELLI_TINYMCE_CONF)]
else:
    NEWSLY_JS = []

try:
    from grappellifit.admin import TranslationAdmin, TranslationStackedInline
    ModelAdmin = TranslationAdmin
    StackedInlineAdmin = TranslationStackedInline
except:
    ModelAdmin = admin.ModelAdmin
    StackedInlineAdmin = admin.StackedInline


class NewsVideoInline(StackedInlineAdmin):
    model = NewsVideo
    extra = 1
    fieldsets = (
        (None, {
            'fields': (
                'title', 'video',
                ('position', 'is_visible',)
            )
        }),
    )


class NewsPhotoInline(StackedInlineAdmin):
    model = NewsPhoto
    extra = 1
    fieldsets = (
        (None, {
            'fields': (
                'title', 'photo',
                ('position', 'is_visible',)
            )
        }),
    )


class NewsDocumentInline(StackedInlineAdmin):
    model = NewsDocument
    extra = 1
    fieldsets = (
        (None, {
            'fields': (
                'title', 'document',
                ('position', 'is_visible',)
            )
        }),
    )


class NewsAdmin(ModelAdmin):
    list_display = ('title', 'author', 'date_added', 'date_publish', 'date_unpublish')
    list_filter = ('author',)
    search_fields = ('title',)
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'date_publish'
    inlines = [NewsPhotoInline, NewsVideoInline, NewsDocumentInline]

    fieldsets = (
        (None, {
            'fields': (
                'author', 
                'category',
                'date_publish', 
                'date_unpublish',
            )
        }),
        (_('Title'), {
            'fields': ('title', 'slug',)
        }),
        (_('Teaser'), {
            'fields': ('teaser',)
        }),
        (_('Content'), {
            'fields': ('body',)
        }),
        (_('SEO'), {
            'fields': ('meta_keywords', 'meta_description',)
        }),
    )

    class Media:
        # FIXME: This might clash with TranslationAdmin.Media.js ..
        js = NEWSLY_JS

admin.site.register(News, NewsAdmin)
