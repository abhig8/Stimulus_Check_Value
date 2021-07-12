$(document).ready(function() {
  $('#stocks').DataTable({
  	"dom":"ftip",
    "paging": false,
    'columnDefs': [
    {'width': '270', 'targets': 0},
    {'width': '100', 'targets': 1},
    {'width': '100', 'targets': 2}
    ],
    "order": [[ 1, "desc" ]],
    language: {
	    searchPlaceholder: "Search",
	    search: "",
  	}
  });
});


function beeLeft() {
  $("#kitty").animate({left: "-0%"}, 4000, "swing", beeRight);
}
function beeRight() {
  $("#kitty").animate({left: "100%"}, 3500, "swing", beeLeft);
}


beeRight();

function checkRadio(){
  document.getElementById('image_custom').checked = "checked";
}