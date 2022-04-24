import { io } from "socket.io-client";
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import React, {useEffect, useState} from 'react'
import Voting from "./voting";

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
    <Router>
        <Routes>
          <Route exact path='/' element={<h2>Home Page</h2>} />
          <Route exact path='/vote/:id' element={<Voting />} />
          <Route exact path='*' element={<h1>No page</h1>} />
        </Routes>
    </Router>
  );
}

export default App;
