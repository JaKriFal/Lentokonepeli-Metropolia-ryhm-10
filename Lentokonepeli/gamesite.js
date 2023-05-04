const map = L.map('map', { tap: false });
L.tileLayer('https://{s}.google.com/vt/lyrs=s&x={x}&y={y}&z={z}', {
  maxZoom: 20,
  subdomains: ['mt0', 'mt1', 'mt2', 'mt3'],
}).addTo(map);
map.setView([60, 24], 7);

// lisää markeri helsinki vantaa lentokenttä
const marker = L.marker([60.317222, 24.963333]).addTo(map);
marker.bindPopup('Helsinki-Vantaan lentokenttä').openPopup();

// toinen markkeri tampereen lentokenttä ja popup
const marker2 = L.marker([61.414167, 23.604167]).addTo(map);
marker2.bindPopup('Tampere-Pirkkalan lentokenttä').openPopup();

//kysy käyttäjältä haluatko lentää helsinkiin vai tampereelle ja tee valitusta popupista sininen
const marker3 = L.marker([60.317222, 24.963333], { color: 'blue' }).addTo(map);
marker3.bindPopup('Helsinki-Vantaan lentokenttä').openPopup();

const marker4 = L.marker([61.414167, 23.604167], { color: 'blue' }).addTo(map);
marker4.bindPopup('Tampere-Pirkkalan lentokenttä').openPopup();

// lisää polyline helsinki vantaa lentokenttä ja tampereen lentokenttä
const polyline = L.polyline([
  [60.317222, 24.963333],
  [61.414167, 23.604167],
]).addTo(map);

// laske polyline pituus ja näytä se popupissa
const length = L.GeometryUtil.length(polyline);
const length2 = L.GeometryUtil.length(marker3);
const length3 = L.GeometryUtil.length(marker4);
const length4 = L.GeometryUtil.length(marker);
const length5 = L.GeometryUtil.length(marker2);

// lisää polyline helsinki vantaa lentokenttä ja tampereen lentokenttä
const polyline2 = L.polyline([
  [60.317222, 24.963333],
  [61.414167, 23.604167],
]).addTo(map);



