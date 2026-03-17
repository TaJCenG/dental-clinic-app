import React, { useState } from 'react';
import { useLocation } from 'react-router-dom';
import BookingForm from '../components/BookingForm';
import OTPDisplay from '../components/OTPDisplay';

const BookingPage = () => {
  const location = useLocation();
  const slot = location.state?.slot;
  const [appointment, setAppointment] = useState(null);

  if (!slot) {
    return <p>No slot selected. Go back to calendar.</p>;
  }

  if (appointment) {
    return <OTPDisplay appointment={appointment} />;
  }

  // Display the raw local time strings (no Date conversion)
  return (
    <div>
      <h2>Book Appointment</h2>
      <p>Selected slot: {slot.start} – {slot.end}</p>
      <BookingForm
        selectedSlot={slot}
        onBookingComplete={setAppointment}
      />
    </div>
  );
};

export default BookingPage;