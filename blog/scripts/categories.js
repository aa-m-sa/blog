
function jq( myid ) {
  return "#" + myid.replace( /(:|\.|\[|\]|,|=)/g, "\\$1" );
}

// clickable show/hide category list
$( document ).ready(function() {
  $( ".archive-tag-area" ).each( function(i, e) {
    var taglist = $( this ).children( ".archive-tag-list" );
    taglist.hide();
    $( this ).children( ".archive-tag-clickable").on( 'click', function(event) {
      taglist.toggle( "show" );
    });
  });
})
