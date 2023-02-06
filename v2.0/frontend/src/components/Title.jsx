import React from "react"
import { Box, Heading, useColorMode, Stack, Text, Switch } from "@chakra-ui/react"

function Title() {
    const { colorMode, toggleColorMode } = useColorMode();

    return (
        <Box p={1} mb={2}  textAlign="center">
            <Heading as="h1" size='2xl' noOfLines={1}>
                Todo List
            </Heading>
            {/* <Stack direction="row" spacing={3} justifyContent="center" mt={2}>
                <Text as='b'>Light</Text>
                <Switch isChecked={colorMode === 'dark'} onChange={toggleColorMode} />
                <Text as='b'>Dark</Text>
            </Stack> */}
        </Box>
    );
}

export default Title