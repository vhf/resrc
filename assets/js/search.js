var _gaq = _gaq || [];

$(function () {
  "use strict";

  var selectizeOptions = {
    openOnFocus: false,
    highlight: true,
    hideSelected: true,
    valueField: 'tag',
    labelField: 'tag',
    searchField: ['tag'],
    options: window.tags,
    onChange: search_tags,
    onInitialize: search_tags
  };

  $('#selected-tags').selectize(selectizeOptions);
  $('#excluded-tags').selectize(selectizeOptions);

  $('input[name="op"]').on('change', search_tags);

  var NProgress = window.NProgress;
  NProgress.configure({ trickleRate: 0.3 });
  $(document).ajaxStart(function () {
    NProgress.start();
  });
  $(document).ajaxStop(function () {
    NProgress.done();
  });

  function search_tags () {
    var op = $('input[name="op"]:checked').val() || 'or',
        selectedTags = $('#selected-tags').val() || '',
        excludedTags = $('#excluded-tags').val() || '',
        url = '/search/' + encodeURIComponent(selectedTags) +'%25' + op + '%25' + encodeURIComponent(excludedTags),
        query = buildQueryString(selectedTags, excludedTags, op);

    if (query.length === 0) {
      $('#query').html('Search by tags');
      $('#results').hide();
    }
    else {
      $('#query').html('<a href="/page' + url + '">' + query + '</a>');

      _gaq.push(['_trackEvent', 'Search', window._gaq_page_name, query]);

      $.ajax({
        type:'GET',
        url: '/tag' + url,
        success: function (result) {
          result = $.parseJSON(result);
          $('#results').show();
          injectResults($('#link_results'), result[0]);
          injectResults($('#list_results'), result[1]);
        }
      });
    }
  }

  function resultLayoutTpl (content) {
    return '<div><h5>' + content + '</h5></div>';
  }

  function resultTpl (index, content) {
    content = index + '. <a href="' + content.url + '">' + content.title + '</a>';
    return resultLayoutTpl(content);
  }

  function injectResults ($element, results) {
    $element.empty();
    if (!results.length) {
      $element.append(resultLayoutTpl('Sorry, no result.'));
    }
    else {
      results.forEach(function (result, index) {
        $element.append(resultTpl(index, result));
      });
    }
  }

  function buildQueryString (selectedTags, excludedTags, operand) {
    var query = '';
    if (selectedTags) {
      var tags = selectedTags.split(',');
      var operandSep = operand === 'and' ? ' & ' : ' | ';
      query += tags.join(operandSep);
    }
    if (excludedTags) {
      var excludes = excludedTags.split(',');
      query += ' ~(';
      query += excludes.join(' | ');
      query += ')';
    }
    return query;
  }

});
