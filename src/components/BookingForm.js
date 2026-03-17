import React, { useState } from 'react';
import api from '../services/api';

const BookingForm = ({ selectedSlot, onBookingComplete }) => {
  const [formData, setFormData] = useState({
    name: '',
    phone: '',
    email: ''
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
  e.preventDefault();
  setLoading(true);
  setError('');

  try {
    const response = await api.post('/appointments/', {
      patient: formData,
      slot: {
        start_time: selectedSlot.start,
        end_time: selectedSlot.end
      }
    });console.log('Sending booking request:', {
  patient: formData,
  slot: {
    start_time: selectedSlot.start,
    end_time: selectedSlot.end
  }
});
    onBookingComplete(response.data);
  } catch (error) {
    console.error('Booking error:', error.response?.data); // Log for debugging
    let errorMsg = 'Booking failed';
    if (error.response?.data?.detail) {
      const detail = error.response.data.detail;
      if (Array.isArray(detail)) {
        // Validation error array from FastAPI
        errorMsg = detail.map(err => err.msg).join(', ');
      } else if (typeof detail === 'string') {
        errorMsg = detail;
      }
    }
    setError(errorMsg);
  } finally {
    setLoading(false);
  }
};

  return (
    <form onSubmit={handleSubmit}>
      <h3>Enter Your Details</h3>
      <input
        type="text"
        name="name"
        placeholder="Full Name"
        value={formData.name}
        onChange={handleChange}
        required
      />
      <input
        type="tel"
        name="phone"
        placeholder="Phone Number"
        value={formData.phone}
        onChange={handleChange}
        required
      />
      <input
        type="email"
        name="email"
        placeholder="Email (optional)"
        value={formData.email}
        onChange={handleChange}
      />
      {error && <p style={{ color: 'red' }}>{error}</p>}
      <button type="submit" disabled={loading}>
        {loading ? 'Booking...' : 'Confirm Booking'}
      </button>
    </form>
  );
};

export default BookingForm;