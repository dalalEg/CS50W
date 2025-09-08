import React, { useEffect, useState } from 'react';
import { fetchAdminDashboard }         from '../api/admin';
import '../styles/AdminDashboard.css';

export default function AdminDashboard() {
  const [data, setData]   = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);
  useEffect(() => {
    fetchAdminDashboard()
      .then(r => setData(r.data))
      .catch(e => setError(e.response?.data || 'Error'))
      .finally(() => setLoading(false));
  }, []);

  if (error) return <p className="error">Error: {JSON.stringify(error)}</p>;
  if (loading) return <p>Loading…</p>;
  if (!data) return <p>No data available</p>;
  
  const { users, bookings, revenue, movies, service_reviews } = data;
  const { funnel = {} } = users || {};
  const {
    repeat_customers,
    one_time_customers,
    auditorium_utilization
  } = bookings;
  const { trend_30d } = revenue;
  return (
    <div className="admin-dashboard">
      <h1>Admin Dashboard</h1>
      <div className="dashboard-grid">
        <section className="card">
          <h2>Users</h2>
          <p>New (7d): {users.new_7d}</p>
          <p>New (30d): {users.new_30d}</p>
          <p>Active: {users.active}</p>
          <p>Retention Rate: {(users.retention_rate * 100).toFixed(1)}%</p>
          <h3>Conversion Funnel</h3>
          <ul className="funnel-list">
            <li>Registered: {funnel.registered}</li>
            <li>Verified: {funnel.verified}</li>
            <li>Booked: {funnel.booked}</li>
            <li>Paid: {funnel.paid}</li>
          </ul>
          <h3>Top by Points</h3>
          <ul>
            {users.top_by_points.map(u =>
              <li key={u.id}>{u.username}: {u.total_points}</li>
            )}
          </ul>

          <h3>Growth Trend (30d)</h3>
          <ul>
            {users.growth_trend_30d.map(d =>
              <li key={d.day}>{d.day}: {d.count}</li>
            )}
          </ul>
        </section>
        <section className="card">
            <h2>Customer Segments</h2>
            <p>Repeat Customers: {repeat_customers}</p>
            <p>One-time Customers: {one_time_customers}</p>
        </section>

        <section className="card">
          <h2>Bookings</h2>
          <p>Total: {bookings.total}</p>
          <p>Pending: {bookings.pending}</p>
          <p>Confirmed: {bookings.confirmed}</p>
          <p>Cancelled: {bookings.cancelled}</p>
          <p>Attended: {bookings.attended}</p>
          <p>Avg Lead (h): {bookings.avg_lead_hours.toFixed(1)}</p>
          <p>Occupancy Rate: {(bookings.occupancy_rate * 100).toFixed(1)}%</p>

          <h3>By Day of Week</h3>
          <ul>
            {bookings.by_day_of_week.map(d =>
              <li key={d.dow}>
                {['Sun','Mon','Tue','Wed','Thu','Fri','Sat'][d.dow % 7]}: {d.count}
              </li>
            )}
          </ul>
        </section>

        <section className="card">
          <h2>Revenue</h2>
          <p>Total: ${revenue.total.toFixed(2)}</p>
          <p>Refunds: ${revenue.refunds.toFixed(2)}</p>
          <p>Failed: {revenue.failed_count}</p>

          <h3>By Movie</h3>
          <ul>
            {revenue.by_movie.map(m =>
              <li key={m.booking__showtime__movie__title}>
                {m.booking__showtime__movie__title}: ${m.revenue.toFixed(2)}
              </li>
            )}
          </ul>
        </section>

        <section className="card">
          <h2>Movies</h2>

          <h3>Top Booked</h3>
          <ul>
            {movies.top_booked.map(m =>
              <li key={m.title}>{m.title}: {m.bookings}</li>
            )}
          </ul>

          <h3>Top Rated</h3>
          <ul>
            {movies.top_rated.map(m =>
              <li key={m.movie__title}>
                {m.movie__title}: {m.avg.toFixed(2)} ({m.cnt} reviews)
              </li>
            )}
          </ul>

          <h3>Most Reviewed</h3>
          <ul>
            {movies.most_reviewed.map(m =>
              <li key={m.title}>{m.title}: {m.reviews}</li>
            )}
          </ul>

          <h3>Top Watchlisted</h3>
          <ul>
            {movies.top_watchlisted.map(m =>
              <li key={m.title}>{m.title}: {m.watchlisted}</li>
            )}
          </ul>
          <h3>Top Favorited</h3>
          <ul>
            {movies.top_favorited.map(m =>
              <li key={m.title}>{m.title}: {m.favorited}</li>
            )}
          </ul>
        </section>
        <section className="card">
          <h2>Auditorium Utilization</h2>
          <ul className="util-list">
            {auditorium_utilization.map(a => (
              <li key={a.auditorium_id}>
                {a.auditorium}: {(a.occupancy_rate * 100).toFixed(1)}%
              </li>
            ))}
          </ul>
        </section>
        <section className="card ">
          <h2>Service Reviews</h2>
          <h3>Avg Rating by Auditorium</h3>
          <ul>
            {service_reviews.by_auditorium.map(a => (
              <li key={a.auditorium_id}>
                {a.auditorium}: {a.average_rating.toFixed(1)}
              </li>
            ))}
          </ul>
          <h3>Avg Rating by Theater</h3>
          <ul>
            {service_reviews.by_theater.map(t => (
              <li key={t.theater_id}>
                {t.theater}: {t.average_rating.toFixed(1)}
              </li>
            ))}
          </ul>
        </section>
        <section className="card">
          <h2>Revenue Trend (30d)</h2>
          <ul className="trend-list">
            {trend_30d.map(r => (
              <li key={r.day}>
                {r.day}: ${r.total.toFixed(2)}
              </li>
            ))}
          </ul>
        </section>
      </div>
    </div>
  );
}
