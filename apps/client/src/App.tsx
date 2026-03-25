import { BrowserRouter } from 'react-router-dom'
import { AppRoutes } from './router'
import { Layout } from './components/Layout'
import './App.css'

function App() {
  return (
    <BrowserRouter>
      <Layout>
        <AppRoutes />
      </Layout>
    </BrowserRouter>
  )
}

export default App
