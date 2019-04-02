/* functie die request stuurt naar de url en als die true teruggeeft dan wordt de input geaccepteerd anders gewijgerd. */
function setUpOnlyAcceptLimited(elemInput, addButton, url) {

    $(addButton).bind('click', function () {
        $.getJSON($SCRIPT_ROOT + url,
            { input: $(elemInput).val() },
            function (data) {
                if(data === true){
                    $(addButton).trigger('acceptAndAdd');
                }else{
                    alert('invalid input');
                }
            });

    })
}
