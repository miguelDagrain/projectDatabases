var formData = new FormData();

function sendMessage() {
   formData.append('Message', $('#administration-form-message').val());

    var request = $.ajax({
        type: "POST",
        url: $SCRIPT_ROOT + '/showInterest/',
        data: formData,
        dataType: 'json',
        processData: false,
        contentType: false
    });

}

function setupFormSendMessage() {
    $('#show-interest-form').bind('submit', function (event) {
            event.preventDefault();
            sendMessage();
            $(this).modal('hide');
    });
}