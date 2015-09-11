//$(document).ready(function() {
//
//  var $blockFormRegistration = $('[data-block-form-registration]');
//  var $blockFormLogin = $('[data-block-form-login]');
//
//  // loading templates registration
//  $('#register_modal').on('show.bs.modal', function() {
//    $.ajax({
//      url: $blockFormRegistration.data('url'),
//      dataType: 'html',
//      success: function (data) {
//        $blockFormRegistration.html(data);
//        $("[data-form-registration]").on('submit', registration);
//        changeSocialUrls();
//      }
//    });
//  });
//
//  if (location.hash && location.hash == '#registration') {
//    $('[data-modal-button-registration]').click();
//  }
//
//  //registration
//  $("[data-form-registration-submit]").on('click', registration);
//
//  function registration(ev) {
//    ev.preventDefault();
//    var form = $blockFormRegistration.find('form');
//    $.ajax({
//      url: $blockFormRegistration.data('url'),
//      dataType: 'html',
//      data: form.serializeArray(),
//      type: 'POST',
//      success: function (data) {
//        $("[data-form-registration]").off('submit', registration);
//        $blockFormRegistration.html(data);
//        $("[data-form-registration]").on('submit', registration);
//        if ($blockFormRegistration.find('form').length == 0) {
//          $('[data-form-registration-submit]').detach();
//        } else {
//          changeSocialUrls();
//        }
//      }
//    });
//  }
//
//  function parseUrlQuery() {
//    var data = {};
//    if (location.search) {
//      var pair = (location.search.substr(1)).split('&');
//      for (var i = 0; i < pair.length; i++) {
//        var param = pair[i].split('=');
//        data[param[0]] = param[1];
//      }
//    }
//    return data;
//  }
//
//  function changeSocialUrls() {
//    var urlQuery = parseUrlQuery();
//    if (urlQuery.next){
//      var $socialUrls = $('[data-social-url]');
//
//      for (var i = 0; i < $socialUrls.length; i++) {
//        var $socialUrl = $($socialUrls[i]);
//        var oldSocialUrl = $socialUrl.attr('href');
//        var newSocialUrl = oldSocialUrl + '?next=' + urlQuery.next;
//        $socialUrl.attr('href', newSocialUrl);
//      }
//    }
//  }
//
//  $('[data-disconnect-social-account]').on('click', function(event){
//    event.preventDefault();
//    var $event = $(event.currentTarget);
//    $event.prev('form').submit();
//  });
//
//  $('[data-require-email-form]').validate({
//     errorClass: "text-danger",
//     rules:{
//        email:{
//          required: true,
//          email: true
//        }
//     },
//     messages:{
//        email:{
//          required: "Обязательное поле.",
//          email: "Введите правильный адрес электронной почты."
//        }
//     }
//  });
//
//});