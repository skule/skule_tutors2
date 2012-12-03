jQuery(document).ready(function() {
  //toggle the componenet with class msg_body
  jQuery(".qualifications .heading").click(function()
  {
    jQuery(this).next(".qualifications .content").toggleClass('open');
  });
});