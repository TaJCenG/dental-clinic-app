import React from 'react';

const OTPDisplay = ({ appointment }) => {
  // Ensure appointment is an object with expected fields
  return (
    <div>
      <h2>Booking Confirmed!</h2>
      <p>Your OTP for check-in is:</p>
      <h1 style={{ fontSize: '3rem', letterSpacing: '5px' }}>{appointment.otp_code}</h1>
      <p>Valid until: {new Date(appointment.otp_expiry).toLocaleString()}</p>
      <p>Please show this OTP at the clinic.</p>
    </div>
  );
};

export default OTPDisplay;