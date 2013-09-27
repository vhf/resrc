jQuery(document).ready(function() {
  // Enable Hallo editor
  jQuery('.editable').hallo({
    plugins: {},
    toolbar: 'halloToolbarFixed'
  });

  var markdownize = function(content) {
    var html = content.split("\n").map($.trim).filter(function(line) {
      return line !== "";
    }).join("\n");

    return toMarkdown(html);
  };

  var ext = {};
  if (typeof Showdown.extensions['resrc'] !== "undefined")
    ext = {
      extensions: ['resrc']
    };

  var converter = new Showdown.converter(ext);

  var htmlize = function(content) {
    return converter.makeHtml(content);
  };

  // Method that converts the HTML contents to Markdown
  var showSource = function(content) {
    var markdown = markdownize(content);
    if (jQuery('#id_mdcontent').get(0).value == markdown) {
      return;
    }
    jQuery('#id_mdcontent').get(0).value = markdown;
  };

  var adapt = function() {
    var mdcontent = jQuery('#id_mdcontent');
    var lines = mdcontent.get(0).value.split("\n").length;
    mdcontent.height(lines * 20 + 10);
  };

  var updateHtml = function(content) {
    if (markdownize(jQuery('.editable').html()) == content) {
      return;
    }
    var html = htmlize(content);
    jQuery('.editable').html(html);
    $('.editable').find('a').each(function(index, item) {
      $item = $(item);
      if ($item.text() === 'link') {
        $item.addClass('lsf symbol').css('color', 'black');
      }
    });
  };

  // Update Markdown every time content is modified
  jQuery('.editable').bind('hallomodified', function(event, data) {
    showSource(data.content);
  });
  jQuery('#id_mdcontent').bind('keyup', function() {
    updateHtml(this.value);
    adapt();
  });
  showSource(jQuery('.editable').html());
  adapt();
});
