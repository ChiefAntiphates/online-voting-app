import { io } from "socket.io-client";
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import React, {useEffect, useState} from 'react'
import Voting from "./pages/voting";
import Home from "./pages/home"
import Create from "./pages/create";
import { SOCKET_BASE } from "./Constants";


function App() {
  

  return (
    <Router>
        <Routes>
          <Route exact path='/' element={<Home />} />
          <Route exact path='/vote/:id' element={<Voting />} />
          <Route exact path='/create' element={<Create />} />
          <Route exact path='*' element={<h1>No page</h1>} />
        </Routes>
    </Router>
  );
}

export default App;
