import { render, screen } from '@testing-library/react'
import App from '../App'

test('renders JobLink app', () => {
  render(<App />)
  expect(screen.getByText('JobLink')).toBeInTheDocument()
})