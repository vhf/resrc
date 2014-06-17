
$(function () {
  "use strict";

  var VOTED_CLASS = 'fi-checkbox';
  var UNVOTED_CLASS = 'fi-check';

  $('#vote, .votes, .arrow-up').click(function() {
    var $this = $(this);
    var itemType = $this.attr('data-type');
    var itemId = $this.attr('data-id');

    // Upper-right button on single link/list page
    var $bigButtonsIcon = $('#vote i');
    // Yellow buttons on the page
    var $buttons = $(
      '.votes[data-id="' + itemId + '"][data-type="' + itemType + '"]'
    );
    var $buttonsIcon = $buttons.find('i');

    var $icons = $buttonsIcon.add($bigButtonsIcon);
    var $votesCounts = $buttons.find('.votes-count');

    // TODO: use django's url function
    var voteUrl = '/' + itemType + '/' + itemId +'/upvote';

    $.ajax({
      type: 'POST',
      url: voteUrl,
      data: 'csrfmiddlewaretoken=' + window.csrfToken
    }).always(function (xhr) {  // TODO: always ? really ?
      var result = $.parseJSON(xhr.responseText).result,
          curVotesCount = parseInt($votesCounts.eq(0).text(), 10),
          newVotesCount;

      if (isNaN(curVotesCount)) {  // no n. of votes displayed on the page
          newVotesCount = '';
      }
      else if (result === 'voted') {
          newVotesCount = curVotesCount + 1;
      }
      else if (result === 'unvoted') {
          newVotesCount = curVotesCount - 1;
      }

      $icons.toggleClass(VOTED_CLASS);
      $icons.toggleClass(UNVOTED_CLASS);
      $votesCounts.text(' ' + newVotesCount + ' ');
    });
  });

  $('.votes').hover(function() {
    var $icon = $(this).find('i').eq(0);
    var $count = $(this).find('span.votes-count').eq(0);
    if($icon.hasClass('fi-check')) {
      $count.html(parseInt($count.html(), 10)+1+' ');
    } else {
      $count.html(parseInt($count.html(), 10)-1+' ');
    }
    $icon.toggleClass(VOTED_CLASS);
    $icon.toggleClass(UNVOTED_CLASS);
  }, function() {
    var $icon = $(this).find('i').eq(0);
    var $count = $(this).find('span.votes-count').eq(0);
    if($icon.hasClass('fi-check')) {
      $count.html(parseInt($count.html(), 10)+1+' ');
    } else {
      $count.html(parseInt($count.html(), 10)-1+' ');
    }
    $icon.toggleClass(VOTED_CLASS);
    $icon.toggleClass(UNVOTED_CLASS);
  });
}(jQuery));
