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

var originalLeave = $.fn.tooltip.Constructor.prototype.leave;
$.fn.tooltip.Constructor.prototype.leave = function(obj) {
  var self = obj instanceof this.constructor ?
    obj : $(obj.currentTarget)[this.type](this.getDelegateOptions()).data('bs.' + this.type)
  var container, timeout;

  originalLeave.call(this, obj);

  if (obj.currentTarget) {
    container = $(obj.currentTarget).siblings('.tooltip')
    timeout = self.timeout;
    container.one('mouseenter', function() {
      //We entered the actual popover – call off the dogs
      clearTimeout(timeout);
      //Let's monitor popover content instead
      container.one('mouseleave', function() {
        $.fn.tooltip.Constructor.prototype.leave.call(self, self);
      });
    })
  }
};


$('body').tooltip({
  selector: '[data-toggle]',
  trigger: 'click hover',
  placement: 'auto',
  delay: {
    show: 50,
    hide: 400
  }
});