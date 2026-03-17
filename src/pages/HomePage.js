import React from 'react';
import { useNavigate } from 'react-router-dom';
import DateTimePicker from '../components/DateTimePicker';

const HomePage = () => {
  const navigate = useNavigate();

  const handleSlotSelect = (slot) => {
    // Navigate to booking page with the selected slot
    navigate('/book', { state: { slot } });
  };

  return (
    <div>
      <h1 style={{ textAlign: 'center' }}>Dental Clinic Booking</h1>
      <DateTimePicker onSlotSelect={handleSlotSelect} />
    </div>
  );
};

export default HomePage;