import React, { useState } from 'react';
import FileUpload from '../components/FileUpload';
import SchemaDisplay from '../components/SchemaDisplay';
import { DataGrid } from '@mui/x-data-grid';
import Paper from '@mui/material/Paper';

const paginationModel = { page: 0, pageSize: 10 };


const Home = () => {
    const [data, setData] = useState([]);  // Store the data from the API
    const [schema, setSchema] = useState([]);  // Store the schema (data types) of the data
    // Handle successful file upload
    const handleUploadSuccess = (data) => {
        alert('File uploaded successfully. Processing started.');
        setSchema(data.schema);
        setData(data.data);
        // console.log(data);
    };

    const updateSchema = (newSchema) => {
      setSchema(newSchema); 
      console.log("Schema updated:", newSchema);
  };
  

    return (
        <div>
        <div>
            <FileUpload onUploadSuccess={handleUploadSuccess} />
            <SchemaDisplay schema={schema} updateSchema={updateSchema}/>
        </div>
        
      <Paper sx={{ height: 800, width: '100%' }}>
      <DataGrid
        rows={data}
        columns={schema}
        initialState={{ pagination: { paginationModel } }}
        pageSizeOptions={[5, 10]}
        checkboxSelection
        sx={{ border: 0 }}
      />
    </Paper>
      </div>
    );
};

export default Home;
