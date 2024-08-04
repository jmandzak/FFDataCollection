# /bin/bash

echo "Updating fantasypros data..."
python3 fantasypros_scraper.py

echo "Updating depth chart data..."
python3 depth.py

echo "Updating strength of schedule data..."
python3 sos.py

echo "Updating boom/bust data..."
python3 boom_bust.py

echo "updating redzone data..."
python3 redzone_scraper.py

echo "Creating master data file..."
cd stats24
python3 ../master_creator.py

cp final/master_sheet.csv ../../FantasyMVP/FantasyMVP/draft/data/master_sheet.csv
cp final/* ../../FFWizard/src/Stats/