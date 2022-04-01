import logo from './logo.svg';
import './App.css';
import { io } from "socket.io-client";
import React, {useContext, useEffect} from 'react'


function App() {


  useEffect(() => {
    const socket = io("http://localhost:5000");
    socket.on("test_topic", data => {
      console.log(data)
    });
  }, [])

  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
      </header>
    </div>
  );
}

export default App;
