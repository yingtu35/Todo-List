import './App.css';
import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Link, Navigate} from "react-router-dom";
import Title from './components/Title';
import Footer from './components/Footer';
import HomePage from './components/HomePage';
import SignUp from './components/SignUp';
import { Box } from "@chakra-ui/react"
import Todos from './components/Todos';


function App() {
  const [userId, setUserId] = useState('');

  function loginCallback(id) {
    setUserId(id);
    // console.log(id);
  }

  function logOutCallback() {
    setUserId("");
  }

  function signUpCallback(id) {
    setUserId(id);
  }

  return (
    <Box>
      {/* TODO: Create a Header page that includes user information, login, logout button */}
      <Title />
      <Router>
        <Routes>
          <Route path="/" element={userId ? <Todos userId={userId} logOutCallback={logOutCallback} /> : <HomePage loginCallback={loginCallback} />}/>
          <Route path="/login" element={userId ? <Todos userId={userId} logOutCallback={logOutCallback} /> : <HomePage loginCallback={loginCallback} />}/>
          <Route path="/signup" element={<SignUp signUpCallback={signUpCallback}/>}/>
          <Route path="*" element={<Navigate to={"/"} />} />
        </Routes>
      </Router>
      <Footer />
    </Box>
    );
}

export default App;
