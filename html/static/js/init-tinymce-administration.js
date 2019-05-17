tinymce.init({
    selector: "textarea.tinymce",

    setup: function (editor) {
        editor.on('change', function () {
            tinymce.triggerSave();
        });

    },

    schema: "html4",
    plugins: "link code",
    menubar: 'file edit insert view format table tools help',
    menu: {
        insert: { title: "insert", items: "link linktofile" }
    },

    setup: function (editor) {

        editor.ui.registry.addMenuItem('linktofile', {
            text: 'link to file',
            icon: 'link',
            onAction: function () {


                editor.windowManager.open({
                    title: 'Link file',
                    size: 'normal',
                    body: [
                        {
                            title: 'General',
                            type: 'panel',
                            name: 'general'
                        },
                    ],
                    buttons: [{
                        type: 'submit',
                        name: 'save',
                        text: 'Save',
                        primary: true,
                        onclick: function() {
                            // TODO: handle primary btn click
                            (this).parent().parent().close();
                        }
                    },
                        {
                            type: 'cancel',
                            name: 'cancel',
                            text: 'Cancel',
                            onclick: function() {
                                (this).parent().parent().close();
                            }
                        }]

                });

            }
        });

    },

    theme: "silver",
    skin: "oxide",
    width: "100%",
    height: "100%",

});