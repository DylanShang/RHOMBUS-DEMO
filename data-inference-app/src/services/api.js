import axios from 'axios';

// Set the base URL for the Django backend
const BASE_URL = 'http://localhost:8000/data/';

// Function to upload files to the backend
export const uploadFile = async (file) => {
    const formData = new FormData();
    formData.append('file', file);
    const response = await axios.post(`${BASE_URL}upload/`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
    });
    return response.data;
};

// Function to process the uploaded file
export const processFile = async (fileId) => {
    const response = await axios.get(`${BASE_URL}process/${fileId}/`);
    return response.data;
};
