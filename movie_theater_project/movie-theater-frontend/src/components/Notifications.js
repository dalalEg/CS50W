import { useNotifications } from '../contexts/NotificationContext';
import '../styles/Notifications.css';
export default function NotificationsList() {
  const { notes, markRead } = useNotifications();
  return (
    <div className="notifications-container">
    <ul className="notifications-list">
      {notes.map(n => (
        <li key={n.id} className={n.is_read ? 'read' : 'unread'}>
          <p className='message'>{n.message}</p>
          {!n.is_read && (
            <button onClick={() => markRead(n.id)}>Mark read</button>
          )}
        </li>
      ))}
    </ul>
  </div>
  );
}