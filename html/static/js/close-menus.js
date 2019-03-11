/**
 * @brief: functie die alle menu's die momenteel openstaan sluit
 */
function closeAllSelected(clickedBox) {
    var menus = document.getElementsByClassName("dropdown-items");
    var entrees = document.getElementsByClassName("dropdown-selected");


    //controleer welke elementen verschuild moeten worden
    for(iterMenu = 0; iterMenu < menus.length; ++iterMenu){
        if(clickedBox !== entrees[iterMenu]){
            menus[iterMenu].classList.add("dropdown-hide");
        }
    }


    menus = document.getElementsByClassName("multi-select-items");
    entrees = document.getElementsByClassName("multi-select-button");

    for(iterMenu = 0; iterMenu < menus.length; ++iterMenu){
        if(clickedBox !== entrees[iterMenu]){
            menus[iterMenu].classList.add("multi-select-hide");
        }
    }
}

// als je buiten de boxen klikt dan sluiten we de boxen
document.addEventListener("click",  function(evt) {

    closeAllSelected(null);
});
