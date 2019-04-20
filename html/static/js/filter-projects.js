function countOccurances(str, search){
    if (search.length <1){
        return 0;
    }
    return (str.match( new RegExp(search, "i")) || []).length;
}

function filterProjects(){

    var searchQ = document.getElementById("SQInput").value;

    // Init
    result = [];
    var sq = searchQ.trim();
    var tokens = sq.split(" ");
    if (sq.length == 0){
        tokens = []
    }

    // Count Occurances in Title
    for ( var i in obj){
        obj[i].relevance = 0;
        for( var j in tokens) {
            // Check in title
            if (countOccurances(obj[i].title, tokens[j])) {
                obj[i].relevance++;

            }
        }
    }

    // Count Occurances in Description
    for( var j in tokens) {
        for (var word in wordTable){
            if (countOccurances(word, tokens[j]) > 0){
                //console.log("influenced by:" + word)
                for ( var i in wordTable[word]) {
                    if (i != "total") {
                        var div = (Object.keys(wordTable[word]).length -1);
                        obj[i].relevance += wordTable[word][i] / (wordTable[word]["total"] * div)
                    }

                }
            }
        }
    }

    // Add to the possible projects list
    for (var i in obj){
        if (obj[i].relevance >= 0 || sq.length === 0 ){
            result.push(obj[i])
        }
    }

    var status = document.getElementById("status");
    var rg = document.getElementById("researchGroup");
    var ms = document.getElementsByClassName("multi-select");

    // get selected types
    var selectedTypes = [];
    for(var i = 0; i < ms[0].children[2].children.length; i++){
        if (!ms[0].children[2].children[i].className.includes("not-selected")){
            selectedTypes.push(ms[0].children[2].children[i].textContent);
        }
    }

    // get selected disciplines
    var selectedDisciplines = [];
    for(var i = 0; i < ms[1].children[2].children.length; i++){
        if (!ms[1].children[2].children[i].className.includes("not-selected")){
            selectedDisciplines.push(ms[1].children[2].children[i].textContent);
        }
    }

    /*
    console.log(selectedTypes);
    console.log(selectedDisciplines);
    console.log(rg.options[rg.selectedIndex].text);
    console.log(status.options[status.selectedIndex].text);
    */

    // Weighted relevance for each token
    for ( var i in result){

        // Check discipline
        var discFound = false;
        for (var itt in result[i].type){
            if (!selectedDisciplines.includes(result[i].disciplines[itt]) ){
                continue;
            }
            discFound = true;
            break;
        }
        if (!discFound && !selectedDisciplines.includes("All")){
            result[i].relevance = -1;
            console.log("disc");
            continue;
        }

        // Check type
        var typeFound = false;
        for (var itt in result[i].type){
            if (!selectedTypes.includes(result[i].type[itt]) ){
                continue;
            }
            typeFound = true;
            break;
        }
        if (!typeFound && !selectedTypes.includes("All")){
            result[i].relevance = -1;
            console.log("type");
            continue;
        }

        // Check research group
        var rgFound = false;
        for (var rgn in result[i].researchGroup){
            if (result[i].researchGroup[rgn] === rg.options[rg.selectedIndex].text){
                rgFound = true;
                break;
            }
        }
        if (!rgFound && rg.selectedIndex>0){
            result[i].relevance = -1;
            console.log("rg");
            continue;
        }

        // Check status
        switch (status.selectedIndex) {
            case 1:
                if (result[i].maxStudents <= result[i].registeredStudents){
                    result[i].relevance = -1;
                    console.log("case1");
                    continue;
                }
                break;
            case 2:
                if (result[i].maxStudents > result[i].registeredStudents){
                    result[i].relevance = -1;
                    console.log("case2");
                    continue;
                }
                break;
        }
    }

    // Sort by relevance
    result.sort(function(a, b){return b.relevance - a.relevance});

    // Update page content
    var tableList = document.getElementById("project_list");
    tableList.innerHTML = tableList.children[0].innerHTML;

    projectCount = 0;
    showMoreProjects(sq)

    /*
    // als je meteen aan de html toevoegd zonder eerst een string te maken dan sluit hij zelf de tags bv.:
    // je schrijft <div> code wordt aangevuld met </div>
    for (var i = 0; i< result.length; i ++) {
        rowStr = '';
        if ((result[i].relevance === 0 && sq.length > 0) || i > 10){break;}


        rowStr += '<tr>' + '<td><a href=' + result[i].href  + '>' + result[i].title + '</a></td>' + '<td>';

        for (var groupIter = 0; groupIter < result[i].researchGroup.length; groupIter++) {
            rowStr += result[i].researchGroup[groupIter] + '<br>';
        }
        rowStr +='</td>' + '<td>[' + result[i].registeredStudents + ' / ' + result[i].maxStudents + ']</td> ' + '</tr>';

        tableList.innerHTML += rowStr;
        projectCount = i+1;
    }
    //console.log("finished");
    */

}

function showMoreProjects(sq) {

    // Update page content
    var tableList = document.getElementById("project_list");
    var pCont = document.createElement("tbody");

    for (var i = projectCount; i < projectCount + 10; i++) {

        if ((result[i].relevance === 0 && sq.length > 0 || result[i].relevance === -1)){break;}

        var cont = document.createElement("tr");

        var name = document.createElement("td");
        var link = document.createElement("a");
        link.appendChild(document.createTextNode(result[i].title));
        link.href = "/projects/" + result[i].ID;
        name.appendChild(link);
        var desc = document.createElement("p");
        desc.appendChild(document.createTextNode(result[i].description));
        name.appendChild(desc);
        cont.appendChild(name);

        /*
        var group = document.createElement("td");

        for (var groupIter in result[i].researchGroup) {
            var newGr = document.createElement("br");
            newGr.appendChild(document.createTextNode(groupIter));

            group.appendChild(newGr);

        }

        cont.appendChild(group);
        */

        var tagCollection = document.createElement("td");
        for (var t in result[i]["tag"]){

            tag = document.createElement("p");
            tag.appendChild(document.createTextNode(result[i]["tag"][t]));
            tagCollection.appendChild(tag);

        }

        cont.appendChild(tagCollection);

        /*
        var stud = document.createElement("td");
        stud.appendChild(document.createTextNode('[' + result[i].registeredStudents + ' / ' + result[i].maxStudents + ']'));
        cont.appendChild(stud);

         */
        pCont.appendChild(cont);
    }
    tableList.appendChild(pCont);

    projectCount += 10;

}