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

let resetButton = document.getElementById('resetbutton')
resetButton.addEventListener('click', async function() {
        const response = await fetch('http://127.0.0.1:3000/reset/')
        const resetjson = response.json()
        console.log(resetjson)
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
    updateStats(data)
    const airports = data.lista_kentista
    const risks = data.riskilista_kentille

    airportMarkers.clearLayers();
    for(let j = 0; j < airports.length; j++){
        if(j === 0) {
            const testmarker = L.marker([airports[j][1], airports[j][2]]).addTo(map);
            airportMarkers.addLayer(testmarker)
            const popupContent = document.createElement('div');
            const h4 = document.createElement('h4');
            const h5 = document.createElement('h5')
            h4.innerHTML = airports[j][0]
            h5.innerHTML = risks[j]
            popupContent.append(h4);
            popupContent.append(h5)
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
            const h5 = document.createElement('h5')
            h4.innerHTML = airports[j][0]
            h5.innerHTML = risks[j]
            popupContent.append(h4);
            popupContent.append(h5)
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
function updateStats(arg) {
    const data = arg.pstats
    const weather = arg.weather
    const moneydisplay = document.getElementById('Money')
    moneydisplay.innerHTML = data[0]
    const timedisplay = document.getElementById('Time')
    timedisplay.innerHTML = data[1]
    const co2display = document.getElementById('CO2')
    co2display.innerHTML = data[2]
    const weatherdisplay = document.getElementById('Weather')
    weatherdisplay.innerHTML = weather[1] ? weather[0] + ' C, ' + weather[1] : "Unknown"
    const rangedisplay = document.getElementById('Range')
    rangedisplay.innerHTML = data[4]
    const locdisplay = document.getElementById('Location')
    locdisplay.innerHTML = data[5]

}

