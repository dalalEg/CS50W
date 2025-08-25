import { api } from './axios';

export function fetchAdminDashboard() {
  return api.get('api/admin/dashboard/');
}
