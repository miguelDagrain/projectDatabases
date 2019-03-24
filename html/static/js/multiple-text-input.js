function setUpMultipleTextInput() {
    var multiTextInputs = $('.multi-text-input');

    //itereer over alle textvakken waar we meerdere inputs kunnen geven
    for(var multiTextInputIter = 0; multiTextInputIter < multiTextInputs.length; multiTextInputIter++){
        var multiTextInput = multiTextInputs[multiTextInputIter];

        //neem de al bestaande elementen (deze moeten aanwezig zijn)
        var addButton = multiTextInput.getElementsByTagName('button')[0];

        $(addButton).attr("type", "button");

        //creeer een element waarin we de al ingevoerde elementen weergeven
        var selected = document.createElement('div');
        $(selected).css({"width":"100%", "display":"block"});
        multiTextInput.appendChild(selected);

        $(addButton).bind("click", function(){
            var input = this.parentElement.getElementsByTagName('input')[0];

            var newItem = document.createElement('div');
            newItem.innerHTML = $(input).val();

            var list = this.parentElement.parentElement.getElementsByTagName('div')[1];
            list.appendChild(newItem);
        });

    }
}