#!/bin/bash

#Path to a .csv file (comma separated) with the following fields: "mriid,gender,age,brain_vol,ventricular_vol" (order matters)
CSV_FILE="/path/to/csv"

#other variables
API_KEY="api_key"
PORT="8000"
ADDRESS="http://000.000.0.000"

# Read the .csv line by line and extract fields (order matters)
tail -n +2 "$CSV_FILE" | while IFS=, read -r mriid gender age brain_vol ventricular_vol; do
  # API call
  curl -X 'POST' \
    "$ADDRESS/generategenderageventbrainvol" \
    -H 'accept: application/json' \
    -H "Authorization: Bearer $API_KEY" \
    -H 'Content-Type: application/json' \
    -d "{
      \"mriid\": \"$mriid\",
      \"gender\": $gender,
      \"age\": $age,
      \"ventricular_vol\": $ventricular_vol,
      \"brain_vol\": $brain_vol,
      \"bucket_name\": \"testniisandrea\",
      \"bucket_folder\": \"ldm\"
    }"
done

