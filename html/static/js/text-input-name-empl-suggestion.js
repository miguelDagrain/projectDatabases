/*
 * functie die een request stuurt om suggesties te kunnen ontvangen
 */
function giveNameSuggestions(elemInput, elemDropdown) {

    $.getJSON($SCRIPT_ROOT + "/check/empl_names", {
        letters: $(elemInput).val()
        },
        function(data){
            $(elemDropdown).removeClass('dropdown-hide');
            $.each(data, function(index, value){
                var dropdownItem = document.createElement('div');
                dropdownItem.innerHTML = value;
                $(dropdownItem).bind('click', function (event) {
                    event.preventDefault();

                    elemInput.innerHTML = dropdownItem.innerHTML;

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
        $(elemDropdown).empty();
        giveNameSuggestions(this, elemDropdown);
    })

    $(elemInput).bind('blur', function () {
        $(elemDropdown).empty();
        $(elemDropdown).addClass('dropdown-hide');
    })
}
