<<<<<<< HEAD
# Unpack the usa_00001.csv.gz file
gunzip -c ./data/usa_00001.csv.gz > ./data/usa_00001.csv

# Find all CSV files including the newly unpacked file
find ./data -name '*.csv' > ./data/allcsvs

# Remove old result files
rm ./data/corresult2.csv
# ...existing code...
rm ./data/corresult4.csv

# Analyze each CSV file and append the results to corresult4.csv
let 'x=0'; while read f; do let 'x=x+1'; python ./src/dp/prep/coranalyze.py "$f" $x >> ./data/corresult4.csv; done <<< "./data/usa_00001.csv"
=======
find ../data -name '*.csv' > ../data/allcsvs
rm ../data/corresult2.csv
let 'x=0'; while read f; do let 'x=x+1'; python3 coranalyze.py "$f" $x >> ../data/corresult4.csv; done < ../data/allcsvs
>>>>>>> 40533f31c4ab3d01b180c28346c3d4345eb46551
