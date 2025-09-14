import React, { useEffect, useState } from 'react';
import { fetchNews } from '../api/news';
import './News.css';

const News = () => {
  const [news, setNews] = useState([]);

  useEffect(() => {
    // Fetch news data from the API
    fetchNews()
      .then(response => {
        setNews(response.data);
      })
      .catch(error => {
        console.error('Error fetching news:', error);
      });
  }, []);

  return (
    <div className="news-container">
      <h2>Latest News</h2>
      {news.length > 0 ? (
        <ul>
          {news.map((item, index) => (
            <li key={index} className="news-item">
              <h3>{item.title}</h3>
              <div style={{ whiteSpace: 'pre-line' }}>
                {item.content}
              </div>
            </li>
          ))}
        </ul>
      ) : (
        <p>No news available at the moment.</p>
      )}
    </div>
  );
};

export default News;
