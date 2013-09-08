function hideForm() {
  $('#feedbackForm').fadeOut('fast', function() {
    $('#feedbackSnippet').animate({
      bottom: '-4'
    });
  });
}

function initiateForm() {
  $('#feedbackForm').unbind('submit');
  $('#feedbackForm input, #feedbackForm textarea').each(function() {
    $(this).attr('placeholder', $('[for=' + $(this).attr('id') + ']').text());
  });

  $('#feedbackForm #feedbackClose').click(function() {
    hideForm();
    return false;
  });

  $('#feedbackForm').submit(function() {
    var form = $(this);
    $.post(form.attr('action'), form.serializeArray(), function(data) {
      if (data.toLowerCase().indexOf('errorlist') == -1) {
        hideForm();
        $('#feedbackSuccess').fadeIn().delay(2000).animate({
          bottom: '-500'
        }).fadeOut().animate({
          bottom: '40'
        });

      }
      form.html(data);
      initiateForm();
    });
    return false;
  });

  $('#feedbackSnippet').attr('href', '#');
  $('#feedbackSnippet').click(function() {
    $(this).animate({
      bottom: '-100'
    });

    $('#feedbackForm').fadeIn();
    $('html').click(function() {
      hideForm();
    });

    $('#feedbackForm').click(function(event) {
      event.stopPropagation();
    });
    return false;
  });
}

$(document).ready(function() {
  initiateForm();
});
