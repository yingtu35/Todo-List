import './App.css';
import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Link, Navigate} from "react-router-dom";
import Header from './components/Header'
import Footer from './components/Footer';
import HomePage from './components/HomePage';
import SignUp from './components/SignUp';
import { Box } from "@chakra-ui/react"
import Todos from './components/Todos';


function App() {
  const [username, setUsername] = useState('');
  const [userId, setUserId] = useState('');

  function loginCallback(data) {
    setUserId(data.user_id);
    setUsername(data.username);
  }

  function logOutCallback() {
    setUserId("");
    setUsername("");
  }

  function signUpCallback(data) {
    setUserId(data.user_id);
    setUsername(data.username);
  }

  return (
    <Box>
      <Router>
        <Header username={username} logOutCallback={logOutCallback}/>
        <Routes>
          <Route path="/" element={userId ? <Todos userId={userId} /> : <HomePage loginCallback={loginCallback} />}/>
          <Route path="/login" element={userId ? <Todos userId={userId} /> : <HomePage loginCallback={loginCallback} />}/>
          <Route path="/signup" element={<SignUp signUpCallback={signUpCallback}/>}/>
          <Route path="*" element={<Navigate to={"/"} />} />
        </Routes>
      </Router>
      <Footer />
    </Box>
    );
}

export default App;
