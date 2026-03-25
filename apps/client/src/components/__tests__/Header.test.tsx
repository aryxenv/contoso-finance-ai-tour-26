import { render, screen } from '@testing-library/react'
import { MemoryRouter } from 'react-router-dom'
import { FluentProvider, teamsLightTheme } from '@fluentui/react-components'
import { Header } from '../Header'

function renderWithProviders(ui: React.ReactElement) {
  return render(
    <FluentProvider theme={teamsLightTheme}>
      <MemoryRouter>{ui}</MemoryRouter>
    </FluentProvider>,
  )
}

describe('Header', () => {
  it('renders the application title', () => {
    renderWithProviders(<Header />)

    expect(screen.getByText('Contoso Finance')).toBeInTheDocument()
  })

  it('renders the GitHub repository link', () => {
    renderWithProviders(<Header />)

    const link = screen.getByRole('link', { name: /github repository/i })
    expect(link).toHaveAttribute('href', 'https://github.com/aryxenv/contoso-finance')
    expect(link).toHaveAttribute('target', '_blank')
  })

  it('renders with noopener noreferrer for security', () => {
    renderWithProviders(<Header />)

    const link = screen.getByRole('link', { name: /github repository/i })
    expect(link).toHaveAttribute('rel', 'noopener noreferrer')
  })
})
