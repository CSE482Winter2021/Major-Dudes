import React from 'react';
import logo from '../www/card.jpg'

function HomePage() {
  return (
    <div className="App">
      <h1 className="App-header">How representative is ORCA card data?</h1>
      <div>
        <p>
          Major King County transit agencies, King County Metro and Sound
          Transit, often rely on ORCA card data to make decisions about their
          services. However, this data is biased against the many transit users
          who do not have an ORCA card.
        </p>
        <p>
          Many people in King County rely on the King County Metro's extensive
          bus system to get around. ORCA cards, issued by KCM and other
          transportation agencies, offer an easy way for riders to access the
          system and for agencies to collect data on riders to improve their
          services. However, not all populations have equal access to ORCA
          cards. This project aims to provide a robust model and intuitive
          interface to allow agencies to explore trends in ORCA card access in
          different commiunities across the county.{" "}
        </p>
      </div>
      <br />
      <br />
      <img src={logo} alt="ORCA card"></img>
    </div>
  );
}

export default HomePage;
