import React, { useRef } from "react"
import { Box, Input, Button, InputGroup, Stack, Text, ButtonGroup, useDisclosure, FormControl, FormLabel, FormHelperText, FormErrorMessage } from "@chakra-ui/react"
import { Modal, ModalOverlay, ModalHeader, ModalCloseButton, ModalContent, ModalBody, ModalFooter} from "@chakra-ui/react"
import { useState, useEffect } from "react"

const TodosContext = React.createContext({
    todos: [],
    getCurrentTodos: () => {}
})

function Addtodo(props) {
    const [item, setItem] = useState("")
    const [isError, setIsError] = useState(false);
    const {todos, getCurrentTodos} = React.useContext(TodosContext)

    function handleInput(event) {
        setItem(event.target.value);
        setIsError(false);
    }
    async function handleSubmit() {
        if (item) {
            const token = localStorage.getItem("token");
            const requestOptions = {
                method: "POST",
                headers: {
                    "Content-Type": "application/json", 
                    "Authorization": "Bearer " + token},
                body: JSON.stringify({
                    "item": item,
                }),
            }

            await fetch(`http://localhost:8000/items`, requestOptions);
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
            ) : (
                <FormHelperText>
                    Write down what to do.
                </FormHelperText>
            )}
        </FormControl>
            
    )
}

function Todo(props){
    const [id, setId] = useState(props.id || null);
    const [item, setItem] = useState(props.item || null);
    const {todos, getCurrentTodos} = React.useContext(TodosContext);
    const { isOpen, onOpen, onClose } = useDisclosure();
    const inputRef = useRef();

    async function handleUpdate(){
        if (inputRef.current.value) {
            const token = localStorage.getItem("token");
            const requestOptions = {
                method: "PUT",
                headers: {
                    "Content-Type": "application/json", 
                    "Authorization": "Bearer " + token},
                body: JSON.stringify({
                    "item": inputRef.current.value,
                }),
            }

            await fetch(`http://localhost:8000/items/${id}`, requestOptions);
            getCurrentTodos();
            onClose();
        }
    }

    async function handleDelete(){
        const token = localStorage.getItem("token");
        const requestOptions = {
            method: "DELETE",
            headers: {"Content-Type": "application/json",
                "Authorization": "Bearer " + token},
        }

        await fetch(`http://localhost:8000/items/${id}`, requestOptions);
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

    const [todos, setTodos] = useState([]);

    async function getCurrentTodos() {
        const token = localStorage.getItem("token");
        const response = await fetch(`http://localhost:8000/items`, {
            method: "GET",
            headers: {"accept": "application/json", 
                    "Authorization": "Bearer " + token}
        });
        const data = await response.json();
        setTodos(data.todos);
    }

    useEffect(() => {
      getCurrentTodos()
    }, [])

    return (
        <TodosContext.Provider value={{todos, getCurrentTodos}}>
            <Addtodo />
            <Stack spacing={4} mt={1}>
                {todos?
                    todos.map((element) => (
                    <Todo id={element.id} item={element.item} />
                )) : 
                null
                }
            </Stack>
        </TodosContext.Provider>
    )
}

export default Todos