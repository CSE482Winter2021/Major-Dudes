import React, {Component} from 'react';
import SimpleSelect from './Selector'
import Button from '@material-ui/core/Button/index';

class Estimator extends Component {
    constructor(props) {
        super(props);
        this.state = {data:[], calculated:false};
        this.childHandler = this.childHandler.bind(this);
        this.calculate = this.calculate.bind(this);
    }
    childHandler(index, dataFromChild) {
        const { data } = this.state;
        data[index] = dataFromChild;
        this.setState({ data });
    }
    calculate() {
        this.setState({calculated:true})
    }
    render() {
        const ageElements = {1:'0 to 4', 2:'5 to 9', 3: '10 to 14', 4: '15 to 17', 5:'18 to 19', 6:'20', 7:'21', 8:'22 to 24', 9:'25 to 29', 10:'30 to 34', 11:'35 to 39', 12:'40 to 44', 13:'45 to 49', 14:'50 to 54', 15:'55 to 59', 16:'60 to 61', 17:'62 to 64', 18:'65 to 66', 19:'67 to 69', 20:'70 to 74', 21:'75 to 79', 22:'80 to 84', 23:'Older than 85'};
        const genderElements = {1:'Male', 2:'Female'};
        const raceElements = {1:'White', 2:'Black', 3:'Native', 4:'Pacific Islander', 5:'Asian', 6:'Other'};
        const incomeElements = {1:'$0 to $9,999', 2:'$10,000 to $19,999', 3:'$20,000 to $34,999', 4:'$35,000 to $49,999', 5:'$50,000 to $74,999', 6:'Above 75,000'};
        const disabilityElements = {1:'No disabilities', 2:'One disability', 3:'Two or more Diabilities'}
        return (
            <div className="App">
                <h1 className="App-header" style={{ textAlign: "center" }}>ORCA Card Estimator</h1>
                <div>Find out how likely a person with some set of demographics is to have an ORCA Card in King County</div>
                <SimpleSelect index={0} label={'Age'} elements={ageElements} action={this.childHandler} />
                <SimpleSelect index={1} label={'Gender'} elements={genderElements} action={this.childHandler} />
                <SimpleSelect index={2} label={'Race'} elements={raceElements} action={this.childHandler} />
                <SimpleSelect index={3} label={'Income'} elements={incomeElements} action={this.childHandler} />
                <SimpleSelect index={4} label={'Disability'} elements={disabilityElements} action={this.childHandler} />
                <Button  margin="20px" onClick={this.calculate}>
                    Calculate ORCA Likelihood
                </Button>
                <div>{this.state.calculated ? <h1> 50% </h1> : null}</div>
                
            </div>
        );
    } 
}

export default Estimator;
