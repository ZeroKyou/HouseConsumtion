$(document).ready(function(){
    if ($('#id_send_email').is(':checked'))
        $('.toggle-visibility').toggle(true);

    $('#id_send_email').change(function(){
        $('.toggle-visibility').slideToggle();
    });
});