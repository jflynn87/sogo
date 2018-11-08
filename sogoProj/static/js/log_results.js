$(function() {

   $( ".datepicker" ).datepicker({
     changeMonth: true,
     changeYear: true,
     yearRange: "2018:2050",
     // You can put more options here.

   });
 });

 $(document).ready(function() {
      $(':input[type="submit"]').prop('disabled', true);
    })

$(function() {
 $('#duration').change(function() {
   var duration = document.getElementById('duration').value
   if (duration[2] != ':') {
      alert ('Please enter MM:SS.  Note you must enter a : for a valid entry.')
      $(this).css("background-color","#ff3333");
    }
   else {
     $(':input[type="submit"]').prop('disabled', false);
     $(this).css("background-color","#FFFFFF");

}
});
 });


 $(function() {
  $('#submit').click(function() {
    var duration = document.getElementById('duration').value
    if (duration[2] != ':') {
       alert ('Please enter MM:SS.  Note you must enter a : for a valid entry.')
 }
 });
  });



// $(function() {
//   $(".duration").durationPicker({
//     minutes: {
//       label: "m",
//       min: 0,
//       max: 59
//     },
//     seconds: {
//       label: "s",
//       min: 0,
//       max: 59
//     },
//     classname: 'form-control',
//     responsive: true
//
// });
//
// $(function() {
//   $("#{submit}").click({
//     console.log('click');
//
//
//
//
// });
