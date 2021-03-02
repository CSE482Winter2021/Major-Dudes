import React, { Component } from "react";
import { MapContainer as Map, GeoJSON } from "react-leaflet";
// import mapData from "../tracts_2020.json";
import mapData from "../tracts_demographics.json";
import waterMap from "../water.json";
import "leaflet/dist/leaflet.css";
import "./MyMap.css";
import FunButton from './button';


class MyMap extends Component {
  constructor(props) {
    super(props);
    this.state = {
      open: true
    };
  }

  tractStyle = {
    fillColor: "green",
    fillOpacity: 0.4,
    weight: 2,
  };
  waterStyle = {
    fillColor: "lightblue",
    fillOpacity: 1,
    color: "grey",
    weight: 2,
  };
  tractBorderStyle = {
    color: "black",
    fillOpacity: 0,
    weight: 2,
  };

  onEachTract = (tract, layer) => {
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
    layer.bindPopup(JSON.stringify(popupContent));

    layer.on('mouseover', function (e) {
      this.openPopup();
    });
    layer.on('mouseout', function (e) {
      this.closePopup();
    });
  }

  render() {
    console.log(waterMap) 
    return (
      <div>
        <h1 style={{ textAlign: "center" }}>King County ORCA Penetration</h1>
        <div className='rowC'>
          <Map style={{ height: "90vh", width: "150vh" }} zoom={10} center={[47.45, -121.8]}>
            <GeoJSON
              style={this.tractStyle}
              data={mapData.features}
            />
            <GeoJSON
              style={this.waterStyle}
              data={waterMap.features}
            />
            <GeoJSON
              style={this.tractBorderStyle}
              data={mapData.features}
              onEachFeature={this.onEachTract}
            />
            
          </Map>
          <div className='rightCol'>
            This react app give population data about each census Tract as well as the expected ORCA penetration rate.
          </div>
        </div>
      </div>
    );
  }
}

export default MyMap;