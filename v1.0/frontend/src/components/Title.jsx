import React from "react"
import { Box, Heading, Text, Link } from "@chakra-ui/react"

function Title() {
    return (
        <Box p={1} mb={2} bg="gray.400" textAlign="center">
            <Heading as="h1" noOfLines={1}>
                Todo List
            </Heading>
        </Box>
    );
}

export default Title