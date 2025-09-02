// src/tests/MovieList.test.js
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import MovieList from '../components/MovieList';
import * as moviesApi from '../api/movies';
import * as genreApi from '../api/genre';
import { BrowserRouter } from 'react-router-dom';

// Mock navigate
const mockedNavigate = jest.fn();
jest.mock('react-router-dom', () => ({
  ...jest.requireActual('react-router-dom'),
  useNavigate: () => mockedNavigate,
}));

// Mock API calls
jest.mock('../api/movies');
jest.mock('../api/genre');

describe('MovieList Component', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

 test('renders movies and handles search', async () => {
  // Mock genre API
  genreApi.fetchGenres.mockResolvedValue({ data: [{ id: 1, name: 'Action' }] });

  // Mock movies API
  moviesApi.fetchMovies.mockResolvedValue({
    data: [
      { id: 1, title: 'Movie One', release_date: '2023-01-01', rating: 8.5, duration: '02:00', genres: [{ id: 1 }], description: 'Desc 1', poster: '', trailer: '' },
      { id: 2, title: 'Movie Two', release_date: '2022-05-10', rating: 7.0, duration: '01:45', genres: [{ id: 1 }], description: 'Desc 2', poster: '', trailer: '' },
    ],
  });

  render(
    <BrowserRouter>
      <MovieList />
    </BrowserRouter>
  );

  // Wait for movies to appear
  await waitFor(() => {
    expect(screen.getByText('Movie One')).toBeInTheDocument();
    expect(screen.getByText('Movie Two')).toBeInTheDocument();
  });

  // Test search input
  const searchInput = screen.getByPlaceholderText(/search by title or keyword/i);
  fireEvent.change(searchInput, { target: { value: 'Movie One' } });

  // Wait for the filtering logic to complete
  await waitFor(() => {
    expect(screen.getByText('Movie One')).toBeInTheDocument();
    expect(screen.queryByText('Movie Two')).toBeInTheDocument();
  });
});
});
