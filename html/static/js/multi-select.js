/**
 * deze js zal er voor zorgen dat we meerdere keuzes kunnen maken uit een dropdownmenu
 */
function setUpMultiSelection() {
    var multiSelectors = document.getElementsByClassName("multi-select");

    for(var nrSelector = 0; nrSelector < multiSelectors.length; nrSelector++){
        var selector = multiSelectors[nrSelector];
        var selectMain = selector.getElementsByTagName("select")[0];

        //maak button
        var button = document.createElement("div");
        button.setAttribute("class", "multi-select-button");
        button.innerHTML = "_('All')";
        selector.appendChild(button);

        //maak een menu
        var menu = document.createElement("div");
        menu.setAttribute("class", "multi-select-items multi-select-hide");
        selector.appendChild(menu);

        //voeg het All item toe
        var allOption = document.createElement("div");
        allOption.setAttribute("class", "multi-select-all multi-select-items-not-selected");
        allOption.innerHTML = selectMain.options[0].innerHTML;
        allOption.onchange = selectMain.onchange;
        //maak het mogelijk om alle opties ineens te selecteren
        allOption.addEventListener("click", function (evt) {
             evt.preventDefault();
             evt.stopPropagation();

             var select = this.parentElement.parentElement.getElementsByTagName("select")[0];

             if($(this).hasClass("multi-select-items-not-selected")) {

                 for (var nrSelect = 0; nrSelect < select.length; nrSelect++) {
                     select.options[nrSelect].setAttribute("selected", "selected");
                 }

                 var selectedItems = this.parentElement.getElementsByClassName("multi-select-items-selected");
                 for (var selectSibling = 0; selectSibling < selectedItems.length; selectSibling) {
                     (selectedItems[selectSibling]).classList.add("multi-select-items-not-selected");
                     (selectedItems[selectSibling]).classList.remove("multi-select-items-selected");
                 }

                 this.classList.remove("multi-select-items-not-selected");
                 this.classList.add("multi-select-items-selected");

                  this.parentElement.previousElementSibling.innerHTML = "All";
             }else{

                 for (var nrSelect = 0; nrSelect < select.length; nrSelect++) {
                     select.options[nrSelect].removeAttribute("selected");
                 }


                 this.classList.remove("multi-select-items-selected");
                 this.classList.add("multi-select-items-not-selected");

                 this.parentElement.previousElementSibling.innerHTML = "None";
             }
            this.onchange();

        });

        menu.appendChild(allOption);
        //allOption.click();
        allOption.classList.remove("multi-select-items-not-selected");
        allOption.classList.add("multi-select-items-selected");
        allOption.parentElement.previousElementSibling.innerHTML = "All";

        //voeg voor elke optie een niet geselecteerd item toe met eventlistener, en verberg deze
        for(var nrSelect = 1; nrSelect < selectMain.length; nrSelect++){
            var newItem =  document.createElement("div");
            newItem.setAttribute("class", "multi-select-items-not-selected");
            newItem.onchange = selectMain.onchange;
            newItem.innerHTML = selectMain.options[nrSelect].innerHTML;



            //voeg de mogelijkheid toe om item te selecteren
            newItem.addEventListener("click", function (evt) {
                evt.preventDefault();
                evt.stopPropagation();

                var allOption = this.parentElement.getElementsByClassName("multi-select-all")[0];

                var select = this.parentElement.parentElement.getElementsByTagName("select")[0];

                if($(allOption).hasClass("multi-select-items-selected")){
                    allOption.classList.remove("multi-select-items-selected");
                    allOption.classList.add("multi-select-items-not-selected");

                    for(var nrSelect = 0; nrSelect < select.length; nrSelect++){
                        if(select.options[nrSelect].innerHTML === this.innerHTML){
                            continue;
                        }
                        select.options[nrSelect].toggleAttribute("selected");
                    }

                    this.parentElement.previousElementSibling.innerHTML = "Selection"
                }else{
                    var anySelected = false;

                    for(var nrSelect = 0; nrSelect < select.length; nrSelect++){
                        if(select.options[nrSelect].getAttribute("selected")){
                            anySelected = true;
                        }

                        if(select.options[nrSelect].innerHTML === this.innerHTML){
                            select.options[nrSelect].toggleAttribute("selected");

                        }
                    }

                    if(anySelected === false && $(this).hasClass("multi-select-items-not-selected")){
                        this.parentElement.previousElementSibling.innerHTML = "Selection"
                    }else if(anySelected === false && $(this).hasClass("multi-select-items-selected")){
                        this.parentElement.previousElementSibling.innerHTML = "None"
                    }
                }


                if($(this).hasClass("multi-select-items-not-selected")){
                    this.classList.remove("multi-select-items-not-selected");
                    this.classList.add("class", "multi-select-items-selected");
                } else {
                    this.classList.remove("multi-select-items-selected");
                    this.classList.add("class", "multi-select-items-not-selected");
                }

                this.onchange();

            });

            menu.appendChild(newItem);
        }

        //voeg aan button een eventlistener toe
        button.addEventListener("click", function (evt) {
           evt.preventDefault();
           evt.stopPropagation();

           closeAllSelected(this);
           this.nextSibling.classList.toggle("multi-select-hide");

        });

        allOption.click(); // zorg ervoor dat de all wordt geklikt (dit deselecteert all in de opties die we presenteren maar verandert nog niets aan de select)
        allOption.click(); // selecteer alle items om te beginnen (in de select worden de items nu ook geselecteerd)
    }
}