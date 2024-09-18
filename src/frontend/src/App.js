import './App.css';
import Login from "./pages/Login.js"
import Panel from "./pages/Panel.js"
import {BrowserRouter as Router,Routes,Route} from "react-router-dom"
function App() {
  return (
    <div>
      <Router>
        <Routes>
          <Route path="/" element={<Login/>} />
          <Route path="/panel" element={<Panel/>} />
        </Routes>
      </Router>

    </div>
  );
}

export default App;
