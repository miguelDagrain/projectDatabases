function addProject(form) {

    var promotorsInput = document.getElementById('Promotors').getElementsByClassName('given-input-block');
    var promotorsArray = [];
    for (var iter = 0; iter < $(promotorsInput).childElementCount; iter++)
    {
        promotorsArray.push(promotorsInput.childNodes[iter].getElementsByTagName('span')[0].innerHTML)
    }


    var tagsInput = document.getElementById('Tags').getElementsByClassName('given-input-block');
    var tagsArray = [];
    for (var iter = 0; iter < $(tagsInput).childElementCount; iter++){
        tagsArray.push(tagsInput.childNodes[iter].getElementsByTagName('span')[0].innerHTML)
    }


    var relatedInput = document.getElementById('Related').getElementsByClassName('given-input-block');
    var relatedArray = [];
    for (var iter = 0; iter < $(relatedInput).childElementCount; iter++) {
        relatedArray.push(relatedInput.childNodes[iter].getElementsByTagName('span')[0].innerHTML)
    }


    $.post($SCRIPT_ROOT + '/projects/',
       {
            Title: $('#administration-form-title').val(), //string
            Maxstudents: $('#administration-form-max').val(), //int
            Researchgroup: $('#administration-form-researchgroup').val(), //array (omwillle van select met multiple attribute)
            Description: $('#administration-form-description').val(), //string
            Type: $('#administration-form-type').val(), //array (omwille van select met multiple attribute)
            Discipline: $('#administration-form-discipline').val(), //array (omwille van select met multiple attribute)
            Promotors: promotorsArray, //array
            Tags: tagsArray, //array
            Related: relatedArray //array
       }
    );

}