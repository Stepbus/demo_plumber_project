from django.contrib import admin
from django.utils.html import format_html

from .models import KeyWords, Client, IgnoreWords


class KeyWordsAdmin(admin.ModelAdmin):
    list_display = ('key_words',)
    list_display_links = ('key_words',)
    list_filter = ('key_words',)
    search_fields = ['key_words']
    search_help_text = 'search by: KEY WORDS NAME'
    fieldsets = (
        ('Operations Details', {
            'fields': ('key_words',)
        }),
    )


class IgnoreWordsAdmin(admin.ModelAdmin):
    list_display = ('key_ignore',)
    list_display_links = ('key_ignore',)
    list_filter = ('key_ignore',)
    search_fields = ['key_ignore']
    search_help_text = 'search by: KEY IGNORE NAME'
    fieldsets = (
        ('Operations Details', {
            'fields': ('key_ignore',)
        }),
    )


class ClientAdmin(admin.ModelAdmin):
    list_display = ('client_id', 'job_title', 'date_published', 'job_location', 'type_klus',
                    'soort_probleem', 'aanvullende_informatie', 'contact_name', 'contact_email', 'contact_phone',
                    'client_page')
    list_display_links = ('client_id',)
    list_filter = (
        'job_title', 'date_published', 'job_location', 'type_klus', 'contact_name', 'contact_email', 'contact_phone')
    search_fields = ['job_title', 'date_published', 'job_location', 'type_klus', 'contact_name', 'contact_email',
                     'contact_phone']
    search_help_text = 'search by: CLIENTS fields'
    fieldsets = (
        ('Clients Details', {
            'fields': ('client_id', 'job_title', 'date_published', 'job_location', 'type_klus',
                       'soort_probleem', 'aanvullende_informatie', 'contact_name', 'contact_email', 'contact_phone',
                       'client_url')
        }),
    )

    def client_page(self, obj):
        if obj.client_url:
            return format_html("<a href='{url}'>{url_ad}</a>", url=obj.client_url, url_ad=obj.client_url)
        return


admin.site.register(KeyWords, KeyWordsAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(IgnoreWords, IgnoreWordsAdmin)
