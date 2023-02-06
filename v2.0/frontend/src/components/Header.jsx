import React from "react"
import pic from "../images/logo.png"
import { useNavigate } from "react-router-dom";
import { MdAccountCircle, MdEmail, MdOutlineLightMode, MdOutlineNightlight } from "react-icons/md"
import { Menu, MenuButton, MenuList, MenuItem, MenuDivider, Button, ButtonGroup, Flex, Text, Image, useColorMode} from "@chakra-ui/react"

function Header(props) {
    const navigate = useNavigate();

    const { colorMode, toggleColorMode } = useColorMode();
    const flexBg = { light: "gray.400", dark: "gray.600"};
    const buttonBg = { light: "gray.400", dark: "gray.600" }
    function handleLogOut() {
        props.logOutCallback();
        navigate('/login');
    }

    return (
        <Flex style={{ display: "grid", justifySelf: "end", padding: "10px" }} bg={flexBg[colorMode]}>
            {/* TODO: Adjust the alignment of Image and ButtonGroup, and move the title to the header */}
            <Image boxSize="50px" src={pic} alt="todo-list logo" />
            <ButtonGroup justifyContent="right">
                {colorMode === "dark" ?
                <Button size="md" 
                        leftIcon={<MdOutlineNightlight />} 
                        onClick={toggleColorMode}
                        bg={buttonBg[colorMode]}>
                            Dark Mode
                </Button> 
                :
                <Button size="md" 
                        leftIcon={<MdOutlineLightMode />} 
                        onClick={toggleColorMode}
                        bg={buttonBg[colorMode]}
                        >
                            Light Mode
                </Button>
                }
                <Button leftIcon={<MdEmail />}
                        size="md"
                        as="a"
                        href="mailto:yingtu35@gmail.com?subject=Reporting%20Issues%20on%20Todo-List%20App&body=Issues:%20"
                        bg={buttonBg[colorMode]}>
                            Report
                </Button>
                {props.username?
                <Menu>
                    <MenuButton
                        as={Button}
                        px={4}
                        py={2}
                        transition='all 0.2s'
                        borderRadius='md'
                        borderWidth='1px'
                        size="md"
                        leftIcon={<MdAccountCircle />}
                        _hover={{ bg: 'gray.200' }}
                        _expanded={{ bg: 'blue.400' }}
                        _focus={{ boxShadow: 'outline' }}
                        
                    >
                    {props.username}
                    </MenuButton>
                    <MenuList>
                        <Flex align="center" justify="center">
                            <MdAccountCircle size="36px"/>
                            <Text>{props.username}</Text>
                        </Flex>
                        <MenuItem>Settings</MenuItem>
                        <MenuDivider />
                        <MenuItem onClick={handleLogOut}>Log Out</MenuItem>
                    </MenuList>
                </Menu>
                :
                // <Button leftIcon={<MdAccountCircle />} size="sm">Login</Button>
                (null)}
                
            </ButtonGroup>
        </Flex>

    )
}

export default Header