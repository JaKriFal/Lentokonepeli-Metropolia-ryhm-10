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

async function getData() {
    const response = await fetch('http://127.0.0.1:3000/kokeilu/')
    const json = await response.json()
    console.log(json)
    return json
}

async function gameUpdate() {
    const data = await getData()
    updateStats(data.pstats)
    const airports = data.lista_kentista

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
            const robButton = document.createElement('button');
            robButton.classList.add('button');
            robButton.innerHTML = 'Ryöstä';
            popupContent.append(robButton);
            robButton.addEventListener('click', async function () {
                    const robresponse = await fetch(`http://127.0.0.1:3000/kokeilu3/`)
                    const robjson = robresponse.json
                    console.log(robjson)
                    await gameUpdate()
            })
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
function updateStats(data) {
    const moneydisplay = document.getElementById('Money')
    moneydisplay.innerHTML = data[0]
    const timedisplay = document.getElementById('Time')
    timedisplay.innerHTML = data[1]
    const co2display = document.getElementById('CO2')
    co2display.innerHTML = data[2]
    const weatherdisplay = document.getElementById('Weather')
    weatherdisplay.innerHTML = data[3]
    const rangedisplay = document.getElementById('Range')
    rangedisplay.innerHTML = data[4]
    const locdisplay = document.getElementById('Location')
    locdisplay.innerHTML = data[5]
}

