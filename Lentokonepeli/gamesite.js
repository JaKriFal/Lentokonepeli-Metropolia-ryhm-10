const map = L.map('map', { tap: false });
L.tileLayer('https://{s}.google.com/vt/lyrs=s&x={x}&y={y}&z={z}', {
  maxZoom: 20,
  subdomains: ['mt0', 'mt1', 'mt2', 'mt3'],
}).addTo(map);
map.setView([60, 24], 7);

let restartButton = document.getElementById('restartbutton')
restartButton.addEventListener('click', getList)
/*
// JSON-pyynnön tekeminen endpointiin
$.getJSON("http://127.0.0.1:3000/kokeilu/", function(data) {

    // Käsitellään vastausdatan pisteet
    var points = data.lista_kentistä.map(function(point) {
        return {
            name: point[0],
            latlng: L.latLng(point[2], point[3]),
            risk: data.riskilista_kentille[data.lista_kentistä.indexOf(point)],
            distance: point[1]
        };
    });

    // Pisteiden piirtäminen kartalle
    for (var i = 0; i < points.length; i++) {
        var point = points[i];
        L.marker(point.latlng)
            .addTo(map)
            .bindPopup(point.name + "<br>Riski jäädä kiinni: " + point.risk + "<br>Etäisyys: " + point.distance.toFixed(2) + " km");
    }
});


 */

async function getList() {
    const response = await fetch('http://127.0.0.1:3000/kokeilu/')
    const json = await response.json()
    console.log(json)
}