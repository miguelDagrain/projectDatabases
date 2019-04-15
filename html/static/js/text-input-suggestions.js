/*
 * functie die een request stuurt om name suggesties te kunnen ontvangen
 */
function giveSuggestions(elemInput, elemDropdown, url) {

    $.getJSON($SCRIPT_ROOT + url, {
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
function setUpSuggestions(elemInput, elemDropdown, url) {

    $(elemInput).bind('input', function(){
        giveSuggestions(this, elemDropdown, url);
    });
}