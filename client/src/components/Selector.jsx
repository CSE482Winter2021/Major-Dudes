import React, { Component } from "react";
import { makeStyles } from "@material-ui/core/styles";
import InputLabel from "@material-ui/core/InputLabel";
import MenuItem from "@material-ui/core/MenuItem";
import FormHelperText from "@material-ui/core/FormHelperText";
import FormControl from "@material-ui/core/FormControl";
import Select from "@material-ui/core/Select";
import Button from '@material-ui/core/Button';

import Popup from "reactjs-popup";
import "reactjs-popup/dist/index.css";

function getDesc(type) {
    switch (type) {
      case "Age":
        return "This is stored by the WA Census as categories of small ranges of ages - for example, 18-19. In some cases, a category will only be a single age.";
      case "Gender":
        return "The WA Census only stores information on biological sex, although it is categorized as 'gender.' For transgender individuals, the census stores their most recent gender identification. For gender non-conforming individuals, the census records their biological sex at birth.";
      case "Race":
        return "The WA Census stores information on race as categories White, Black, Native, Pacific Islander, Asian, or Other. Races not specified here (for example, Middle Eastern), or mixed races, are typically categorized under 'Other.'";
      case "Income":
        return "The WA Census stores information on yearly income in categories by ranges of values, up to $200k, above which is under a single category.";
      case "Disability":
        return "The WA Census stores information on disability in categories of either 0 (no disabilities), 1 (single disability), or 2+ (multiple disabilities). For the purpoes of our model, we combined 1 and 2+ into 'disabled' and 0 into 'not disabled.'";
    }
    return type
}

class SimpleSelect extends Component {
  constructor(props) {
    super(props);
    this.state = { val: null };
  }

  render() {
    const handleChange = (event) => {
      this.setState({ val: event.target.value });
      console.log("handleChange " + event.target.value);
      this.props.action(this.props.index, event.target.value);
    };

    const items = [];

    for (let k in this.props.elements) {
      items.push(<MenuItem value={k}>{this.props.elements[k]}</MenuItem>);
    }

    return (
      <div>
        <FormControl style={{ margin: "5%" }}>
          <br />
          <Popup trigger={<Button> (info)</Button>} position="bottom center">
            <div>{getDesc(this.props.label)}</div>
          </Popup>
          <InputLabel id="demo-simple-select-helper-label">
            {this.props.label}
          </InputLabel>
          <Select
            labelId="demo-simple-select-helper-label"
            id="demo-simple-select-helper"
            onChange={handleChange}
          >
            <MenuItem value="">
              <em>None</em>
            </MenuItem>
            {items}
          </Select>
          <FormHelperText>{this.props.helptext}</FormHelperText>
        </FormControl>
      </div>
    );
  }
}

export default SimpleSelect;
