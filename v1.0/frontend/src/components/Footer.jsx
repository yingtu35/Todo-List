import React from "react"
import { Box, Text, Link } from "@chakra-ui/react"

function Footer() {
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
            <Text>Follow me on:</Text>
            <Link href='https://github.com/yingtu35' color="blue" isExternal mr={1}>
                GitHub
            </Link>
            <Link href='https://www.linkedin.com/in/yingtu/' color="blue" isExternal>
                Linkedin
            </Link>
        </Box>
    )
}

export default Footer