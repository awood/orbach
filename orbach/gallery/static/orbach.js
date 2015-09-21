window.setTimeout(function() {
    $(".flash-fade-out").fadeTo(500, 0).slideUp(500, function(){
        $(this).remove();
    });
}, 5000);
