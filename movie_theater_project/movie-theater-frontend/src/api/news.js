import { api } from './axios';

// Fetch news with pagination
export const fetchNews = (page = 1, pageSize = 10) =>
  api.get(`/api/news/?page=${page}&page_size=${pageSize}`);