import React from 'react';
import { render, screen } from '@testing-library/react';
import App from './App';

// Mock the useAuth hook
jest.mock('./contexts/AuthContext', () => ({
  useAuth: () => ({
    user: { name: 'Test User' },
    loading: false,
    logout: jest.fn(),
  }),
}));

// Mock the useNotifications hook
jest.mock('./contexts/NotificationContext', () => ({
  useNotifications: () => ({
    notes: [{ id: 1, is_read: false }],
  }),
}));

test('renders the header and navigation links', () => {
  render(<App />);
  // Check for the header
  expect(screen.getByText(/🎬 Dali Movie Theater/i)).toBeInTheDocument();
  // Check for navigation links
  expect(screen.getByText(/All Movies/i)).toBeInTheDocument();
  expect(screen.getByText(/Available Showtimes/i)).toBeInTheDocument();
  expect(screen.getByText(/Our Theaters/i)).toBeInTheDocument();
  expect(screen.getByText(/Profile/i)).toBeInTheDocument();
});
