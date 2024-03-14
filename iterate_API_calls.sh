#!/bin/bash

#Path to a .csv file (comma separated) with the following fields: "mriid,gender,age,brain_vol,ventricular_vol" (order matters)
CSV_FILE="/home/aboscutti/diffusion/ALL_scaled.csv"

# Read the .csv line by line and extract fields (order matters)
tail -n +2 "$CSV_FILE" | while IFS=, read -r mriid gender age brain_vol ventricular_vol; do
  # API call
  curl -X 'POST' \
    'http://184.105.4.118:8000/generategenderageventbrainvol' \
    -H 'accept: application/json' \
    -H 'Authorization: Bearer e3b76d48a3082e5e650019f5951f9a10' \
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

