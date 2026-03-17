import React, { useState, useEffect } from 'react';
import api from '../services/api';
import { useAuth } from '../contexts/AuthContext';

const AdminDashboard = () => {
  const [stats, setStats] = useState(null);
  const [availability, setAvailability] = useState([]);
  const [appointments, setAppointments] = useState([]);
  const [newBlock, setNewBlock] = useState({ date: '', start: '09:00', end: '17:00', reason: '' });
  const { logout } = useAuth();

  useEffect(() => {
    fetchStats();
    fetchAvailability();
    fetchAppointments();
  }, []);

  const fetchStats = async () => {
    try {
      const response = await api.get('/admin/dashboard/stats');
      setStats(response.data);
    } catch (error) {
      console.error('Failed to fetch stats', error);
    }
  };

  const fetchAvailability = async () => {
    try {
      const response = await api.get('/admin/availability');
      setAvailability(response.data);
    } catch (error) {
      console.error('Failed to fetch availability', error);
    }
  };

  const fetchAppointments = async () => {
    try {
      const response = await api.get('/admin/appointments');
      setAppointments(response.data);
    } catch (error) {
      console.error('Failed to fetch appointments', error);
    }
  };

  const handleCheckIn = async (appointmentId) => {
    const otp = prompt('Enter OTP provided by patient:');
    if (!otp) return;
    try {
      await api.post(`/appointments/${appointmentId}/check-in?otp=${otp}`);
      alert('Check-in successful');
      fetchAppointments(); // refresh list
      fetchStats(); // refresh stats
    } catch (error) {
      alert(error.response?.data?.detail || 'Check-in failed');
    }
  };

  const handleComplete = async (appointmentId) => {
    if (!window.confirm('Mark this appointment as completed?')) return;
    try {
      await api.post(`/appointments/${appointmentId}/complete`);
      alert('Appointment completed');
      fetchAppointments();
      fetchStats();
    } catch (error) {
      alert(error.response?.data?.detail || 'Completion failed');
    }
  };

  const handleBlockSubmit = async (e) => {
    e.preventDefault();
    try {
      await api.post('/admin/availability', {
        date: newBlock.date,
        start_time: newBlock.start,
        end_time: newBlock.end,
        is_available: false,
        reason_blocked: newBlock.reason
      });
      fetchAvailability();
      setNewBlock({ date: '', start: '09:00', end: '17:00', reason: '' });
    } catch (error) {
      console.error('Failed to block date', error);
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'pending': return 'orange';
      case 'visited': return 'blue';
      case 'completed': return 'green';
      case 'cancelled': return 'red';
      default: return 'gray';
    }
  };

  return (
    <div style={{ padding: '20px' }}>
      <h1>Admin Dashboard</h1>
      <button onClick={logout} style={{ float: 'right' }}>Logout</button>

      {/* Stats */}
      {stats && (
        <div>
          <h2>Stats</h2>
          <p>Total: {stats.total}</p>
          <p>Pending: {stats.pending}</p>
          <p>Visited: {stats.visited}</p>
          <p>Completed: {stats.completed}</p>
          <p>Cancelled: {stats.cancelled}</p>
        </div>
      )}

      {/* Block Dates */}
      <h2>Block Dates</h2>
      <form onSubmit={handleBlockSubmit}>
        <input
          type="date"
          value={newBlock.date}
          onChange={(e) => setNewBlock({...newBlock, date: e.target.value})}
          required
        />
        <input
          type="time"
          value={newBlock.start}
          onChange={(e) => setNewBlock({...newBlock, start: e.target.value})}
        />
        <input
          type="time"
          value={newBlock.end}
          onChange={(e) => setNewBlock({...newBlock, end: e.target.value})}
        />
        <input
          type="text"
          placeholder="Reason (optional)"
          value={newBlock.reason}
          onChange={(e) => setNewBlock({...newBlock, reason: e.target.value})}
        />
        <button type="submit">Block</button>
      </form>

      {/* Appointments List */}
      <h2>Appointments</h2>
      <button onClick={fetchAppointments}>Refresh</button>
      {appointments.length === 0 ? (
        <p>No appointments found.</p>
      ) : (
        <table style={{ width: '100%', borderCollapse: 'collapse' }}>
          <thead>
            <tr>
              <th>ID</th>
              <th>Patient</th>
              <th>Phone</th>
              <th>Date/Time</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {appointments.map(apt => (
              <tr key={apt.id}>
                <td>{apt.id}</td>
                <td>{apt.patient_name}</td>
                <td>{apt.patient_phone}</td>
                <td>{new Date(apt.start_time).toLocaleString()} – {new Date(apt.end_time).toLocaleTimeString()}</td>
                <td style={{ color: getStatusColor(apt.status), fontWeight: 'bold' }}>
                  {apt.status.toUpperCase()}
                </td>
                <td>
                  {apt.status === 'pending' && (
                    <button onClick={() => handleCheckIn(apt.id)}>Check In</button>
                  )}
                  {apt.status === 'visited' && (
                    <button onClick={() => handleComplete(apt.id)}>Complete</button>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
};

export default AdminDashboard;