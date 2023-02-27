import './App.css';
import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Link, Navigate} from "react-router-dom";
import Header from './components/Header'
import Footer from './components/Footer';
import HomePage from './components/HomePage';
import SignUp from './components/SignUp';
import { Box } from "@chakra-ui/react"
import Todos from './components/Todos';

// TODO: Should send request with a token to automatically login
function App() {
  const [username, setUsername] = useState('');

  function loginCallback(data) {
    setUsername(data.username);
  }

  function logOutCallback() {
    setUsername("");
  }

  function signUpCallback(data) {
    // setUserId(data.user_id);
    // setUsername(data.username);
    return
  }

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (token){
      fetch("http://localhost:8000/user", {
            method: "GET",
            headers: {"accept": "application/json", 
                    "Authorization": "Bearer " + token}
        })
        .then(response => response.json())
        .then((data) => {
          if (data.user){
            setUsername(data.user.username);
          }
          else {
            setUsername("");
          }})
    }
  })

  return (
    <Box className='container'>
      <Router>
        <Header username={username} logOutCallback={logOutCallback}/>
        <Routes>
          <Route path="/" element={username ? <Todos /> : <HomePage loginCallback={loginCallback} />}/>
          <Route path="/login" element={username ? <Todos /> : <HomePage loginCallback={loginCallback} />}/>
          <Route path="/signup" element={<SignUp signUpCallback={signUpCallback}/>}/>
          <Route path="*" element={<Navigate to={"/"} />} />
        </Routes>
      </Router>
      <Footer />
    </Box>
    );
}

export default App;
