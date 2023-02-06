import React from "react"
import {FaGithub, FaFacebook, FaLinkedin, FaInstagram} from "react-icons/fa"
import { Box, Text, Button } from "@chakra-ui/react"

function Footer() {

    function handleClick(href) {
        window.location.href = href;
    }

    return (
        <Box 
            position="fixed"
            bottom={0}
            left={0}
            width="100%"
            backgroundColor="gray.400"
            p={4}
            textAlign="center"
        >
            <Text>Copyright © 2023 Ying Tu. All rights reserved</Text>
            <Button variant="ghost"
                    onClick={() => handleClick("https://github.com/yingtu35")}>
                <FaGithub size="24px" />
            </Button>
            <Button colorScheme="linkedin"
                    variant="ghost"
                    onClick={() => handleClick("https://www.linkedin.com/in/ying-tu-06b208102/")}>
                <FaLinkedin size="24px" />
            </Button>
            <Button colorScheme="facebook"
                    variant="ghost"
                    onClick={() => handleClick("https://www.facebook.com/profile.php?id=100000582214483")}>
                <FaFacebook size="24px" />
            </Button>
            <Button colorScheme="pink"
                    variant="ghost"
                    onClick={() => handleClick("https://www.instagram.com/orevo860305/")}>
                <FaInstagram size="24px" />
            </Button>
        </Box>
    )
}

export default Footer