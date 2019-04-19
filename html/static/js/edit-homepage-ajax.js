var formData = new FormData();

function handleUploadAttachementDrop (event) {

    //prevent file from being opened
    event.preventDefault();

    if(event.dataTransfer.items){
        for (var it = 0; it < event.dataTransfer.items.length; it++) {
            if(event.dataTransfer.items[it].kind === 'file') {
                var file = event.dataTransfer.items[it].getAsFile();

                window.formData.append('Attachments', file);

                var listItem = "<li>" + file.name + "</li>";

                $('#administration-form-upload').append(listItem);
            }
        }

    }else {
        for (var it = 0; it < ev.dataTransfer.files.length; it++) {
            window.formData.append('Attachments', event.dataTransfer.files[it]);

            var listItem = "<li>" +  event.dataTransfer.files[it].name + "</li>";
            $('#administration-form-upload').append(listItem);
        }
    }

}

function handleUploadAttachementOver (event) {
    //prevent file from being opened
    event.preventDefault();
}

