$(document).ready(function() {
  $('#stocks').DataTable({
    "paging": false,
    'columnDefs': [
    {'width': '270', 'targets': 0},
    {'width': '100', 'targets': 1},
    {'width': '100', 'targets': 2}
    ],
    "order": [[ 1, "desc" ]],
  });
});


$(document).ready(function() {
    $("#b").animate({left: "+=700"}, 2500);
    $("#b").animate({left: "-=500"}, 1500);
});
