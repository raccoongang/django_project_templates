/**
 * Created by sendr on 23.07.15.
 */


jQuery(document).ready(function ($) {
  //   script for choosing images

  $('.interest_choice a').on('click', function(){
    var check = $(this).next();
    if (check.prop('checked')) {
      check.removeAttr('checked');
      $(this).css('background-color', 'inherit');
    }
    else {
      check.prop('checked', 'checked');
      $(this).css('background-color', '#cacaca');
    }
  });

  // slideUp for course item

  $('.span-close').on('click', function(){
      $(this).parentsUntil('.close-modal').slideUp(300);
  });

  //slideUp for del_element in book.html !!!!!!!temporarily!!!!!!!!!!!

  $('.del_element').on('click', function(){
      $(this).closest('.what_slideUp').slideUp(300);
  });

  $('.grid').isotope({
    // options
    itemSelector: '.grid-item',
    percentPosition: 'true'
  });

  // for search
  $('.cust_button').on('click', function(){
     if($(this).hasClass('cust_button_click'))
     {
         $(this).removeClass('cust_button_click');
         $(this).removeAttr('checked');
     }
      else{
         $(this).addClass('cust_button_click');
         $(this).attr("checked", true);
     }
  });

  //  for subscribe button
  $('.cust_radio').on('click', function(){
     if($(this).hasClass('cust_button_click'))
     {
         $(this).removeClass('cust_button_click');
         $(this).removeAttr('checked');
     }
      else{
         $(this).addClass('cust_button_click');
         $(this).attr("checked", true);
     }
  });
  $(".js-example-basic-multiple").select2();
  $(".js-example-basic-single").select2();
  $(".js-example-tags").select2({
      tags: true
  });
  $("[name='public_boolean']").bootstrapSwitch();
  $('.prev_page').on('click', function(ev){
      ev.preventDefault();
      history.back();
  });
  $('.show_hide').on('click', function(ev){
      ev.preventDefault();
      $('[data-what-show]').toggleClass('hidden');
      if ($('[data-what-show]').hasClass('hidden')){
          $('.show_hide').text('показать все');
      } else {
          $('.show_hide').text('скрыть');
      }
  });

  // remove followed
  $('[data-button-followed-remove]').hover(
    function(event){
      $(event.currentTarget).toggleClass('btn-primary btn-danger').val('Отмена');
    },
    function(event){
      $(event.currentTarget).toggleClass('btn-primary btn-danger').val('Читаю');
    }
  );

  $('[data-button-ajax-followed-remove]').on('click', function(event) {
    var $event = $(event.currentTarget);
    var csrfmiddlewaretoken = $('[name = "csrfmiddlewaretoken"]').val();
    $.ajax({
      url: $event.data('url'),
      data: {csrfmiddlewaretoken: csrfmiddlewaretoken},
      dataType: 'json',
      type: 'POST',
      success: function (data) {
        $('[data-following-count]').text(data.following_count);
        $event.parents('li').remove();
      }
    });
  });

  // add tags in settings account
  var $selectSettingsTags = $('[data-select-settings-tags]');

  $selectSettingsTags.select2({
    language: 'ru',
    ajax: {
      url: $selectSettingsTags.data("url"),
      dataType: 'json',
      delay: 250,
      data: function (params) {
        return {
          q: params.term,
          account_id: $selectSettingsTags.data("account-id")
        };
      },
      processResults: function (data) {
        return {
          results: data.items
        };
      },
      cache: true
    },
    tags: true,
    minimumInputLength: 3,
    templateResult: formatRepoSettingsTags,
    templateSelection: formatRepoSelectionSettingsTags
  });

  function formatRepoSettingsTags(repo) {
    if (repo.loading) return repo.text;
    var markup = repo.name;
    return markup;
  }

  function formatRepoSelectionSettingsTags (repo) {
    return repo.name || repo.text;
  }

  $selectSettingsTags.parents('form').validate({
     rules:{
        tags:{
          required: true
        }
     },
     messages:{
        tags:{
          required: ""
        }
     }
  });


});
