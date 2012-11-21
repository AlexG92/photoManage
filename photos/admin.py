from photos.models import Photo, Album
from django.contrib import admin

class PhotoAdmin(admin.ModelAdmin):
    list_filter = ['pub_date']
    date_hierarchy = 'pub_date'
    list_display = ('album','title', 'pub_date')
    fieldsets = [
        (None,  {'fields': ['album', 'title', 'photo', 'pub_date']}),
    ]

admin.site.register(Photo, PhotoAdmin)
admin.site.register(Album)