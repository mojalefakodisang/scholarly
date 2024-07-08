$(".add-btn").hover(function() {
    $(this).append("<p>Add Content</p>");
    $(this).addClass("add-btn");
}, function() {
    $(this).find("p").remove();
});

$(".add-review-btn").hover(function() {
    $(this).append("<p>Add Review</p>");
    $(this).addClass("add-btn-animate");
}, function() {
    $(this).find("p").remove();
});