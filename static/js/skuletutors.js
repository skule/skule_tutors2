jQuery(document).ready(function () {
    //toggle the component with class qualifications/heading
    jQuery(".qualifications").click(function () {
        jQuery(this).children(".qualifications .content").toggleClass('open');
    });
});