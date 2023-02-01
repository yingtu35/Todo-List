import React, { useState } from "react"
import { Flex, Box, ButtonGroup, Button, Input, Stack, useColorMode, Heading } from "@chakra-ui/react"
import { useNavigate } from "react-router-dom";
import { FormControl, FormLabel, FormHelperText } from "@chakra-ui/react";

function HomePage(props) {
    const navigate = useNavigate();

    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [emailError, setEmailError] = useState(false);
    const [passwordError, setPasswordError] = useState(false);

    const { colorMode, toggleColorMode } = useColorMode();
    const boxBg = { light: "gray.100", dark: "gray.400"}
    const inputBg = { light: "gray.200", dark: "gray.600" };

    async function handleLogin(){
        if (email === "") {
            setEmailError(true);
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
                "email": email,
                "password": password,
            }),
        }
        
        const response = await fetch("http://localhost:8000/user/login", requestOptions);
        if (response.ok){
            const data = await response.json();
            props.loginCallback(data.user_id);
            navigate("/");
        }else {
            // TODO: Display error message to the screen
            const data = await response.json();
            console.log(data.detail);
        }

    }

    function handleSignUp() {
        navigate("/signup");
    }

    function handleEmailInput(e){
        setEmail(e.target.value);
        if (email !== ""){
            setEmailError(false);
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
            <Flex align="center" justify="center" h="80vh">
                <Box p={5} borderWidth="1px" w="500px" rounded="lg" bg={boxBg[colorMode]}>
                    <Stack spacing={3}>
                        <Heading as='h3' size='lg'>User Login</Heading>
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