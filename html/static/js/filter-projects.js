function countOccurances(str, search){
    return (str.match( new RegExp(search, "gi")) || []).length;
}

function filterProjects(){

    var searchQ = document.getElementById("SQInput").value;

    // Init
    var result = obj;
    var sq = searchQ.trim();
    var tokens = sq.split(" ");
    var tokenCount = [];
    var totalTokenCount = [];
    var tokenProjectCount = [];

    for( var i in tokens) {
        tokenProjectCount[i] = 0;
        totalTokenCount[i] = 0;
        tokenCount[i] = [];
    }

    // Count Occurances
    for ( var i in result){
        result[i].relevance = 0;
        for( var j in tokens) {

            // Check in title
            if (countOccurances(result[i].title, tokens[j])) {
                result[i].relevance ++;

            }

            // Check in description
            var count = 0;
            for (word in result[i].words){
                if (countOccurances(word, tokens[j]) > 0){
                    count += result[i].words[word];
                }
            }

            tokenCount[j][i] = count;   // tokenCount for this project

            if (count > 0){
                totalTokenCount[j] += count;    // total token count
                tokenProjectCount[j] += 1;
            }

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
            if (!selectedDisciplines.includes(result[i].discipline[itt]) ){
                continue;
            }
            discFound = true;
            break;
        }
        if (!discFound && !selectedDisciplines.includes("All")){
            result[i].relevance = 0;
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
            result[i].relevance = 0;
            continue;
        }

        // Check research group
        var rgFound = false;
        for (var rgn in result[i].researchGroup){
            if (result[i].researchGroup[rgn] == rg.options[rg.selectedIndex].text){
                rgFound = true;
                break;
            }
        }
        if (!rgFound && rg.selectedIndex>0){
            result[i].relevance = 0;
            continue;
        }

        // Check status
        switch (status.selectedIndex) {
            case 1:
                if (result[i].maxStudents <= result[i].registeredStudents){
                    result[i].relevance = 0;
                    continue;
                }
                break;
            case 2:
                if (result[i].maxStudents > result[i].registeredStudents){
                    result[i].relevance = 0;
                    continue;
                }
                break;
        }

        for( var j in tokens) {
            if (tokenCount[j][i] && tokenProjectCount[j] !== 0){

                result[i].relevance += tokenCount[j][i] / totalTokenCount[j] / tokenProjectCount[j];
            }
        }

    }

    // Sort by relevance
    result.sort(function(a, b){return b.relevance - a.relevance});

    // Update page content
    var tableList = document.getElementById("project_list");
    tableList.innerHTML = tableList.children[0].innerHTML;

    // als je meteen aan de html toevoegd zonder eerst een string te maken dan sluit hij zelf de tags bv.:
    // je schrijft <div> code wordt aangevuld met </div>
    for (var i in result) {
        rowStr = '';
        if (result[i].relevance == 0){break;}

        rowStr += '<tr>' + '<td><a href=' + result[i].href  + '>' + result[i].title + '</a></td>' + '<td>';

        for (var groupIter = 0; groupIter < result[i].researchGroup.length; groupIter++) {
            rowStr += result[i].researchGroup[groupIter] + '<br>';
        }
        rowStr +='</td>' + '<td>[' + result[i].registeredStudents + ' / ' + result[i].maxStudents + ']</td> ' + '</tr>';

        tableList.innerHTML += rowStr;

    }
}