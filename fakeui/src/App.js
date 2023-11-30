import logo from './logo.svg';
// import './App.css';
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import SearchNews from './Screens/Search';

function App() {
  return (
    <div className="App">
      <Router>
        <Routes>
          <Route exact path='/' element={<SearchNews/>}></Route>
        </Routes>
        
      </Router>
    </div>
  );
}

export default App;
