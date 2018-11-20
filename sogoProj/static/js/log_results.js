$(function() {

   $( ".datepicker" ).datepicker({
     changeMonth: true,
     changeYear: true,
     yearRange: "2018:2050",
     // You can put more options here.

   });
 });

 //$(document).ready(function() {
//      if ($('#duration_field')[0].value != 0) {
//          $(':input[type="submit"]').prop('disabled', false);
//      }
//      else {
//      $(':input[type="submit"]').prop('disabled', true);
//    }
//    })


$(document).ready(function(){
    var selected_activity = $("#activity")[0].selectedIndex;
    var activity_pk = $("#activity")[0].value
    if (selected_activity <= 0) {
      document.getElementById('sets').style.display = "none"
      document.getElementById('duration').style.display = "none"
    }
    else {
      get_target_type(activity_pk)
    }


  })

// $(function() {
//  $('#duration_field').change(function() {
//    var duration = document.getElementById('duration_field').value
//    if (duration[2] != ':') {
//       alert ('Please enter MM:SS.  Note you must enter a : for a valid entry.')
//       $(this).css("background-color","#ff3333");
//     }
//    else if (duration.substring(0,2) > 59) {
//       alert ('Maximum 59 minutes, please re-enter')
//       $(this).css("background-color","#ff3333");
// }
//    else if (duration.substring(3,5) > 59) {
//       alert ('Maximum 59 seconds, please re-enter')
//       $(this).css("background-color","#ff3333");
// }
//    else {
//      $(':input[type="submit"]').prop('disabled', false);
//      $(this).css("background-color","#FFFFFF");
//
// }
// });
//  });
//
//

// function validate_form () {
//   var activity = $("#activity")[0].value
//   var returnVal = true
//   returnval = get_target_type_cb(activity, function( json ){
//     if (json == "T") {
//     var duration = document.getElementById('duration_field').value
//     console.log(duration);
//         if (duration[2] != ':') {
//             alert ('Time invalid.  Please enter MM:SS.  Note you must enter a : for a valid entry.')
//             var returnVal= false
//                              }
//         else if (duration.substring(0,2) > 59) {
//             alert ('Maximum 59 minutes, please re-enter')
//             return false
//           }
//         else if (duration.substring(3,5) > 59) {
//             alert ('Maximum 59 seconds, please re-enter')
//             return false
//           }
//         else {
//             return true }
//              }
//     else {
//          return true
//         }
//         alert(returnVal);
//         return returnVal
//
//   })
//         alert(returnVal);
//         return returnVal
// }


$(function() {
   $('#activity').change(function() {
     console.log($(this)[0].value);
     get_target_type($(this)[0].value)

       })

   })
function get_target_type(activity) {
  console.log('func', activity);
  $.ajax({
      type: "GET",
      url: "/sogo_app/ajax/get_target_type/",
      dataType: 'json',
      data: {
        activity: activity
            },
      success: function (json) {
        console.log(json);
        if (json === 'T') {
          document.getElementById('duration').style.display = "inline"
          document.getElementById('sets').style.display = "none"

        }
        else if (json === "R") {
          document.getElementById('duration').style.display = "none"
          document.getElementById('sets').style.display = "inline"

        }
        return json

      },
      failure: function(json) {
        console.log('fail');
        console.log(json);
      }

});

 };

 // function get_target_type_cb(activity, callback) {
 //   console.log('func', activity);
 //   $.ajax({
 //       type: "GET",
 //       url: "/sogo_app/ajax/get_target_type/",
 //       dataType: 'json',
 //       data: {
 //         activity: activity
 //             },
 //       success: function (json) {callback(json) },
 //
 //       failure: function(json) {
 //         console.log('fail');
 //         console.log(json);
 //       }
 //
 // });
 //
 //  };
