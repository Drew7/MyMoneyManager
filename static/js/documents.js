$(function () {

  /* Functions */

  var loadForm = function () {
    var btn = $(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $("#modal-document").modal("show");
      },
      success: function (data) {
        $("#modal-document .modal-content").html(data.html_form);
      }
    });
  };

  var saveForm = function () {
    var form = $(this);
    $.ajax({
      url: form.attr("action"),
      data: form.serialize(),
      type: form.attr("method"),
      dataType: 'json',
      success: function (data) {
        if (data.form_is_valid) {
          $("#documents-table tbody").html(data.html_document_list);
          $("#modal-document").modal("hide");
        }
        else {
          $("#modal-document .modal-content").html(data.html_form);
        }
      }
    });
    return false;
  };

  $(".js-create-document").click(loadForm);
  $("#modal-document").on("submit", ".js-document-create-form", saveForm);

  $("#documents-table").on("click", ".js-update-document", loadForm);
  $("#modal-document").on("submit", ".js-document-update-form", saveForm);

  $("#documents-table").on("click", ".js-delete-document", loadForm);
  $("#modal-document").on("submit", ".js-document-delete-form", saveForm);
  
  
});


$(document).ready(function ($) {
  $(document).on('click','.page-link', function( event ){
      event.preventDefault();
      var page =  $(this).attr('data-page');
      $.ajax({
        type: "GET",
        url: "/documents/",
        data: {
          'page': page,
        },
        dataType: "json",
        success: function (data) {
          history.pushState(null, null, newUrl('page', page));
          $("#documents-table tbody").html(data.html_document_list);
          $("#doc_pagination").html(data.html_pagination);
        }
      });
  });
  
  $('#transactions').click(function(event) { 
    event.preventDefault(); 
    $.ajax({
      type: "GET",  
      url: $('#transactions').attr('href'),
      dataType: "json",
      success: function (data) {
        history.pushState(null, null, $('#transactions').attr('href'));
        $("#documents-table").attr("hidden", false);
        $("#documents-table tbody").html(data.html_document_list);
        $("#doc_pagination").html(data.html_pagination);
      }
    });
    return false; // for good measure
  });

  function newUrl(k, v){
      var url = window.location.search;
      var arr;
      var param = k+'='+v;
      if (url.length > 0){
          arr = url.split('&');
          for( var i =0; i < arr.length; i++){
              var index = arr[i].indexOf(k);
              if (index > -1 ){
                  arr.splice(i, 1);
                  break;
              ;}
          }
      }
      else{
          arr =new Array();
      }
      arr.push(param);
      if (arr[0].indexOf('?') == -1){ arr[0]='?'+arr[0]; }
      return arr.join('&');
  }
});
