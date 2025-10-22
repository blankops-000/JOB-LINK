import React from 'react';
import { render, screen } from '@testing-library/react';
import App from './App';

test('renders JobLink homepage', () => {
  render(<App />);
  const welcomeElement = screen.getByText(/welcome to joblink/i);
  expect(welcomeElement).toBeInTheDocument();
});
