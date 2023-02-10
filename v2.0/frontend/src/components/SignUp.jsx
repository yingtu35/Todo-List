import React, { useState } from "react"
import { Flex, Box, Heading, ButtonGroup, Button, Input, Stack, useColorMode, Collapse, Alert, AlertDescription } from "@chakra-ui/react"
import { FormControl, FormLabel, FormHelperText } from "@chakra-ui/react";
import { useNavigate } from "react-router-dom";

function SignUp(props) {
    const navigate = useNavigate();

    const [username, setUsername] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [usernameError, setUsernameError] = useState(false);
    const [emailError, setEmailError] = useState(false);
    const [passwordError, setPasswordError] = useState(false);

    const [signupError, setSignupError] = useState(false);
    const [signupMsg, setSignupMsg] = useState('');
    
    const { colorMode, toggleColorMode } = useColorMode();
    const boxBg = { light: "gray.100", dark: "gray.400"};
    const inputBg = { light: "gray.200", dark: "gray.600" };

    async function handleSignUp() {
        if (username === "" || email === "" || password === ""){
            if (username === "") {
                setUsernameError(true);
            }
            if (email === "") {
                setEmailError(true);
            }
            if (password === "") {
                setPasswordError(true);
            }
            return;
        }

        const requestOptions = {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({
                "username": username,
                "email": email,
                "password": password,
            }),
        }
        
        const response = await fetch("http://localhost:8000/Sign-up", requestOptions);
        if (response.ok){
            const data = await response.json();
            // props.signUpCallback(data);
            // navigate("/");
        }else {
            const data = await response.json();
            setSignupError(true);
            setSignupMsg(data.detail);
        }
        return;
    }

    function handleBack() {
        navigate("/");
    }

    function handleUsernameInput(e) {
        setUsername(e.target.value);
        if (usernameError && username !== ""){
            setUsernameError(false);
        }

    }

    function handleEmailInput(e){
        setEmail(e.target.value);
        if (emailError && email !== ""){
            setEmailError(false);
        }
    }

    function handlePasswordInput(e){
        setPassword(e.target.value);
        if (passwordError && password !== ""){
            setPasswordError(false);
        }
    }

    return (
        <Flex align="center" justify="center" h="80vh">
            <Box p={5} borderWidth="1px" w="500px" rounded="lg" bg={boxBg[colorMode]}>
                <Stack spacing={3}>
                    <Heading as='h3' size='lg'>User Sign Up</Heading>
                    <Collapse in={signupError}>
                        <Alert status="error">
                            <AlertDescription>{signupMsg}</AlertDescription>
                        </Alert>
                    </Collapse>
                    <FormControl>
                        <FormLabel>Email</FormLabel>
                        <Input type='email' 
                                value={email}
                                placeholder="Email" 
                                bg={inputBg[colorMode]} 
                                onChange={handleEmailInput} />
                        {!emailError ? (null) : (<FormHelperText>Email is required.</FormHelperText>)}
                    </FormControl>
                    <FormControl>
                        <FormLabel>Username</FormLabel>
                        <Input type='text' 
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
                        <Button colorScheme="green" 
                                onClick={handleSignUp}>Sign up</Button>
                        <Button colorScheme="red"
                                onClick={handleBack}>Back</Button>
                    </ButtonGroup>
                </Stack>       
            </Box>
        </Flex>
    );
}

export default SignUp