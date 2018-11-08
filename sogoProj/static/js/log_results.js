$(function() {

   $( ".datepicker" ).datepicker({
     changeMonth: true,
     changeYear: true,
     yearRange: "2018:2050",
     // You can put more options here.

   });
 });

$(function() {
  $(".timing").timingfield({
    maxHour:        23,
    width:          263,
    //hoursText:      'H',
    minutesText:    'M',
    secondsText:    'S',
    hasSeconds:     true

});




});
