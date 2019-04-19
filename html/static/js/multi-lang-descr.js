function setUpMultilangInput() {
    var clicked = document.createElement('span');
    $(clicked).css({'display':'none'});
    clicked.innerHTML = 'nl';
    $('#multi-language-desc-buttons').append(clicked);

    var nlButton = document.createElement('button');
    $(nlButton).attr({'type':'button'});
    $(nlButton).addClass('language-button');
    $(nlButton).addClass('selected-language-button');
    nlButton.innerHTML = 'nl';

    var nlDesc = document.createElement('div');
    $(nlDesc).css({'display':'none'});

    var nlUploads = document.createElement('ul');
    $(nlUploads).css({'display':'none'});

    $("#multi-language-desc-buttons").append(nlButton);
    $("#multi-language-desc-buttons").append(nlDesc);
    $("#multi-language-desc-buttons").append(nlUploads);

    var engButton = document.createElement('button');
    $(engButton).attr({'type':'button'});
    $(engButton).addClass('language-button');
    engButton.innerHTML = 'eng';

    var engDesc = document.createElement('div');
    $(engDesc).css({'display':'none'});

    var engUploads = document.createElement('ul');
    $(engUploads).css({'display':'none'});

    $("#multi-language-desc-buttons").append(engButton);
    $("#multi-language-desc-buttons").append(engDesc);
    $("#multi-language-desc-buttons").append(engUploads);

    $(nlButton).bind('click', function () {
        var lastLang = $('#multi-language-desc-buttons').children()[0].innerHTML;
        if(lastLang === 'en') {
            var textToSafe = $('#administration-form-description').val();

            $("#multi-language-desc-buttons").children()[5].innerHTML = textToSafe;
            $($("#multi-language-desc-buttons").children()[4]).removeClass('selected-language-button');

            $($("#multi-language-desc-buttons").children()[1]).addClass('selected-language-button');
            tinyMCE.get('administration-form-description').setContent($("#multi-language-desc-buttons").children()[2].innerHTML);
            //we slaan de tekst nog op anders wordt die niet teruggegeven bij val()
            tinyMCE.triggerSave();

            $("#administration-form-upload").children('li').each(function () {
                $($("#multi-language-desc-buttons").children()[6]).append(this);
            });

            $($("#multi-language-desc-buttons").children()[3]).children('li').each(function () {
                $("#administration-form-upload").append(this);
            });

            $('#multi-language-desc-buttons').children()[0].innerHTML = 'nl';
        }
    });

    $(engButton).bind('click', function () {
        var lastLang = $('#multi-language-desc-buttons').children()[0].innerHTML;
        if(lastLang === 'nl'){
            var textToSafe = $('#administration-form-description').val();

            $("#multi-language-desc-buttons").children()[2].innerHTML = textToSafe;
            $($("#multi-language-desc-buttons").children()[1]).removeClass('selected-language-button');

            $($("#multi-language-desc-buttons").children()[4]).addClass('selected-language-button');
            tinyMCE.get('administration-form-description').setContent($("#multi-language-desc-buttons").children()[5].innerHTML);
            //we slaan de tekst nog op anders wordt die niet teruggegeven bij val()
            tinyMCE.triggerSave();

            $("#administration-form-upload").children('li').each(function () {
                $($("#multi-language-desc-buttons").children()[3]).append(this);
            });

            $($("#multi-language-desc-buttons").children()[6]).children('li').each(function () {
               $("#administration-form-upload").append(this);
            });

            $('#multi-language-desc-buttons').children()[0].innerHTML = 'en';
        }
    })
}