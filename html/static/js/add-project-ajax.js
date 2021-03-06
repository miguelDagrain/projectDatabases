var formData = new FormData();

function handleUploadAttachementDrop(event) {

    //prevent file from being opened
    event.preventDefault();

    if (event.dataTransfer.items) {
        var currentLang = $('#multi-language-desc-buttons').children()[0].innerHTML;
        for (var it = 0; it < event.dataTransfer.items.length; it++) {
            if (event.dataTransfer.items[it].kind === 'file') {
                var file = event.dataTransfer.items[it].getAsFile();

                if (currentLang === 'nl') {
                    window.formData.append('nlUploads', file);
                } else if (currentLang === 'en') {
                    window.formData.append('engUploads', file);
                }


                var listItem = "<li>" + file.name + "</li>";

                $('#administration-form-upload').append(listItem);
            }
        }

    } else {
        for (var it = 0; it < ev.dataTransfer.files.length; it++) {
            window.formData.append('Attachments', event.dataTransfer.files[it]);

            var listItem = "<li>" + event.dataTransfer.files[it].name + "</li>";
            $('#administration-form-upload').append(listItem);
        }
    }

}


function handleUploadAttachementOver(event) {
    //prevent file from being opened
    event.preventDefault();
}

function addProject() {

    var promotorsInput = document.getElementById('Promotors').getElementsByClassName('given-input-block')[0];
    for (var iter = 0; iter < promotorsInput.childElementCount; iter++) {
        formData.append('Promotors', promotorsInput.children[iter].getElementsByTagName('span')[0].innerHTML)
    }

    var supervisorsInput = document.getElementById('Supervisors').getElementsByClassName('given-input-block')[0];
    for (var iter = 0; iter < supervisorsInput.childElementCount; iter++) {
        formData.append('Supervisors', supervisorsInput.children[iter].getElementsByTagName('span')[0].innerHTML)
    }

    var externInput = document.getElementById('Extern').getElementsByClassName('given-input-block')[0];
    for (var iter = 0; iter < externInput.childElementCount; iter++) {
        formData.append('Extern', externInput.children[iter].getElementsByTagName('span')[0].innerHTML)
    }

    var tagsInput = document.getElementById('Tags').getElementsByClassName('given-input-block')[0];
    for (var iter = 0; iter < tagsInput.childElementCount; iter++) {
        formData.append('Tags', tagsInput.children[iter].getElementsByTagName('span')[0].innerHTML)
    }


    var relatedInput = document.getElementById('Related').getElementsByClassName('given-input-block')[0];
    for (var iter = 0; iter < relatedInput.childElementCount; iter++) {
        formData.append('Related', relatedInput.children[iter].getElementsByTagName('span')[0].innerHTML)
    }


    for (var iter = 0; iter < document.getElementById('administration-form-researchgroup').options.length; ++iter) {
        var groupOption = document.getElementById('administration-form-researchgroup').options[iter];

        if (groupOption.selected) {
            formData.append('Researchgroup', $(groupOption).val().toString(10));
        }
    }


    for (var iter = 0; iter < document.getElementById('administration-form-type').options.length; ++iter) {
        var typeOption = document.getElementById('administration-form-type').options[iter];

        if (typeOption.selected) {
            formData.append('Type', $(typeOption).val().toString(10));
        }
    }


    for (var iter = 0; iter < document.getElementById('administration-form-discipline').options.length; ++iter) {
        var disciplineOption = document.getElementById('administration-form-discipline').options[iter];

        if (disciplineOption.selected) {
            formData.append('Discipline', $(disciplineOption).val().toString(10));
        }
    }

    var nlDesc = $("#nlDesc");
    var engDesc = $("#engDesc");

    var nlButton = $("#nlButton");
    var enButton = $("#enButton");

    nlButton = document.getElementById('nlButton');
    enButton = document.getElementById('enButton');

    formData.append('Title', $('#administration-form-title').val());
    formData.append('Maxstudents', $('#administration-form-max').val().toString(10));

    if ('' === nlDesc.html() && '' === engDesc.html()) {
        enButton.click();
    }

    // To make sure the data is stored, we have to simulate a click on the other button.
    // See code in multi-lang-descr.js line 45-92
    nlButton.click();
    enButton.click();
    nlButton.click();

    formData.append('nlDescription', nlDesc.html());
    formData.append('engDescription', engDesc.html());


    var request = $.ajax({
        type: "POST",
        url: $SCRIPT_ROOT + '/projects/',
        data: formData,
        dataType: 'json',
        processData: false,
        contentType: false
    });

    request.done(function (data) {
        if (data.result) { //check if true is returned
            $('#modal-form-project').modal('hide'); //sluit de modal
            window.location.replace($SCRIPT_ROOT + '/projects'); //this wil call the get, empty inputs of modal
        } else {
            var url = new URL($SCRIPT_ROOT + '/projects');
            url.searchParams.append("error", true);
            console.log(url.toString());
            window.location.replace(url.toString());
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

$(document).ready(function () {
    $('#add-project-form').submit(function () {
        $('#submit-btn').attr("disabled", true);
    });
});