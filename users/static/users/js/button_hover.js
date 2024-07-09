$(document).ready(function() {
    $("input[type='radio']").hover(
        function() {
            $(this).next('label').css('opacity', '0.5')
        },
        function() {
            $(this).next('label').css('opacity', '1')
        },
    )
});