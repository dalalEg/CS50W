import { api } from './axios';

export const fetchNotifications  = () => api.get('/api/notifications/');
export const markNotificationRead = id => api.patch(`/api/notifications/${id}/`, {
  is_read: true
});
export const markAllNotificationsRead = () => api.patch('/api/notifications/mark-all-read/', {
  is_read: true
});