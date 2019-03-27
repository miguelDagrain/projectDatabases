/*
 * functie die een request stuurt om suggesties te kunnen ontvangen
 */
function giveNameSuggestions(elemInput, elemDropdown) {

    $.getJSON($SCRIPT_ROOT + "/check/empl_names", {
        letters: $(elemInput).val()
        },
        function(data){
            $(elemDropdown).empty();
            $(elemDropdown).removeClass('dropdown-hide');
            $.each(data, function(index, value){
                var dropdownItem = document.createElement('div');
                dropdownItem.innerHTML = value;
                $(dropdownItem).bind('click', function (event) {
                    event.preventDefault();

                    $(elemInput).val(this.innerHTML);

                    //leeg het parentelement
                    $(this.parentElement).addClass('dropdown-hide');
                    $(this.parentElement).empty();
                });
                $(elemDropdown).append(dropdownItem);
            })
        });
}

/*
 * functie om een text-input name suggestions te geven
 */
function setUpNameSuggestions(elemInput, elemDropdown) {

    $(elemInput).bind('input', function(){
        giveNameSuggestions(this, elemDropdown);
    });
}

/*
 * functie die er voor zorgt dat enkel namen van onderzoekmedewerkers worden geaccepteerd.
 */
function setUpOnlyAcceptNames(elemInput, addButton) {

    $(addButton).bind('click', function () {
        $.getJSON($SCRIPT_ROOT + "/check/empl_name_correct",
            { name: $(elemInput).val() },
            function (data) {
                if(data === true){
                    $(addButton).trigger('acceptAndAdd');
                }else{
                    alert('invalid name');
                }
            });

    })
}