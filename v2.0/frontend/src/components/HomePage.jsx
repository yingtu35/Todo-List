import React, { useState } from "react"
import { Flex, Box, ButtonGroup, Button, Input, Stack, useColorMode, Heading, Collapse, Alert, AlertDescription } from "@chakra-ui/react"
import { useNavigate } from "react-router-dom";
import { FormControl, FormLabel, FormHelperText } from "@chakra-ui/react";

function HomePage(props) {
    const navigate = useNavigate();

    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [usernameError, setUsernameError] = useState(false);
    const [passwordError, setPasswordError] = useState(false);

    const [loginError, setLoginError] = useState(false);
    const [loginMsg, setLoginMsg] = useState("");

    const { colorMode, toggleColorMode } = useColorMode();
    const boxBg = { light: "gray.100", dark: "gray.400"}
    const inputBg = { light: "gray.200", dark: "gray.600" };

    async function handleLogin(){
        if (username === "") {
            setUsernameError(true);
            return;
        }
        if (password === "") {
            setPasswordError(true);
            return;
        }

        const requestOptions = {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({
                "username": username,
                "password": password,
            }),
        }
        
        const response = await fetch("http://localhost:8000/login", requestOptions);
        if (response.ok){
            const data = await response.json();
            props.loginCallback(data);
            navigate("/");
        }else {
            const data = await response.json();
            setLoginError(true);
            setLoginMsg(data.detail);
        }

    }

    function handleSignUp() {
        navigate("/signup");
    }

    function handleUsernameInput(e){
        setUsername(e.target.value);
        if (username !== ""){
            setUsernameError(false);
        }
    }

    function handlePasswordInput(e){
        setPassword(e.target.value);
        if (password !== ""){
            setPasswordError(false);
        }
    }

    return (
        <Box>
            <Flex align="center" justify="center" h="75vh">
                <Box p={5} borderWidth="1px" w="500px" rounded="lg" bg={boxBg[colorMode]}>
                    <Stack spacing={3}>
                        <Heading as='h3' size='lg'>User Login</Heading>
                        <Collapse in={loginError}>
                            <Alert status="error">
                                <AlertDescription>{loginMsg}</AlertDescription>
                            </Alert>
                        </Collapse>
                        <FormControl>
                            <FormLabel>Username</FormLabel>
                            <Input type='text'
                                   autoFocus 
                                   value={username}
                                   placeholder="Username" 
                                   bg={inputBg[colorMode]} 
                                   onChange={handleUsernameInput} />
                            {!usernameError ? (null) : (<FormHelperText>Username is required.</FormHelperText>)}
                        </FormControl>
                        <FormControl>
                            <FormLabel>Password</FormLabel>
                            <Input type='password' 
                                   value={password}
                                   placeholder="Password" 
                                   bg={inputBg[colorMode]}  
                                   onChange={handlePasswordInput} />
                            {!passwordError ? (null) : (<FormHelperText>Password is required.</FormHelperText>)}
                        </FormControl>
                        <ButtonGroup justifyContent="right">
                            <Button colorScheme="cyan" 
                                    onClick={handleLogin}>Login</Button>
                            <Button colorScheme="green" onClick={handleSignUp}>Sign up</Button>
                        </ButtonGroup>
                    </Stack>       
                </Box>
            </Flex>
        </Box>
    )
}

export default HomePage