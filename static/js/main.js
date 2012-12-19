$(document).ready(function() {

/**
$('.albumTitle').click(function(){
    var albumTitle = prompt('Please enter a new album name');
    return false;
})
**/

$('.albumTitle').click(function(){
    var id = $(this).attr('id')
    $('#albumTitleChangeID').val(id);
})

$('.photoTitle').click(function(){
    var id = $(this).attr('id')
    $('#photoTitleChangeID').val(id);
})


$(function() {
    $( ".draggable" ).draggable();
    $( ".droppable" ).droppable({
        drop: function( event, ui ) {
            // Not the fastest commands
            albumID = $(this).find('.albumTitle').attr('id');
            photoID = ui.draggable.find('.photoTitle').attr('id');

            $('#photoID').attr('value',photoID);
            $('#albumID').attr('value',albumID);
            $('#assignPhotoToAlbum').submit()
        }
    });
});

});