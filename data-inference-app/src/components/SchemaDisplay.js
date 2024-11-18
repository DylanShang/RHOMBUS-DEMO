import React from 'react';
const dataTypes = [
    'String',
    'Number'
];
const SchemaDisplay = ({ schema,updateSchema}) => {
    const handleTypeChange = (column, newType) => {
        const updatedSchema = [...schema];
        updatedSchema[column]["type"] = newType;
        updateSchema(updatedSchema);
    };
    return (
        <div>
            <h3>Inferred Schema</h3>
            <table border="1">
                <thead>
                    <tr>
                        <th>Column</th>
                        <th>Inferred Data Type</th>
                        <th>Display Data Type</th>
                    </tr>
                </thead>
                <tbody>
                    {Object.entries(schema).map(([column, data]) => (
                        <tr key={column}>
                            <td>{data["field"]}</td>
                            <td>{data["inferredType"]}</td>
                            {/* <td>{data}</td> */}
                            <td>
                                <select
                                    value={data["type"]}
                                    onChange={(e) => handleTypeChange(column, e.target.value)}
                                    style={{ width: '100%', padding: '5px', borderRadius: '4px', border: '1px solid #ddd' }}
                                >
                                    {dataTypes.map((type) => (
                                        <option key={type} value={type}>
                                            {type}
                                        </option>
                                    ))}
                                </select>
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
};

export default SchemaDisplay;
