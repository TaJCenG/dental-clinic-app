import React, { useState } from 'react';

const DateTimePicker = ({ onSlotSelect }) => {
  const [date, setDate] = useState('');
  const [startTime, setStartTime] = useState('09:00');
  const [endTime, setEndTime] = useState('09:30');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!date || !startTime || !endTime) {
      alert('Please select date and times');
      return;
    }
    if (endTime <= startTime) {
      alert('End time must be after start time');
      return;
    }
    // Send the local time strings directly (no conversion)
    const startDateTime = `${date}T${startTime}:00`;
    const endDateTime = `${date}T${endTime}:00`;
    onSlotSelect({ start: startDateTime, end: endDateTime });
  };

  return (
    <div style={{ maxWidth: '400px', margin: '0 auto' }}>
      <h3>Select Appointment Time</h3>
      <form onSubmit={handleSubmit}>
        <div style={{ marginBottom: '15px' }}>
          <label htmlFor="date">Date: </label>
          <input
            type="date"
            id="date"
            value={date}
            onChange={(e) => setDate(e.target.value)}
            required
            style={{ width: '100%', padding: '8px' }}
          />
        </div>
        <div style={{ marginBottom: '15px' }}>
          <label htmlFor="startTime">Start Time: </label>
          <input
            type="time"
            id="startTime"
            value={startTime}
            onChange={(e) => setStartTime(e.target.value)}
            step="1800"  // 30-minute increments
            required
            style={{ width: '100%', padding: '8px' }}
          />
        </div>
        <div style={{ marginBottom: '15px' }}>
          <label htmlFor="endTime">End Time: </label>
          <input
            type="time"
            id="endTime"
            value={endTime}
            onChange={(e) => setEndTime(e.target.value)}
            step="1800"
            required
            style={{ width: '100%', padding: '8px' }}
          />
        </div>
        <button type="submit" style={{ padding: '10px 20px', width: '100%' }}>
          Check Availability & Continue
        </button>
      </form>
    </div>
  );
};

export default DateTimePicker;