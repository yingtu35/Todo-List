import React, { useRef } from "react"
import { Box, Input, Button, InputGroup, Stack, Text, ButtonGroup, useDisclosure, FormControl, FormLabel, FormHelperText, FormErrorMessage } from "@chakra-ui/react"
import { Modal, ModalOverlay, ModalHeader, ModalCloseButton, ModalContent, ModalBody, ModalFooter} from "@chakra-ui/react"
import { useState, useEffect } from "react"
import { useNavigate } from "react-router-dom"

const TodosContext = React.createContext({
    todos: [],
    getCurrentTodos: () => {}
})

function Addtodo(props) {
    const [userId, setUserId] = useState(props.userId || null);
    const [item, setItem] = useState("")
    const [isError, setIsError] = useState(false);
    const {todos, getCurrentTodos} = React.useContext(TodosContext)

    function handleInput(event) {
        setItem(event.target.value);
        setIsError(false);
    }
    async function handleSubmit() {
        if (item) {
            const requestOptions = {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({
                    "item": item,
                    "owner_id": userId,
                }),
            }

            await fetch("http://localhost:8000/item", requestOptions);
            getCurrentTodos();
            setItem("");
        }
        else {
            setIsError(true);
        }
    }

    return (
        <FormControl>
            <FormLabel>Todo</FormLabel>
            <InputGroup>
                <Input 
                    type="text"
                    placeholder="Enter here"
                    value={item}
                    autoFocus={true}
                    onChange={handleInput}
                />
                <Button colorScheme="blue" onClick={handleSubmit}>Submit</Button>
            </InputGroup>
            {isError? (
                <FormHelperText>
                    Input is required.
                </FormHelperText>
            )
            : (
                <FormHelperText>
                    Write down what to do.
                </FormHelperText>
            )
            }
            
        </FormControl>
            
    )
}

function Todo(props){
    const [id, setId] = useState(props.id || null);
    const [item, setItem] = useState(props.item || null);
    const [userId, setUserId] = useState(props.userId || null);
    const {todos, getCurrentTodos} = React.useContext(TodosContext);
    const { isOpen, onOpen, onClose } = useDisclosure();
    const inputRef = useRef();

    async function handleUpdate(){
        if (inputRef.current.value) {
            const requestOptions = {
                method: "PUT",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({
                    "item": inputRef.current.value,
                    "owner_id": userId
                }),
            }

            await fetch(`http://localhost:8000/item/${id}`, requestOptions);
            getCurrentTodos();
            onClose();
        }
    }

    async function handleDelete(){
        const requestOptions = {
            method: "DELETE",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({
                "owner_id": userId
            }),
        }

        await fetch(`http://localhost:8000/item/${id}`, requestOptions);
        getCurrentTodos();
    }


    useEffect(() => {
        setId(props.id);
        setItem(props.item);
    }, [props.id, props.item])

    return (
        <Box p={1}>
            <Text fontSize='md'>{item}</Text>
            <ButtonGroup gap={4}>
                <Button colorScheme='blue' size='sm' onClick={onOpen}>Edit</Button>
                <Button colorScheme='red' size='sm' onClick={handleDelete}>Delete</Button>
            </ButtonGroup>

            <Modal isOpen={isOpen} onClose={onClose}>
                <ModalOverlay />
                <ModalContent>
                    <ModalHeader>Update Todo Item</ModalHeader>
                    <ModalCloseButton />
                    <ModalBody>
                        <Input 
                            placeholder="Enter here"
                            defaultValue={item}
                            ref={inputRef}
                            autoFocus={true}
                        />
                    </ModalBody>

                    <ModalFooter>
                        <Button colorScheme="blue" onClick={handleUpdate}>Update</Button>
                    </ModalFooter>
                </ModalContent>
            </Modal>
        </Box>
    )
}

function Todos(props){
    const navigate = useNavigate();

    const [todos, setTodos] = useState([]);
    const [userId, setUserId] = useState(props.userId || -1);

    async function getCurrentTodos() {
        const response = await fetch(`http://localhost:8000/item/${userId}`);
        const data = await response.json();
        setTodos(data.todos);
    }

    function handleLogOut() {
        props.logOutCallback();
        navigate('/login');
    }

    useEffect(() => {
      getCurrentTodos()
    }, [])

    return (
        <TodosContext.Provider value={{todos, getCurrentTodos}}>
            {/* // TODO: Display user information and log out button in the header, not here */}
            <Button colorScheme="red" onClick={handleLogOut}>Log out</Button>
            <Addtodo userId={userId} />
            <Stack spacing={4} mt={1}>
                {todos.map((element) => (
                    <Todo id={element.id} item={element.item} userId={userId} />
                ))}
            </Stack>
        </TodosContext.Provider>
    )
}

export default Todos