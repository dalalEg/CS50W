import {api} from './axios';

export const fetchNews = () => api.get('/api/news/');