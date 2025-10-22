const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

export const testBackendConnection = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/test-cors`);
    const data = await response.json();
    console.log('✅ Backend connection successful:', data);
    return data;
  } catch (error) {
    console.error('❌ Backend connection failed:', error);
    throw error;
  }
};

export default {
  testBackendConnection
};