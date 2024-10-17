var $elements = $('.hidden');
$elements.each(function(i) {
  let el = this;
  setTimeout(function() {
    $(el).css("opacity", 1);
  }, 1000 * i);
  });
