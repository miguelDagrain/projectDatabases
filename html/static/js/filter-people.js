
function countOccurances(str, search){
    if (search.length <1){
        return 0;
    }
    return (str.match( new RegExp(search, "i")) || []).length;
}


function filterPeople(){

    var searchQ = document.getElementById("SQInput").value;

    // Init
    result = [];
    var sq = searchQ.trim();
    var tokens = sq.split(" ");
    if (sq.length === 0){
        tokens = []
    }

    for (var i in peopleList ){
        peopleList[i].relevance = 0;
            for (var t in tokens){
            if (countOccurances(peopleList[i]["name"], tokens[t]) > 0) {
                peopleList[i].relevance += 1;
            }
        }
    }

    var rg = document.getElementById("research_group");
    var prom = document.getElementById("promotor");

    for (var i in peopleList ){
        if (peopleList[i].relevance > 0 || sq.length === 0 ) {
            if (rg.options[rg.selectedIndex].text === peopleList[i]["group"] || rg.selectedIndex === 0 ){
                switch (prom.selectedIndex){
                    case 0 :
                        result.push(peopleList[i]);
                        break;
                    case 1 :
                        if (peopleList[i]["promotor"]){
                            result.push(peopleList[i]);
                        }
                        break;
                    case 2:
                        if (!peopleList[i]["promotor"]){
                            result.push(peopleList[i]);
                        }
                        break;
                }
            }

        }

    }

    result.sort(function(a, b){return b.relevance - a.relevance});

    // Update page content
    var tableList = document.getElementById("people_table");
    tableList.innerHTML = tableList.children[0].innerHTML;

    peopleCount = 0;
    showMorePeople(sq);

}

function showMorePeople(sq){

    var tableList = document.getElementById("people_table");
    var pCont = document.createElement("tbody");

    for (var i = peopleCount; i < peopleCount + 20; i++) {
        if (result.length <= i){break;}
        if ((result[i].relevance === 0 && sq.length > 0 || result[i].relevance === -1 )){break;}

        var cont = document.createElement("tr");

        var name = document.createElement("td");
        var link = document.createElement("a");
        link.appendChild(document.createTextNode(result[i]["name"]));
        link.href = "/people/" + result[i]["ID"];
        name.appendChild(link);
        cont.appendChild(name);

        var rg = document.createElement("td");
        rg.appendChild(document.createTextNode(result[i]["group"]));
        cont.appendChild(rg);

        var promotor = document.createElement("td");

        if (result[i]["promotor"]) {
            promotor.appendChild(document.createTextNode("\n" +
                "                    \n" +
                "                        ✔\n" +
                "                    \n" +
                "                "));

        }else{
            promotor.appendChild(document.createTextNode("\n" +
                "                    \n" +
                "                        ❌\n" +
                "                    \n" +
                "                "));
        }
        cont.appendChild(promotor);
        pCont.appendChild(cont);

    }
    tableList.appendChild(pCont);

    peopleCount += 20;

    
}