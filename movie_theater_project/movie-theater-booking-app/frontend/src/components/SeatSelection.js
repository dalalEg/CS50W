import React, { useState } from 'react';

const SeatSelection = ({ seats, onSeatSelect }) => {
    const [selectedSeats, setSelectedSeats] = useState([]);

    const handleSeatClick = (seat) => {
        const isSelected = selectedSeats.includes(seat);
        const newSelectedSeats = isSelected 
            ? selectedSeats.filter(s => s !== seat) 
            : [...selectedSeats, seat];

        setSelectedSeats(newSelectedSeats);
        onSeatSelect(newSelectedSeats);
    };

    return (
        <div className="seat-selection">
            <h2>Select Your Seats</h2>
            <div className="seats">
                {seats.map(seat => (
                    <div 
                        key={seat.id} 
                        className={`seat ${selectedSeats.includes(seat) ? 'selected' : ''}`} 
                        onClick={() => handleSeatClick(seat)}
                    >
                        {seat.number}
                    </div>
                ))}
            </div>
            <div className="selected-seats">
                <h3>Selected Seats:</h3>
                {selectedSeats.map(seat => (
                    <span key={seat.id}>{seat.number} </span>
                ))}
            </div>
        </div>
    );
};

export default SeatSelection;