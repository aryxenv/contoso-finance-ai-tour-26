import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { FluentProvider } from '@fluentui/react-components'
import { contosoTheme } from './theme'
import App from './App'

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <FluentProvider theme={contosoTheme}>
      <App />
    </FluentProvider>
  </StrictMode>,
)
