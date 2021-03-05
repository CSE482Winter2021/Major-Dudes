import React from 'react';
import SimpleSelect from './Selector'
function Estimator() {
  return (
    <div className="App">
      <h1 className="App-header" style={{ textAlign: "center" }}>ORCA Card Estimator</h1>
      <div>Find out how likely a person with some set of demographics is to have an ORCA Card in King County</div>
      <SimpleSelect />
    </div>
  );
}

export default Estimator;
