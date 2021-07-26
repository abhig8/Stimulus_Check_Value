$(document).ready(function() {
  $('#stocks').DataTable({
    "paging": false,
    "bAutoWidth": false,
    "order": [[ 2, "desc" ]],
    language: {
	    searchPlaceholder: "Search",
	    search: "",
  	}
  });
});


function beeLeft() {
  $("#moving_meme").animate({left: "0%"}, 4000, "swing", beeRight);
}
function beeRight() {
  $("#moving_meme").animate({left: $(window).width() - 150}, 3500, "swing", beeLeft);
}
beeRight();


function checkRadio(){
  document.getElementById('image_custom').checked = "checked";
}