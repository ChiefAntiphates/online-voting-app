import logo from './logo.svg';
import './App.css';
import { io } from "socket.io-client";
import React, {useContext, useEffect, useState} from 'react'

const SOCKET_BASE = "http://localhost:5000"

function App() {

  const [buttonClicks, setButtonClicks] = useState(0)

  useEffect(() => {
    const test_socket = io(`${SOCKET_BASE}/testnp`);
    test_socket.on("test_topic", data => {
      console.log(data) 
    })
    //socketio.emit('clicked', {"number": button_clicks}, namespace='/button_clicks')
    const button_socket = io(`${SOCKET_BASE}/button_clicks`)
    button_socket.on("clicked", data => {
      console.log("HELLO")
      console.log(data)
      setButtonClicks(data.number)
    })
  }, [])

  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <h1>There have been {buttonClicks} button clicks</h1>
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
