import { Route, Routes } from 'react-router-dom';

import Navbar from './components/Navbar/Navbar';
import Home from './pages/Home';
import About from './pages/About';
import Login from './pages/login';
import Leaderboard from './pages/Leaderboard';

import 'bootstrap/dist/css/bootstrap.min.css'

function App() {
  return (
    <>
      <Navbar />
      <Routes >
        <Route path="/" element={<Home /> }/>
        <Route path="/about" element={<About />}/>
        <Route path="/login" element={<Login />}/>
        <Route path="/leaderboard" element={<Leaderboard />}/>
      </Routes>
    </>
  );
}

export default App;
