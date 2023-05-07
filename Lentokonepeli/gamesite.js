const map = L.map('map', { tap: false });
L.tileLayer('https://{s}.google.com/vt/lyrs=s&x={x}&y={y}&z={z}', {
  maxZoom: 20,
  subdomains: ['mt0', 'mt1', 'mt2', 'mt3'],
}).addTo(map);
map.setView([60, 24], 7);


//constants
const airportMarkers = L.featureGroup().addTo(map);



let startButton = document.getElementById('startbutton')
startButton.addEventListener('click', async function() {
        await gameUpdate()

    })


/*
            const marker = L.marker([airport.latitude, airport.longitude]).addTo(map);
            airportMarkers.addLayer(marker);
            marker.setIcon(blueIcon);
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

async function getData() {
    const response = await fetch('http://127.0.0.1:3000/kokeilu/')
    const json = await response.json()
    console.log(json)
    return json
}

async function gameUpdate() {
    let data = await getData()
    let airports = data.lista_kentista
    airportMarkers.clearLayers();
    for(let j = 0; j < airports.length; j++){
        if(j === 0) {
            const testmarker = L.marker([airports[j][1], airports[j][2]]).addTo(map);
            airportMarkers.addLayer(testmarker)
            const popupContent = document.createElement('div');
            const h4 = document.createElement('h4');
            h4.innerHTML = airports[j][0]
            popupContent.append(h4);
            testmarker.bindPopup(popupContent);
            testmarker._icon.classList.add("huechange");
                    } else {
            const testmarker = L.marker([airports[j][1], airports[j][2]]).addTo(map);
            airportMarkers.addLayer(testmarker)
            const popupContent = document.createElement('div');
            const h4 = document.createElement('h4');
            h4.innerHTML = airports[j][0]
            popupContent.append(h4);
            testmarker.bindPopup(popupContent);
            const flyButton = document.createElement('button');
            flyButton.classList.add('button');
            flyButton.innerHTML = 'Lennä';
            popupContent.append(flyButton);
                    flyButton.addEventListener('click', async function () {
            const flyresponse = await fetch(`http://127.0.0.1:3000/kokeilu2/${j+1}`)
            const flyjson = flyresponse.json
            console.log(flyjson)
            await gameUpdate()

        })
        map.flyTo([data.omapaikka[1], data.omapaikka[2]], 7);

        }


    }

}

