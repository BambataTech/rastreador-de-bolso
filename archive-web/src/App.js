import React, { useState } from 'react';
import './App.css';
import Tweets from './Tweets/Tweets';
import UserInput from './UserInput/UserInput';

function App() {
  const [search, setSearch] = useState();

  const changeUsernameHandler = (event) => {
    setSearch(event.target.value);
  };

  // const script = document.createElement('script');
  // script.src = 'https://platform.twitter.com/widgets.js';
  // script.async = true;
  // document.body.appendChild(script);

  return (
    <section className="App">
      <div>
        <h1>Arquivo de Tweets - Bolsonaro</h1>
      </div>
      <div>
        <UserInput changed={changeUsernameHandler} search={search} />
      </div>
      <div className="Tweets">
        {search && search.length > 3 ? <Tweets search={search} /> : null}
      </div>
    </section>
  );
}

export default App;
