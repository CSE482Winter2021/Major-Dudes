import React, { Component } from "react";
import L from 'leaflet';
import R from 'leaflet-responsive-popup';
import { MapContainer as Map, GeoJSON } from "react-leaflet";
import mapData from "../tracts_demographics.json";
import waterMap from "../water.json";
import "leaflet/dist/leaflet.css";
import "./MyMap.css";

const tractStyle = {
  fillColor: "green",
  fillOpacity: 0.4,
  weight: 2,
};
const waterStyle = {
  fillColor: "lightblue",
  fillOpacity: 1,
  color: "grey",
  weight: 2,
};
const tractBorderStyle = {
  color: "black",
  fillOpacity: 0,
  weight: 2,
};

function onEachTract (tract, layer) {
  console.log(tract.properties)

  var dict = {}

  dict['Tract Number'] = tract.properties.[ 'TRACT NUMBER'];
  dict['Population']= tract.properties.POPULATION;
  dict['Male'] = tract.properties.MALE;
  dict['Female']= tract.properties.FEMALE;
  dict['White'] = tract.properties.WHITE;
  dict['Black'] = tract.properties.BLACK;
  dict['Native']= tract.properties.NATIVE;
  dict['Asian'] = tract.properties.ASIAN;
  dict['Pacific Islander'] = tract.properties.[ 'PACIFIC ISLANDER' ];
  dict['Other Race'] = tract.properties.OTHER;
  dict['Disabled'] = tract.properties.DISABLED;

  var popupContent = '<table>';
  for (var p in dict) {
      popupContent += '<tr><td>' + p + '</td><td>'+ dict[p] + '</td></tr>';
  }
  popupContent += '</table>';
  const popup = R.responsivePopup().setContent(JSON.stringify(popupContent));
  layer.bindPopup(popup);

  layer.on('mouseover mousemove', function (e) {
    this.openPopup(e.latlng);
  });
  layer.on('mouseout', function (e) {
    this.closePopup();
  });
}

function MyMap() {
  return (
    <div>
      <h1 style={{ textAlign: "center" }}>King County ORCA Penetration</h1>
      <div className='rowC'>
        <Map style={{ height: "90vh", width: "150vh" }} zoom={10} center={[47.45, -121.8]}>
          <GeoJSON
            style={tractStyle}
            data={mapData.features}
          />
          <GeoJSON
            style={waterStyle}
            data={waterMap.features}
          />
          <GeoJSON
            style={tractBorderStyle}
            data={mapData.features}
            onEachFeature={onEachTract}
          />
          
        </Map>
        <div className='rightCol'>
          This react app give population data about each census Tract as well as the expected ORCA penetration rate.
        </div>
      </div>
    </div>
  );
}

export default MyMap;