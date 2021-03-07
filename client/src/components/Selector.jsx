import React, { Component } from "react";
import { makeStyles } from '@material-ui/core/styles';
import InputLabel from '@material-ui/core/InputLabel';
import MenuItem from '@material-ui/core/MenuItem';
import FormHelperText from '@material-ui/core/FormHelperText';
import FormControl from '@material-ui/core/FormControl';
import Select from '@material-ui/core/Select';
// import { Parser } from 'html-to-react';

const useStyles = makeStyles((theme) => ({
    formControl: {
        margin: theme.spacing(1),
        minWidth: 120,
    },
    selectEmpty: {
        marginTop: theme.spacing(2),
    },
}));

class SimpleSelect extends Component {
    constructor(props) {
        super(props);
        this.state = {val:null};
    }

    render() {
        const handleChange = (event) => {
            this.setState({ val: event.target.value });
            console.log('handleChange ' + event.target.value)
            this.props.action(this.props.index, event.target.value);
        };
    
        const items = []
    
        for (let k in this.props.elements) {
            items.push(<MenuItem value={k}>{this.props.elements[k]}</MenuItem>)
        }
    
        return (
            <div>
                <FormControl>
                    <InputLabel id="demo-simple-select-helper-label">{this.props.label}</InputLabel>
                    <Select
                        labelId="demo-simple-select-helper-label"
                        id="demo-simple-select-helper"
                        // value={age}
                        onChange={handleChange}
                    >
                        <MenuItem value="">
                            <em>None</em>
                        </MenuItem>
                        {items}
                    </Select>
                    <FormHelperText>Select the {this.props.label} to calculate the ORCA rate for</FormHelperText>
                </FormControl>
            </div>
        );
    }
}

export default SimpleSelect;