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

function editHomepage(){

    console.log("send");

    var request = $.ajax({
        type: "POST",
        url: $SCRIPT_ROOT + '/home/',
        data: formData,
        dataType: 'json',
        processData: false,
        contentType: false
    });

    request.done(function (data){
        if(data.result){ //check if true is returned
            window.location.replace($SCRIPT_ROOT + '/home/'); //this wil call the get
        }
    });

}



function setupFormEditHomepage() {
    $('#aedit-home-form').bind('submit', function (event) {
        event.preventDefault();
        editHomepage();
        $(this).modal('hide');
    });
}