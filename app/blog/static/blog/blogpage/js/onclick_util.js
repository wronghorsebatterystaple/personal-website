$(document).ready(function() {
    $("#copy-permanent-link-btn").on("click", function() {
        navigator.clipboard.writeText(URL_ABS_POST_PERMANENT_LINK);
        customFlash("Link copied!");
    });
});
