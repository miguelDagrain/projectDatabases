
tinymce.init({
    selector: "textarea.tinymce",

    setup: function (editor) {
        editor.on('change', function () {
            tinymce.triggerSave();
        });

    },

    schema: "html4",
    plugins: "link code",
    menubar: 'file edit insert view format table tools help ',
    menu: {
        insert: { title: "insert", items: "link linktofile" }
    },

        setup: function (editor) {

            var openDialog = function () {

                var files = document.getElementById("administration-form-upload").firstChild;

                var myListItems = [];

                while (files != null){
                    myListItems.push(files.innerHTML.toString());
                    files = files.nextSibling;
                }

                var itemss = [];
                tinymce.each(myListItems, function (myListItemName) {
                    itemss.push({
                        text: myListItemName,
                        value: myListItemName
                    });
                });


                return editor.windowManager.open({
                    title: 'Example plugin',
                    body: {
                        type: 'panel',
                        items: [
                            {
                                type: 'selectbox',
                                name: 'title',
                                label: 'Title',
                                items: itemss
                            },
                            {
                                type: 'input',
                                name: 'Text',
                                label: 'Text to display'
                            }
                        ]
                    },
                    buttons: [
                        {
                            type: 'cancel',
                            text: 'Close'
                        },
                        {
                            type: 'submit',
                            text: 'Save',
                            primary: true
                        }
                    ],
                    onSubmit: function (api) {
                        var data = api.getData();
                        // Insert content when the window form is submitted

                        var a = document.createElement("a");

                        if (dl === "../download/"){

                            var t = document.getElementById("administration-form-title").value.toString();

                            a.href= dl + t + "_" + data.title;
                        }else{
                            a.href= dl + data.title;
                        }

                        a.appendChild(document.createTextNode(data.Text));

                        editor.insertContent(a.outerHTML.toString());
                        api.close();
                    }
                });

            };

            editor.ui.registry.addMenuItem('linktofile', {
                text: 'link to file',
                icon: 'link',
                onAction: function () {
                    // Open window
                    openDialog();

                }
            });

        },

    theme: "silver",
    skin: "oxide",
    width: "100%",
    height: "100%",

});

// Prevent Bootstrap dialog from blocking focusin
$(document).on('focusin', function(e) {
    if ($(e.target).closest(".mce-window").length) {
        e.stopImmediatePropagation();
    }
});