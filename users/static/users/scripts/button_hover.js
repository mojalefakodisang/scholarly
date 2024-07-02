$(".add-btn").hover(function() {
    $(this).append("<p>Add Content</p>");
    $(this).addClass("add-btn-animate");
}, function() {
    $(this).find("p").remove();
});