import pandas as pd
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.parsers import MultiPartParser, FormParser
import os

@csrf_exempt  # Temporarily disabling CSRF for this endpoint; consider better alternatives in production.
@api_view(['POST'])
def upload_file(request):
    # Handle file upload from React
    if 'file' not in request.FILES:
        return JsonResponse({'error': 'No file provided'}, status=400)
    
    file = request.FILES['file']
    
    # Ensure the file is either CSV or Excel (xlsx)
    if file.name.endswith('.csv'):
        file_data = pd.read_csv(file)
    elif file.name.endswith('.xlsx'):
        file_data = pd.read_excel(file)
    else:
        return JsonResponse({'error': 'Invalid file type. Only CSV and Excel are supported.'}, status=400)
    

    # Add an ID column if not present
    if 'id' not in file_data.columns:
        file_data['id'] = range(1, len(file_data) + 1)  

    file_data = infer_and_convert_types(file_data)
    data_dict = file_data.to_dict(orient='records')
    
    # Process the data with Pandas (For example: infer the data types)
    schema = file_data.dtypes.astype(str).to_dict()  # Get data types of columns

    schema = {'id': schema.pop('id'), **schema}
    

    # Map Pandas dtypes to desired types
    type_mapping = {
        "object": "text",
        "datetime64[ns]": "date",
    }

    # Convert schema to the desired format
    
    schema = [
        {
            "field": column,
            "headerName": column.capitalize(),
            "width": 150,  # Default width, can adjust as needed
            "type": "Number" if dtype.startswith(('int', 'float')) else "String",
            "inferredType": type_mapping.get(dtype, dtype)
        }
        for column, dtype in schema.items()
    ]
    # schema.insert(0,{"field": "id","headerName": "ID","width": 100,"type": "int","inferredType": "int"})
    


    # Return both the data and the inferred schema (data types)
    return JsonResponse({'data': data_dict, 'schema': schema}, status=200)



def infer_and_convert_types(df, category_threshold=0.5):
    """
    Infer and convert data types for a Pandas DataFrame.
    
    Args:
        df (pd.DataFrame): The input DataFrame.
        category_threshold (float): Threshold for converting to 'category' type, 
                                    based on the ratio of unique values to total rows.
    
    Returns:
        pd.DataFrame: A DataFrame with inferred and converted data types.
    """
    def is_date_column(series):
        """
        Check if a column is likely a date.
        """
        try:
            pd.to_datetime(series.dropna().sample(min(len(series.dropna()), 10)), errors='raise')
            return True
        except (ValueError, TypeError):
            return False
    
    def is_number(series,threshold=0.8):
        converted = pd.to_numeric(series, errors='coerce')
        num_valid_values = converted.notna().sum()
        valid_ratio = num_valid_values / len(series)
        if valid_ratio >= threshold: # Check if at least 80% of values are valid
            print(f"Column '{column}' is mostly numeric ({valid_ratio:.2%}). Converting to numeric.")
            return True
        else:
            print(f"Column '{column}' is not mostly numeric ({valid_ratio:.2%}). Skipping conversion.")
            return False

    def is_bool_column(series):
        """
        Check if a column is likely boolean.
        """
        non_na_values = series.dropna().unique()
        bool_equivalents = {True, False, 1, 0}
        return set(non_na_values).issubset(bool_equivalents)

    for column in df.columns:
        col_data = df[column]

        # Check for boolean
        if is_bool_column(col_data):
            df[column] = col_data.astype(bool)
            continue

        # Check for integers
        if is_number(col_data):
            col_data = pd.to_numeric(col_data, errors='coerce')
            col_data = col_data.fillna(-1)  # Fill NaN values with -1 for integer conversion
            if col_data.dropna().mod(1).eq(0).all():  # Check if all values are whole numbers
                df[column] = pd.to_numeric(col_data, downcast='integer', errors='coerce')
                continue
        
            # Check for floats
                df[column] = pd.to_numeric(col_data, downcast='float', errors='coerce')
                continue

        # Check for dates
        if is_date_column(col_data):
            df[column] = pd.to_datetime(col_data, errors='coerce', infer_datetime_format=True)
            continue

        # Check for categories
        if pd.api.types.is_object_dtype(col_data):
            num_unique_values = col_data.nunique(dropna=False)
            if num_unique_values < category_threshold * len(df):
                df[column] = col_data.astype('category')
                continue

        def is_timedelta_like(series):
            # Check if the series has typical timedelta patterns
            timedelta_patterns = ["P", "T", "H", "M", "S", "D"]
            sample = series.dropna().astype(str).head(10)
            return all(any(c in val for c in timedelta_patterns) for val in sample)

        if is_timedelta_like(col_data):
            try:
                df[column] = pd.to_timedelta(col_data, errors='coerce')
            except ValueError:
                pass

    return df
