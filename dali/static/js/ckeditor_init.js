var ck = {
  config : {
    filebrowserImageBrowseUrl : '/gallery/choose_picture/',
    toolbar:  [
      ['Cut','Copy','Paste','PasteText','PasteFromWord','-', 'SpellChecker', 'Scayt'],
      ['Undo','Redo','-','Find','Replace','-','SelectAll','RemoveFormat'],
      ['Link','Unlink','Anchor', 'Image'],
      ['HorizontalRule','Smiley','SpecialChar','PageBreak'],
      '/',
      ['Bold','Italic','Underline','Strike','-','Subscript','Superscript'],
      ['NumberedList','BulletedList','-','Outdent','Indent','Blockquote'],
      ['JustifyLeft','JustifyCenter','JustifyRight','JustifyBlock'],
      '/',
      ['Styles','Format','Font','FontSize'],
      ['TextColor','BGColor'],
      ['Maximize', 'ShowBlocks', 'Source']
    ]
  }
};

$(document).ready(function() {
  $.each(['id_body', 'id_content', 'id_description'], function(index, element) {
    if($('#' + element).length > 0) {
      $('label[for="' + element + '"]').hide();
      CKEDITOR.replace(element, ck.config);
    }
  });
});
  