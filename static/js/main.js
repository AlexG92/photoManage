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


});