function addProject() {

    var promotorsInput = document.getElementById('Promotors').getElementsByClassName('given-input-block')[0];
    var promotorsArray = [];
    for (var iter = 0; iter < promotorsInput.childElementCount; iter++)
    {
        promotorsArray.push(promotorsInput.children[iter].getElementsByTagName('span')[0].innerHTML)
    }


    var tagsInput = document.getElementById('Tags').getElementsByClassName('given-input-block')[0];
    var tagsArray = [];
    for (var iter = 0; iter < tagsInput.childElementCount; iter++){
        tagsArray.push(tagsInput.children[iter].getElementsByTagName('span')[0].innerHTML)
    }


    var relatedInput = document.getElementById('Related').getElementsByClassName('given-input-block')[0];
    var relatedArray = [];
    for (var iter = 0; iter < relatedInput.childElementCount; iter++) {
        relatedArray.push(relatedInput.children[iter].getElementsByTagName('span')[0].innerHTML)
    }


    var groupArray = [];
    for (var iter = 0; iter < document.getElementById('administration-form-researchgroup').options.length; ++iter) {
        var groupOption = document.getElementById('administration-form-researchgroup').options[iter];

        if(groupOption.selected){
            groupArray.push($(groupOption).val());
        }
    }


    var typeArray = [];
    for (var iter = 0; iter < document.getElementById('administration-form-type').options.length; ++iter) {
        var typeOption =  document.getElementById('administration-form-type').options[iter];

        if(typeOption.selected){
            typeArray.push($(typeOption).val());
        }
    }


    var disciplineArray = [];
    for (var iter = 0; iter < document.getElementById('administration-form-discipline').options.length; ++iter) {
        var disciplineOption = document.getElementById('administration-form-discipline').options[iter];

        if(disciplineOption.selected){
            disciplineArray.push($(disciplineOption).val());
        }
    }

    var title =  $('#administration-form-title').val();
    var max = $('#administration-form-max').val();
    var desc = $('#administration-form-description').val();

    var request = $.ajax({
        type: "POST",
        url: $SCRIPT_ROOT + '/projects/',
        data: JSON.stringify({
            Title: title, //string
            Maxstudents: max, //int
            Researchgroup: groupArray, //array (omwillle van select met multiple attribute)
            Description: desc, //string
            Type: typeArray, //array (omwille van select met multiple attribute)
            Discipline: disciplineArray, //array (omwille van select met multiple attribute)
            Promotors: promotorsArray, //array
            Tags: tagsArray, //array
            Related: relatedArray //array
        }),
        contentType: 'application/json;charset=UTF-8'
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
        $(this).attr('disabled', true);
    });
}