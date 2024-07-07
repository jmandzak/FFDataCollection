# /bin/bash

echo "Updating fantasypros data..."
python3 fantasypros_scraper.py

echo "Updating depth chart data..."
python3 depth.py

echo "Updating strength of schedule data..."
python3 sos.py

echo "Updating boom/bust data..."
python3 boom_bust.py

echo "Creating master data file..."
cd stats24
python3 ../master_creator.py