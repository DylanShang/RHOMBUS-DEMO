import React, { useState } from 'react';
import { uploadFile } from '../services/api';

const FileUpload = ({ onUploadSuccess }) => {
    const [file, setFile] = useState(null); // State to store the selected file
    const [uploading, setUploading] = useState(false); // State to track upload status
    const [error, setError] = useState(''); // State to track errors

    // Handle file selection
    const handleFileChange = (event) => {
        setFile(event.target.files[0]);
    };

    // Handle file upload
    const handleUpload = async () => {
        if (!file) {
            setError('Please select a file to upload.');
            return;
        }
        setError('');
        setUploading(true);
        try {
            const response = await uploadFile(file); // Call the API to upload the file
            onUploadSuccess(response); // Notify the parent component of success
        } catch (err) {
            setError('Failed to upload file.');
        } finally {
            setUploading(false);
        }
    };

    return (
        <div>
            <h2>Upload a File</h2>
            <input type="file" onChange={handleFileChange} />
            <button onClick={handleUpload} disabled={uploading}>
                {uploading ? 'Uploading...' : 'Upload'}
            </button>
            {error && <p style={{ color: 'red' }}>{error}</p>}
        </div>
    );
};

export default FileUpload;
