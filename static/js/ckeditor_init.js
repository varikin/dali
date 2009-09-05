$(document).ready(function() {
  CKEDITOR.replace('id_body', {
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
      ['Maximize', 'ShowBlocks']
    ]
  });
  $('label[for="id_body"]').hide();
});
  