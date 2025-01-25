'use strict';

(function ($) {
	
	
	
})(jQuery);

$(function () {

    ///نمایش زیر منو
    $(".showCategorySubMenu").click(function () {
      $(this).closest('li').find(" > ul").toggleClass("show");
      $(this).toggleClass('open');
    })
});