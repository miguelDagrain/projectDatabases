/**
 * deze js zal er voor zorgen dat we meerdere inputs kunnen geven bij een texinput met add button
 */
function setUpMultipleTextInput() {
    var multiTextInputs = $('.multi-text-input');

    //itereer over alle textvakken waar we meerdere inputs kunnen geven
    for(var multiTextInputIter = 0; multiTextInputIter < multiTextInputs.length; multiTextInputIter++){
        var multiTextInput = multiTextInputs[multiTextInputIter];

        //neem de al bestaande elementen (deze moeten aanwezig zijn)
        var addButton = multiTextInput.getElementsByClassName('input-block')[0].getElementsByTagName('button')[0];

        $(addButton).attr({'type':"button"});

        //creeer een element waarin we de al ingevoerde elementen weergeven
        var selected = document.createElement('div');
        $(selected).addClass('given-input-block');
        multiTextInput.appendChild(selected);

        $(addButton).bind("acceptAndAdd", function(){

            var newItem = document.createElement('div');
            $(newItem).css({'display':'inline-block', 'color':'#003366', 'background-color':'rgba(255, 255, 255, 0.8)',
                            'border':'1px solid #ffffff', 'border-radius':'4px', 'margin-right':'5px', 'margin-bottom':'4px'});


            var input = this.parentElement.getElementsByTagName('input')[0];
            var valueListItem = document.createElement('span');
            valueListItem.innerHTML = $(input).val();

            newItem.appendChild(valueListItem);

            var removeButton = document.createElement('button');
            $(removeButton).attr({'type':'button'});
            $(removeButton).css({'margin-left':'4px', 'background-color':'rgba(255, 255, 255, 0)',
                                'border':'none'});

            $(removeButton).bind('click', function () {
                this.parentElement.remove();
            });

            var logoButton = document.createElement('img');
            $(logoButton).attr({'src':'/static/image/delete1.png', 'alt':'remove'});
            $(logoButton).css({'border':'1px solid #003366', 'border-radius':'50%'});

            removeButton.appendChild(logoButton);
            newItem.appendChild(removeButton);

            this.parentElement.parentElement.getElementsByClassName('given-input-block')[0].appendChild(newItem);
        });

    }
}

/**
 * standaard functie om add button click te initialiseren, het kan soms handig zijn om een eigen specifieke functie te
 * schrijven in plaats van deze te gebruiken
 */
function standardConnectAddClick(addButton) {
    $(addButton).bind('click', function () {
        $(addButton).trigger('acceptAndAdd');
    });
}
