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
from StringIO import StringIO
import zipfile
from zipfile import ZipFile
from django.http import HttpResponse
from photoManage.photos.models import *
from django.contrib import messages
from photoManage.util import uri, render_to_json
from photoManage.photos.thumbnail import create_thumb
from photoManage.photos.photofilesystem import get_directory, change_directory
import shutil

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

@uri('photos/album/(?P<album_id>\d+)')
@login_required
def album(request, album_id):
    albumSelected = get_object_or_404(Album, pk=album_id)
    photos = Photo.objects.filter(owner = request.user).exclude(album__isnull=False)
    albumPhotos = Photo.objects.filter(owner = request.user, album_id = albumSelected)
    return render_to_response('album/index.html',
        {
            'photos': photos,
            'albumSelected': albumSelected,
            'albumPhotos':albumPhotos,
            'album':albumSelected,
        },
        context_instance=RequestContext(request))

@uri('photos/newphoto/', method='POST')
@login_required
@require_POST
def newphoto(request):
    form = UploadFileForm(request.POST, request.FILES)
    requestOrigin = request.META['HTTP_REFERER']
    if form.is_valid():
        albumSelected = request.POST.get('albumid', None)
        for file in request.FILES.getlist('file'):
            Photo(owner = request.user, pub_date = timezone.now(), photo = file, title = file.name, album_id = albumSelected ).save()
            #create_thumb(request.user, str(file), album=None)
        return HttpResponseRedirect(requestOrigin)
    else:
        messages.error(request, 'Please upload JPGS, GIFS, or PNG format only.')
        return HttpResponseRedirect(requestOrigin)

@uri('photos/changephotoname/', method='POST')
@login_required
@require_POST
def changephotoname(request):
    form = ChangeFileName(request.POST)
    requestOrigin = request.META['HTTP_REFERER']
    if form.is_valid():
        photo = Photo.objects.get(pk = request.POST['photoTitleChangeID'], owner = request.user)
        photo.title = request.POST['title']
        photo.save()
        return HttpResponseRedirect(requestOrigin)
    else:
        messages.error(request, 'Please input a proper title')
        return HttpResponseRedirect(requestOrigin)

@uri('photos/deletephoto/', method='POST')
@login_required
@require_POST
def deletephoto(request):
    photo = Photo.objects.get(pk = request.POST['delete'], owner = request.user)
    os.remove(photo.photo.path)
    photo.delete()
    requestOrigin = request.META['HTTP_REFERER']
    return HttpResponseRedirect(requestOrigin)

@uri('photos/newalbum/', method='POST')
@login_required
@require_POST
def newalbum(request):
    form = AlbumForm(request.POST)
    requestOrigin = request.META['HTTP_REFERER']
    if form.is_valid():
        Album(owner = request.user, title = request.POST['title']).save()
        return HttpResponseRedirect(requestOrigin)
    else:
        messages.error(request, 'Please input a proper title')
        return HttpResponseRedirect(requestOrigin)

@uri('photos/changealbumname/', method='POST')
@login_required
@require_POST
def changealbumname(request):
    form = AlbumForm(request.POST)
    requestOrigin = request.META['HTTP_REFERER']
    if form.is_valid():
        try:
            album = Album.objects.get(pk = request.POST['albumTitleChangeID'], owner=request.user)
            currentAlbumTitle = album.title
            album.title = request.POST['title']
            source = get_directory(request.user, None, currentAlbumTitle, False)
            destination = get_directory(request.user, None, album.title, False)
            change_directory(source,destination)
            photos = Photo.objects.filter(album = album, owner = request.user)
            for photo in photos:
                filename = photo.filename()
                photo.photo = 'photographs/' + photo.owner.username + '/' + album.title + '/' + filename
                photo.save()
            album.save()
            return HttpResponseRedirect(requestOrigin)
        except Exception as e:
            messages.error(request, '%s' % e.message)
            return HttpResponseRedirect(requestOrigin)
    else:
        messages.error(request, 'Please input a proper title')
        return HttpResponseRedirect(requestOrigin)

@uri('photos/deletealbum/', method='POST')
@login_required
@require_POST
def deletealbum(request):
    requestOrigin = request.META['HTTP_REFERER']
    album = Album.objects.get(pk = request.POST['delete'], owner = request.user)
    photos = Photo.objects.filter(album = album, owner = request.user)
    for photo in photos:
        filename = photo.filename()
        source = photo.photo.path
        destination = get_directory(request.user, filename,)
        photo.photo = 'photographs/' + photo.owner.username + '/' + filename
        photo.save()
        shutil.move(source, destination)
    currentLocation = get_directory(request.user, None, album.title)
    try:
        shutil.rmtree(currentLocation)
    except Exception as e:
        messages.error(request, '%s (%s)' % (e.message, type(e)))
    album.delete()
    return HttpResponseRedirect(requestOrigin)

@uri('photos/assignphototoalbum/', method='POST')
@login_required
@require_POST
def assignphototoalbum(request):
    albumSelected = Album.objects.get(pk = request.POST['albumid'], owner = request.user)
    photo = Photo.objects.get(pk = request.POST['addToAlbum'], owner = request.user)
    filename = photo.filename()
    source = photo.photo.path
    destination = get_directory(request.user, filename, albumSelected)
    shutil.move(source, destination)
    photo.album = albumSelected
    photo.photo = 'photographs/' + photo.owner.username + '/' + albumSelected.title + '/' + filename
    photo.save()
    requestOrigin = request.META['HTTP_REFERER']
    return HttpResponseRedirect(requestOrigin)

@uri('photos/download/')
@login_required
def download_zip(request):
    path = os.path.join('media\photographs\\', '%s' % request.user)
    in_memory = StringIO()
    zip = ZipFile(in_memory, 'a', zipfile.ZIP_DEFLATED)
    for root, dirs, files in os.walk(path):
        for file in files:
            zip.write(os.path.join(root, file))
    zip.close()
    response = HttpResponse(mimetype="application/zip")
    response["Content-Disposition"] = "attachment; filename=photos.zip"

    in_memory.seek(0)
    response.write(in_memory.read())
    return response