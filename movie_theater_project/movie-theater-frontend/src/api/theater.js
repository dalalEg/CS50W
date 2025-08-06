// src/api/movies.js
import { api} from './axios';

export const fetchTheaters = () => api.get('/api/theaters/');
export const fetchTheaterById = id => api.get(`/api/theaters/${id}/`);
export const fetchTheaterByName = name => api.get(`/api/theaters/name/${name}/`);
export const fetchTheaterByLocation = (city, state) => 
  api.get(`/api/theaters/location/${city}/${state}/`);