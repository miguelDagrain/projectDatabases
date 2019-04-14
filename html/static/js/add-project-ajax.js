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

function addProject() {

    var promotorsInput = document.getElementById('Promotors').getElementsByClassName('given-input-block')[0];
    for (var iter = 0; iter < promotorsInput.childElementCount; iter++)
    {
        formData.append('Promotor', promotorsInput.children[iter].getElementsByTagName('span')[0].innerHTML)
    }


    var tagsInput = document.getElementById('Tags').getElementsByClassName('given-input-block')[0];
    for (var iter = 0; iter < tagsInput.childElementCount; iter++){
        formData.append('Tags', tagsInput.children[iter].getElementsByTagName('span')[0].innerHTML)
    }


    var relatedInput = document.getElementById('Related').getElementsByClassName('given-input-block')[0];
    for (var iter = 0; iter < relatedInput.childElementCount; iter++) {
        formData.append('Related', relatedInput.children[iter].getElementsByTagName('span')[0].innerHTML)
    }


    for (var iter = 0; iter < document.getElementById('administration-form-researchgroup').options.length; ++iter) {
        var groupOption = document.getElementById('administration-form-researchgroup').options[iter];

        if(groupOption.selected){
            formData.append('Researchgroup', $(groupOption).val().toString(10));
        }
    }


    for (var iter = 0; iter < document.getElementById('administration-form-type').options.length; ++iter) {
        var typeOption =  document.getElementById('administration-form-type').options[iter];

        if(typeOption.selected){
            formData.append('Type', $(typeOption).val().toString(10));
        }
    }


    for (var iter = 0; iter < document.getElementById('administration-form-discipline').options.length; ++iter) {
        var disciplineOption = document.getElementById('administration-form-discipline').options[iter];

        if(disciplineOption.selected){
            formData.append('Discipline', $(disciplineOption).val().toString(10));
        }
    }

    formData.append('Title', $('#administration-form-title').val());
    formData.append('Maxstudents', $('#administration-form-max').val().toString(10));
    formData.append('Description', $('#administration-form-description').val());

    var request = $.ajax({
        type: "POST",
        url: $SCRIPT_ROOT + '/projects/',
        data: formData,
        dataType: 'json',
        processData: false,
        contentType: false
    });

    request.done(function (data){
        if(data.result){ //check if true is returned
            window.location.replace($SCRIPT_ROOT + '/projects'); //this wil call the get
        }
    });

}

function setupFormAddProject() {
    $('#add-project-form').bind('submit', function (event) {
        event.preventDefault();
        addProject();
        $(this).modal('hide');
    });
}