tinymce.init({
    selector: "textarea.tinymce",

    setup: function (editor) {
        editor.on('change', function () {
            tinymce.triggerSave();
        });
    },

    theme: "silver",
    skin: "oxide",
    width: "100%",
    height: "100%"
});