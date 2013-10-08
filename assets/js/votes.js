
$(function () {
  $('#vote, .votes').click(function() {
    var $this = $(this);
    var itemType = $this.attr('data-type');
    var itemId = $this.attr('data-id');

    var $symbol = $('#vote');  // button without the number of votes
    var $buttons = $(  // buttons to upvote the same item
      '.votes[data-id="' + itemId + '"][data-type="' + itemType + '"]'
    );

    // TODO: use django's url function
    var voteUrl = '/' + itemType + '/' + itemId +'/upvote';

    $.ajax({
      type: 'POST',
      url: voteUrl,
      data: 'csrfmiddlewaretoken=' + window.csrfToken
    }).always(function (xhr) {
      var result = $.parseJSON(xhr.responseText).result,
          curValue = parseInt($this.html(), 10),
          newValue, iconClasses, symbolIcon;

      // when clicking on button w/out n. of votes
      if (isNaN(curValue) && $buttons.length > 0) {
        curValue = parseInt($buttons.eq(0).html(), 10);
      }

      if (result === 'voted') {
        newValue = curValue + 1;
        iconClasses = 'lsf lsf2';
        symbolIcon = 'checkbox';
      }
      else if (result === 'unvoted') {
        newValue = curValue - 1;
        iconClasses = 'lsf';
        symbolIcon = 'check';
      }

      $symbol.html(symbolIcon);
      if (isNaN(newValue)) {
        newValue = '';
      }
      $buttons.html('' + newValue +' <i class="' + iconClasses + '"></i>');
    });
  });
}(jQuery));
