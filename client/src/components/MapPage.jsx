import React, { Component } from "react";
import L from 'leaflet';
import R from 'leaflet-responsive-popup';
import { MapContainer as Map, GeoJSON } from "react-leaflet";
import mapData from "../tracts_demographics.json";
import waterMap from "../water.json";
import "leaflet/dist/leaflet.css";
import "./MapPage.css";
import Button from '@material-ui/core/Button/index';
import SimpleSelect from './Selector'
import tract_demos from "../tract_to_demographics.json";

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
  tract_num: ''
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
    const popup = R.responsivePopup().setContent('Tract Number ' + tract.id);
    layer.bindPopup(popup);
  
    layer.on('mouseover mousemove', function (e) {
      this.openPopup(e.latlng);
    });

    layer.on('click', (e) => {
      this.handleTractClick(tract.id)
      layer.center(e.latlng)
    });
    layer.on('mouseout', function (e) {
      this.closePopup();
    });
  }

  handleTractClick(tr_num) {
    // if (this.state.tract_num === tr_num)
    //   return;
    this.setState({
      clicked: true,
      tract_num: tr_num,
    });
    console.log(this.state);
  }

  getDemographics() {
    // var react = new Parser();
    const {tract_num }= this.state;
    const ageElements = {1:'0 to 4', 2:'5 to 9', 3: '10 to 14', 4: '15 to 17', 5:'18 to 19', 6:'20', 7:'21', 8:'22 to 24', 9:'25 to 29', 10:'30 to 34', 11:'35 to 39', 12:'40 to 44', 13:'45 to 49', 14:'50 to 54', 15:'55 to 59', 16:'60 to 61', 17:'62 to 64', 18:'65 to 66', 19:'67 to 69', 20:'70 to 74', 21:'75 to 79', 22:'80 to 84', 23:'Older than 85'};
    const genderElements = {1:'Male', 2:'Female'};
    const raceElements = {1:'White', 2:'Black', 3:'Native', 4:'Pacific Islander', 5:'Asian', 6:'Other'};
    const incomeElements = {1:'$0 to $9,999', 2:'$10,000 to $14,999', 3:'$15,000 to $19,999', 4:'$20,000 to $24,999', 5:'$25,000 to $29,999', 6:'$30,000 to $34,999', 7:'$35,000 to $39,999', 8:'$40,000 to $44,999', 9:'$45,000 to $49,999', 10:'$50,000 to $59,999', 11:'$60,000 to $74,999', 12:'$75,000 to $99,999', 13:'$100,000 to $124,999', 14:'$125,000 to $149,999', 15:'$150,000 to $199,999', 16:'More than $200,000'};
    const disabilityElements = {1:'Disabled', 2:'Not Disabled'}
    return (
      <div className='container'>
        <table className='demo_table'>
          <tr>
            <th></th>
            <th>King County</th>
            <th>Tract {tract_demos[tract_num]['name']}</th>
          </tr>
          <tr>
            <td>Age: {ageElements[this.props.selectors[0]]}</td>
            <td>{Math.round(10000 * tract_demos['total']['age'][this.props.selectors[0]]/tract_demos['total']['age'][0]) / 100}%</td>
            <td>{Math.round(10000 *tract_demos[tract_num]['age'][this.props.selectors[0]]/tract_demos[tract_num]['age'][0]) / 100}%</td>
          </tr>
          <tr>
            <td>Gender: {genderElements[this.props.selectors[1]]}</td>
            <td>{Math.round(10000 * tract_demos['total']['gender'][this.props.selectors[1]]/tract_demos['total']['gender'][0]) / 100}%</td>
            <td>{Math.round(10000 *tract_demos[tract_num]['gender'][this.props.selectors[1]]/tract_demos[tract_num]['gender'][0]) / 100}%</td>
          </tr>
          <tr>
            <td>Race: {raceElements[this.props.selectors[2]]}</td>
            <td>{Math.round(10000 * tract_demos['total']['race'][this.props.selectors[2]]/tract_demos['total']['race'][0]) / 100}%</td>
            <td>{Math.round(10000 *tract_demos[tract_num]['race'][this.props.selectors[2]]/tract_demos[tract_num]['race'][0]) / 100}%</td>
          </tr>
          <tr>
            <td>Income: {incomeElements[this.props.selectors[3]]}</td>
            <td>{Math.round(10000 * tract_demos['total']['income'][this.props.selectors[3]]/tract_demos['total']['income'][0]) / 100}%</td>
            <td>{Math.round(10000 *tract_demos[tract_num]['income'][this.props.selectors[3]]/tract_demos[tract_num]['income'][0]) / 100}%</td>
          </tr>
          <tr>
            <td>{disabilityElements[this.props.selectors[4]]}</td>
            <td>{Math.round(10000 * tract_demos['total']['disability'][this.props.selectors[4]]/tract_demos['total']['disability'][0]) / 100}%</td>
            <td>{Math.round(10000 *tract_demos[tract_num]['disability'][this.props.selectors[4]]/tract_demos[tract_num]['disability'][0]) / 100}%</td>
          </tr>
          <tr>
            <td>All Selections</td>
            <td>{Math.round(1000000 * (tract_demos['total']['disability'][this.props.selectors[4]]/tract_demos['total']['disability'][0]) * (tract_demos['total']['income'][this.props.selectors[3]]/tract_demos['total']['income'][0]) * (tract_demos['total']['race'][this.props.selectors[2]]/tract_demos['total']['race'][0]) * (tract_demos['total']['gender'][this.props.selectors[1]]/tract_demos['total']['gender'][0]) * (tract_demos['total']['age'][this.props.selectors[0]]/tract_demos['total']['age'][0])) / 10000}%</td>
            <td>{Math.round(1000000 * (tract_demos[tract_num]['disability'][this.props.selectors[4]]/tract_demos[tract_num]['disability'][0]) * (tract_demos[tract_num]['income'][this.props.selectors[3]]/tract_demos[tract_num]['income'][0]) * (tract_demos[tract_num]['race'][this.props.selectors[2]]/tract_demos[tract_num]['race'][0]) * (tract_demos[tract_num]['gender'][this.props.selectors[1]]/tract_demos[tract_num]['gender'][0]) * (tract_demos[tract_num]['age'][this.props.selectors[0]]/tract_demos[tract_num]['age'][0])) / 10000}%</td>
          </tr>
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
    const tractSelector = {'006600': 66, '005300' : 53, '025805' : 258.05};

    return (
      <div className="container">
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
        <div className='overlay'>
          <SimpleSelect index={0} label={'Tract Number'} elements={tractSelector} action={(a, b)=>{this.handleTractClick(b)}} helptext={'Select a tract number to view details about your chosen demographics in that tract.'}/>
          <div className='link'><a href="https://geocoding.geo.census.gov/geocoder/geographies/address?form">Find any address's corresponding tract here</a></div>
        </div>
        { clicked ? <div className='overlay'>
          <h3>
            Likelihood of selected demographics in Tract {tract_demos[tract_num]['name']}
          </h3>
          <this.getDemographics />
          <Button  margin="20px" onClick={this.unClicked} transitionDuration={0}>
            Close
          </Button>
        </div> : null}
    </div>
    );
  }
}

export default MapPage;