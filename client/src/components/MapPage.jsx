import React, { Component } from "react";
import L from 'leaflet';
import R from 'leaflet-responsive-popup';
import { MapContainer as Map, GeoJSON } from "react-leaflet";
import mapData from "../tracts_demographics.json";
import waterMap from "../water.json";
import "leaflet/dist/leaflet.css";
import "./MapPage.css";
import Button from '@material-ui/core/Button/index';

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

const defaultState = {
  clicked: false,
  tract_num: 0,
  population: 0,
  male: 0,
  female: 0,
  white: 0,
  black: 0,
  native: 0,
  asian: 0,
  pacIsl: 0,
  other: 0,
  disabled: 0,
};

class MapPage extends Component {
  constructor(props) {
    super(props);
    this.state = defaultState;
    this.onEachTract = this.onEachTract.bind(this);
    this.handleTractClick = this.handleTractClick.bind(this);
    this.getDemographics = this.getDemographics.bind(this);
    this.unClicked = this.unClicked.bind(this);
  }

  onEachTract (tract, layer) {
    var dict = {}
  
    dict['Tract Number'] = tract.properties['TRACT NUMBER'];
    dict['Population']= tract.properties.POPULATION;
    dict['Male'] = tract.properties.MALE;
    dict['Female']= tract.properties.FEMALE;
    dict['White'] = tract.properties.WHITE;
    dict['Black'] = tract.properties.BLACK;
    dict['Native']= tract.properties.NATIVE;
    dict['Asian'] = tract.properties.ASIAN;
    dict['Pacific Islander'] = tract.properties['PACIFIC ISLANDER'];
    dict['Other Race'] = tract.properties.OTHER;
    dict['Disabled'] = tract.properties.DISABLED;
  
    const popup = R.responsivePopup().setContent('Tract Number ' + dict['Tract Number']);
    layer.bindPopup(popup);
  
    layer.on('mouseover mousemove', function (e) {
      this.openPopup(e.latlng);
    });

    layer.on('click', () => {this.handleTractClick(dict)});
    layer.on('mouseout', function (e) {
      this.closePopup();
    });
    
  }

  handleTractClick(dict) {
    if (this.state.tract_num === dict['Tract Number'])
      return;
    this.setState({
      clicked: true,
      tract_num: dict['Tract Number'],
      population: dict['Population'],
      male: dict['Male'],
      female: dict['Female'],
      white: dict['White'],
      black: dict['Black'],
      native: dict['Native'],
      asian: dict['Asian'],
      pacIsl: dict['Pacific Islander'],
      other: dict['Other Race'],
      disabled: dict['Disabled'],
    });
    console.log(this.state);
  }

  getDemographics() {
    // var react = new Parser();
    const demos = this.state;
    return (
      <div className='container'>
        <table className='demo_table'>
          <tr><th>Total Population</th><td>{demos['population']}</td></tr>
          <tr><th>Population Male</th><td>{demos['male']}</td></tr>
          <tr><th>Population Female</th><td>{demos['female']}</td></tr>
          <tr><th>Population Disabled</th><td>{demos['disabled']}</td></tr>
        </table>
        <p className='italics'>Racial Demographics:</p>
        
        <table className='demo_table'>
           <tr><th>White</th><td>{demos['white']}</td></tr>
           <tr><th>Black</th><td>{demos['black']}</td></tr>
           <tr><th>Native</th><td>{demos['native']}</td></tr>
           <tr><th>Asian</th><td>{demos['asian']}</td></tr>
           <tr><th>Pacific Islander</th><td>{demos['pacIsl']}</td></tr>
           <tr><th>Other Race</th><td>{demos['other']}</td></tr>
         </table>
      </div>
      );
  }
  
  unClicked() {
    this.setState({
      clicked: false,
    });
  }

  render() {
    const { clicked, tract_num } = this.state;
    return (
      <div className="App">
        <h1 className="App-header">King County Interactive Map</h1>
        <div className='container'>
          <div className='leaflet-container'>
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
                onEachFeature={this.onEachTract}
              />
            </Map>
          </div>
          { clicked ? <div className='overlay'>
            <h3>
              Tract {tract_num} Demographics:
            </h3>
            <this.getDemographics />
            <Button  margin="20px" onClick={this.unClicked} transitionDuration={0}>
              Close
            </Button>
          </div> : null}
        </div>
      </div>
    );
  }
}

export default MapPage;