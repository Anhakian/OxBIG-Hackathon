import './App.css'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import HomePage from './routes/Homepage'
import MoodChat from './moodchat/page.js'

function App() {
  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/chat/mood" element={<MoodChat />} />
        </Routes>
      </div>
    </Router>
  )
}

export default App
