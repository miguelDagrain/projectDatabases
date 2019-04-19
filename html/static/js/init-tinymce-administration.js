tinymce.init({
    selector: "textarea.tinymce",

    setup: function (editor) {
        editor.on('change', function () {
            tinymce.triggerSave();
        });

    },

    plugins: "link code",
    menubar: 'file edit insert view format table tools help',

    theme: "silver",
    skin: "oxide",
    width: "100%",
    height: "100%",

});