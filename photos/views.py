from os import remove
from django import forms
from django.core.files import File
from django.db.models.fields.files import ImageField
from django.core.files.uploadedfile import SimpleUploadedFile
from django.shortcuts import get_object_or_404, render_to_response
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.views.decorators.http import require_POST
from photoManage.photos.models import *
from photoManage.util import uri
from photoManage.util import render

@uri('photos/')
@login_required
def index(request):
    """
    Main Photo Management Page

    Redirected here after REGISTRATION or LOGIN
    All POST actions to manipulate PHOTOS and ALBUMS redirect to this view

    Functionality included in this view:
    CRUD Photo
    CRUD Album
    """

    #Collect all photos owned by the user and not associated with albums for display
    photos = Photo.objects.filter(owner = request.user, album_id=None)

    #Collect all albums owned by the user for display
    albums = Album.objects.filter(owner = request.user)

    #Form to upload multiple images extends Djangos form.ImageField()
    #Fields taken 'file' (image)
    form = UploadFileForm()

    #Form to upload album
    #Fields taken are 'title'(charfield)
    formAlbum = AlbumForm()
    return render_to_response('photos/index.html',
        {
            'form': form,
            'formAlbum': formAlbum,
            'photos': photos,
            'albums':albums,
        },
        context_instance=RequestContext(request))

@uri('photos/newphoto/', method='POST')
@login_required
@require_POST
def newphoto(request):
    form = UploadFileForm(request.POST, request.FILES)
    if form.is_valid():
        for file in request.FILES.getlist('file'):
            Photo(owner = request.user, pub_date = timezone.now(), photo = file, title = file.name ).save()
        return HttpResponseRedirect("/photos/")
    else:
        request.session['error_message_photo'] = "Please upload JPGS, GIFS, or PNG format only"
        return HttpResponseRedirect("/photos/")
        #return render_to_response('photos/index.html', {'form': form, 'photos': photos, "albums":albums, 'error_message_photo': error_message},context_instance=RequestContext(request))

@uri('photos/changephotoname/', method='POST')
@login_required
@require_POST
def changephotoname(request):
    form = ChangeFileName(request.POST)
    if form.is_valid():
        photo = Photo.objects.get(pk = request.POST['photoTitleChangeID'], owner = request.user)
        photo.title = request.POST['title']
        photo.save()
        return HttpResponseRedirect("/photos/")
    else:
        request.session['error_message_photo']  = "Please input a proper title"
        return HttpResponseRedirect("/photos/")
        #return render_to_response('photos/index.html', {'form': form, 'photos': photos, "albums":albums, 'error_message_photo': error_message},context_instance=RequestContext(request))

@uri('photos/deletephoto/', method='POST')
@login_required
@require_POST
def deletephoto(request):
    photo = Photo.objects.get(pk = request.POST['delete'], owner = request.user)
    os.remove(photo.photo.path)
    photo.delete()
    return HttpResponseRedirect("/photos/")

@uri('photos/newalbum/', method='POST')
@login_required
@require_POST
def newalbum(request):
    form = AlbumForm(request.POST)
    if form.is_valid():
        Album(owner = request.user, title = request.POST['title']).save()
        return HttpResponseRedirect("/photos/")
    else:
        request.session['error_message_album']  = "Please input a proper album name"
        form = AlbumForm()
        return HttpResponseRedirect("/photos/")
        #return render_to_response('photos/index.html', {'form': form, 'photos': photos, "albums":albums, 'error_message_album': error_message},context_instance=RequestContext(request))

@uri('photos/changealbumname/', method='POST')
@login_required
@require_POST
def changealbumname(request):
    form = AlbumForm(request.POST)
    if form.is_valid():
        album = Album.objects.get(pk = request.POST['albumTitleChangeID'], owner=request.user)
        album.title = request.POST['title']
        album.save()
        return HttpResponseRedirect("/photos/")
    else:
        request.session['error_message_album'] = "Please input a proper album name"
        form = AlbumForm()
        return HttpResponseRedirect("/photos/")
        #return render_to_response('photos/index.html', {'form': form, 'photos': photos, "albums":albums, 'error_message_album': error_message},context_instance=RequestContext(request))

@uri('photos/deletealbum/', method='POST')
@login_required
@require_POST
def deletealbum(request):
    Album.objects.get(pk = request.POST['delete'], owner = request.user).delete()
    return HttpResponseRedirect("/photos/")

@uri('photos/album/(?P<album_id>\d+)')
@login_required
def album(request, album_id):
    albumSelected = get_object_or_404(Album, pk=album_id)
    photos = Photo.objects.filter(owner = request.user).exclude(album__isnull=False)
    albumPhotos = Photo.objects.filter(owner = request.user, album_id = albumSelected)
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            for file in request.FILES.getlist('file'):
                Photo(owner = request.user, pub_date = timezone.now(), photo = file, title = file.name ).save()
            return render_to_response('album/index.html', {'form': form, 'albumNumber': albumSelected, 'photos': photos, 'albumPhotos':albumPhotos},context_instance=RequestContext(request))
        elif 'delete' in request.POST:
            if photo.owner == request.user:
                photo = Photo(pk = request.POST['delete'])
                photo.delete()
            return render_to_response('album/index.html', {'albumNumber': albumSelected, 'photos': photos, 'albumPhotos':albumPhotos},context_instance=RequestContext(request))
        elif 'addAlbum' in request.POST:
            photo = Photo.objects.filter(pk = request.POST['addAlbum']).update(album = albumSelected)
            return render_to_response('album/index.html', {'albumNumber': albumSelected, 'photos': photos, 'albumPhotos':albumPhotos},context_instance=RequestContext(request))
        else:
            error_message = "Please input a proper album name"
            form = AlbumForm()
            return render_to_response('album/index.html', {'albumNumber': albumSelected, 'error_message': error_message, 'albumPhotos':albumPhotos},context_instance=RequestContext(request))
    else:
        return render_to_response('album/index.html', {'photos': photos, 'albumSelected': albumSelected, 'albumPhotos':albumPhotos},context_instance=RequestContext(request))