console.log('Carmine is based');

function loadDoc(url, func) {
    let xhttp = new XMLHttpRequest();
    xhttp.onload = function() {
        if (xhttp.status != 200) {
            console.log("Error");
        } else {
            func(xhttp.response);
        }
    }
    xhttp.open("GET", url);
    xhttp.send();
}

function apartment_search() {
    let txtSearch = document.getElementById("txtSearch");

    let selBeds = document.getElementById("selBeds");

    let selSort = document.getElementById("selSort");
    let url = "/apt/" + txtSearch.value + "/" + selBeds.value + "/" + selSort.value;
    console.log(url);
    loadDoc(url, apartment_search_results);
}

function apartment_search_results(response) {
    let data = JSON.parse(response);
    let result = data["result"];
    console.log(result);

    let temp = "";

    for (let i = 0; i < result.length; i++) {
        let apartment = result[i];

        temp += "<div class=\"apartment_container\">";
        temp += "<div>" + "Apartment: " + apartment["title"] + "</div>";
        temp += "<div>" + "Monthly Rent: $" + apartment["monthly rent"] +  "</div>";
        temp += "<div>" + "Beds: "  + apartment["beds"] + "</div>";
        temp += "<div>" + "Description: " + apartment["description"] + "</div>";
        temp += "</div>";
    }

    let divResults = document.getElementById("divResults");
    divResults.innerHTML = temp;
}

