import React, { Component } from 'react';
import axios from 'axios';
import SimpleSelect from './Selector';
import Button from '@material-ui/core/Button/index';
import "./MapPage.css";
import MapPage from "./MapPage.jsx"

class Estimator extends Component {
    constructor(props) {
        super(props);
        this.state = {data:[], calculated:false, loading:false, total:-1};
        this.childHandler = this.childHandler.bind(this);
        this.calculate = this.calculate.bind(this);
    }
    childHandler(index, dataFromChild) {
        const { data } = this.state;
        data[index] = dataFromChild;
        this.setState({ data });
    }
    async calculate() {
        const age = this.state.data[0];
        const gender = this.state.data[1];
        const race = this.state.data[2];
        const income = this.state.data[3];
        const dis = this.state.data[4];
        const url = `http://localhost:5000/model_output?age=${age}&gender=${gender}&race=${race}&income=${income}&dis=${dis}&`;
        try {
            this.setState({ loading: true });
            const response = await axios.get(url);
            this.setState({loading: false});
            this.setState({ calculated: true, total: response.data})
        } catch (err) {
            this.setState({ loading: false });
            this.setState({
                calculated: true,
                total: 'error',
            });
            console.log(err);
        }
    }
    render() {
        const ageElements = {1:'0 to 4', 2:'5 to 9', 3: '10 to 14', 4: '15 to 17', 5:'18 to 19', 6:'20', 7:'21', 8:'22 to 24', 9:'25 to 29', 10:'30 to 34', 11:'35 to 39', 12:'40 to 44', 13:'45 to 49', 14:'50 to 54', 15:'55 to 59', 16:'60 to 61', 17:'62 to 64', 18:'65 to 66', 19:'67 to 69', 20:'70 to 74', 21:'75 to 79', 22:'80 to 84', 23:'Older than 85'};
        const genderElements = {1:'Male', 2:'Female'};
        const raceElements = {1:'White', 2:'Black', 3:'Native', 4:'Pacific Islander', 5:'Asian', 6:'Other'};
        const incomeElements = {1:'$0 to $9,999', 2:'$10,000 to $14,999', 3:'$15,000 to $19,999', 4:'$20,000 to $24,999', 5:'$25,000 to $29,999', 6:'$30,000 to $34,999', 7:'$35,000 to $39,999', 8:'$40,000 to $44,999', 9:'$45,000 to $49,999', 10:'$50,000 to $59,999', 11:'$60,000 to $74,999', 12:'$75,000 to $99,999', 13:'$100,000 to $124,999', 14:'$125,000 to $149,999', 15:'$150,000 to $199,999', 16:'More than $200,000'};
        const disabilityElements = {1:'Disabled', 2:'Not Disabled'}

        return (
            <div className="App">
                <h1 className="App-header" style={{ textAlign: "center" }}>ORCA Card Estimator</h1>
                <div>Select an option for each of the following demographics to find out how likely such a person is to own an ORCA Card in King County</div>
                <div className="rowC">
                    <SimpleSelect index={0} label={'Age'} elements={ageElements} action={this.childHandler} helptext={'Select an age range to calculate the ORCA rate for'}/>
                    <SimpleSelect index={1} label={'Gender'} elements={genderElements} action={this.childHandler} helptext={'Select a gender to calculate the ORCA rate for'}/>
                    <SimpleSelect index={2} label={'Race'} elements={raceElements} action={this.childHandler} helptext={'Select a race to calculate the ORCA rate for'}/>
                    <SimpleSelect index={3} label={'Income'} elements={incomeElements} action={this.childHandler} helptext={'Select an income range to calculate the ORCA rate for'}/>
                    <SimpleSelect index={4} label={'Disability'} elements={disabilityElements} action={this.childHandler} helptext={'Select a disability status to calculate the ORCA rate for'}/>
                </div>
                <Button variant="contained" color="primary" margin="20px" onClick={this.calculate}>
                    Calculate ORCA Likelihood
                </Button>
                <div><h1>Estimated ORCA Likelihood: {
                    this.state.loading ?
                        'loading...'
                        : this.state.calculated
                            ? this.state.total + '%'
                            : null}</h1></div>
                <MapPage selectors={this.state.data}/>
            </div>
        );
    }
}

export default Estimator;
