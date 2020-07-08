let accessToken = "";

function buttonClick() {
    let artistName = document.getElementById("searchBox").value; 
    let response = fetchAsync2('http://127.0.0.1:5000/getRelatedArtists?artistName=' + artistName + '&accessToken=' + accessToken)
}

window.onload = function() {
    url = new URL(window.location.href);



    if (!url.searchParams.get('accessToken')) {
        fetchAsync('http://127.0.0.1:5000/login');
    } else {
        accessToken = url.searchParams.get('accessToken');
    }

}

async function fetchAsync (url) {
    let response = await fetch(url);
    let data = await response.json();
    window.location.href = data.url;
}

async function fetchAsync2 (url) {
    let response = await fetch(url);
    let data = await response.text();
    console.log(data)
    document.getElementById("result").innerHTML = JSON.stringify(data);
}