import React from 'react';

export default function ConfirmDialog({ message, onYes, onNo }) {
  return (
    <div className="confirm-backdrop">
      <div className="confirm-box">
        <p>{message}</p>
        <button onClick={onYes} className="btn btn-primary">Yes</button>
        <button onClick={onNo}  className="btn btn-secondary">No</button>
      </div>
    </div>
  );
}