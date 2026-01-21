import { useState } from 'react'
import { Routes, Route } from 'react-router-dom';
import Contract from './pages/ContractPage';
import LayoutMain from './layout/LayoutMain';
import HomePage from './pages/HomePage';


function App() {
  const [count, setCount] = useState(0)

  return (
    <>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route element={<LayoutMain />}>
          <Route path="/contract" element={<Contract />} />
        </Route>
    </Routes>
    </>
  )
}

export default App
