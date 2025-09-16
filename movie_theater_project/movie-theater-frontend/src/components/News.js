import React, { useState, useEffect } from 'react';
import { fetchNews } from '../api/news';
import '../styles/News.css';  // Create this CSS file if needed

const News = () => {
  const [news, setNews] = useState([]);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const pageSize = 10;  // Adjust as needed

  useEffect(() => {
    fetchNewsData(currentPage);
  }, [currentPage]);

  const fetchNewsData = async (page) => {
    setLoading(true);
    try {
      const response = await fetchNews(page, pageSize);
      setNews(response.data.results || response.data);
      setTotalPages(Math.ceil((response.data.count || 0) / pageSize));
      setError(null);
    } catch {
      setError('Failed to load news');
    } finally {
      setLoading(false);
    }
  };

  const handlePageChange = (page) => {
    if (page >= 1 && page <= totalPages) {
      setCurrentPage(page);
    }
  };

  if (loading) return <p>Loading news...</p>;
  if (error) return <p>{error}</p>;

  return (
    <div className="news">
      <h2>Latest News</h2>
      <ul>
        {news.length === 0 && <p>No news available.</p>}
        {news.map(item => (
          <li key={item.id}>
            <h3>{item.title}</h3>
            <div style={{whiteSpace: 'pre-line', display: 'flex', alignItems: 'center' }}>
            <p>{item.content}</p>
            </div>
            
            <p><strong>Published:</strong> {new Date(item.published_at).toLocaleString()}</p>
          </li>
        ))}
      </ul>
      {/* Pagination Controls */}
      <div className="pagination">
        <button onClick={() => handlePageChange(currentPage - 1)} disabled={currentPage === 1}>
          Previous
        </button>
        <span>Page {currentPage} of {totalPages}</span>
        <button onClick={() => handlePageChange(currentPage + 1)} disabled={currentPage === totalPages}>
          Next
        </button>
      </div>
    </div>
  );
};

export default News;
