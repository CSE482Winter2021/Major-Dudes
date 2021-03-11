import React from 'react';

function HomePage() {
  return (
    <div className="App">
      <h1 className="App-header">How representative is ORCA card data?</h1>
      <div>
      <p>Major King County transit agencies, King County Metro and Sound Transit, often rely on ORCA card data to make decisions about their services. However, this data is biased against the many transit users who do not have an ORCA card.</p>
      <p>The goal of our project is to provide data about who these people are who we don’t have ORCA card data on. We have worked to provide an estimate of how likely a person with certain demographic characteristics is to have an ORCA card as a way of improving our understanding of how representative this data is of the entire King County population. We hope that this will help policy makers prioritize areas of need that are typically neglected due to a lack of data on those areas/populations. </p>
      </div>
    </div>
  );
}

export default HomePage;
