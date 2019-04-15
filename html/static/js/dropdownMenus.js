/**
 *  Deze js zal er voor zorgen dat elke <select> en <option>'s beschreven worden door <div> en <div>'s
 *  omdat het laatste nu eenmaal makkelijker opmaakbaar is met css dan <option>'s.
 *  (dewelke eigenlijk niet kunnen opgemaakt worden met css).
 **/
function setUpDropdowns() {

    var dropdowns = document.getElementsByClassName("dropdown");
    for (iter = 0; iter < dropdowns.length; iter++) { //we doen dit voor elke dropdown
        var selector = dropdowns[iter].getElementsByTagName("select")[0]; //we gaan ervan uit dat er maar een select per dropdown is
        var selected = document.createElement("div");
        selected.setAttribute("class", "dropdown-selected");
        selected.innerHTML = selector.options[selector.selectedIndex].innerHTML; //zet de inner-html naar de html van de geselecteerde optie
        dropdowns[iter].appendChild(selected); //voeg het nieuwe element toe in de overkoepelende klasse van de selector

        //voor de lijst met elementen:
        var possibleSelection = document.createElement("div");
        possibleSelection.setAttribute("class", "dropdown-items dropdown-hide"); //dit element en zijn subelementen zullen dus niet zichtbaar zijn

        dropdowns[iter].appendChild(possibleSelection); //voeg de lijst toe aan het blok

        //maak de subelementen aan
        for (iterElems = 0; iterElems < selector.length; iterElems++) {

            var optionalElem = document.createElement("div");
            optionalElem.innerHTML = selector.options[iterElems].innerHTML;
            optionalElem.onchange = selector.onchange;
            possibleSelection.appendChild(optionalElem); //voeg de optie toe
            optionalElem.addEventListener("click", function (evt) {

                // this = div (optie) -> parent = div (menu) -> parent = div (overkoepelend met <select>), heeft maar een <select>
                var selectBlock = this.parentNode.parentNode.getElementsByTagName("select")[0];

                // this = div (optie) -> parent = div (menu) -> previousSibling = div (box met selected)
                var clickableBox = this.parentNode.previousSibling;

                for (iterOpties = 0; iterOpties < selectBlock.length; iterOpties++) {
                    if (selectBlock.options[iterOpties].innerHTML === this.innerHTML) {
                        selectBlock.selectedIndex = iterOpties; //we selecteren de correcte optie
                        clickableBox.innerHTML = this.innerHTML; //we passen de inhoud van de box aan
                        break;
                    }
                }

                this.onchange();
                clickableBox.click();//we sluiten zo het menu
            }); //geef de mogelijkheid om deze optie te selecteren
        }

        //Nu moet men nog de mogeljjkheid krijgen om het selectiemenu te openen
        selected.addEventListener("click", function (evt)
        {

            closeAllSelected(this); //sluit alle menu's behalve deze

            //onderstaande code: neem de volgende object in de DOM structuur, neem daarvan
            //de lijst van klassen, en schakel de klasse dropdown-hide aan of uit (switch-knop).
            this.nextSibling.classList.toggle("dropdown-hide");

            evt.preventDefault();
            evt.stopPropagation();
        });


    }
}
/* Deze code is zeer sterk gebaseerd op degene uit https://www.w3schools.com/howto/howto_custom_select.asp */