import React, { Component } from "react";
import { MapContainer as Map, GeoJSON } from "react-leaflet";
import mapData from "../tracts_2020.json";
import "leaflet/dist/leaflet.css";
import "./MyMap.css";

class MyMap extends Component {
  tractStyle = {
    fillColor: "red",
    fillOpacity: 1,
    color: "black",
    weight: 2,
  };

  onEachTract = (tract, layer) => {
    const tractName = tract.properties.TRACTCE20;
    console.log(tractName);
    layer.bindPopup(tractName);

    layer.options.fillOpacity = 0.4;

    layer.on('mouseover', function (e) {
      this.openPopup();
    });
    layer.on('mouseout', function (e) {
        this.closePopup();
    });
  };

  render() {
    return (
      <div>
        <h1 style={{ textAlign: "center" }}>King County ORCA Penetration</h1>
        <div className='rowC'>
          <Map style={{ height: "90vh", width: "150vh" }} zoom={10} center={[47.45, -121.8]}>
            <GeoJSON
              style={this.tractStyle}
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