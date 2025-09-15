import { api,fetchCSRFToken } from './axios';

export const fetchNotifications  = () => api.get('/api/notifications/');
export const markNotificationRead = async id => {
  await fetchCSRFToken();
  return await api.patch(`/api/notifications/${id}/`, {
    is_read: true
  });
};
export const markAllNotificationsRead = async () => {
  await fetchCSRFToken();
  return await api.patch('/api/notifications/mark-all-read/', {
    is_read: true
  });
};