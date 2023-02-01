import './App.css';
import Title from "./components/Title"
import Todos from "./components/Todos"
import Footer from "./components/Footer"
import { Box } from "@chakra-ui/react"


function App() {
  return (
    <Box>
      <Title />
      <Todos />
      <Footer />
    </Box>
    
    
    );
}

export default App;
