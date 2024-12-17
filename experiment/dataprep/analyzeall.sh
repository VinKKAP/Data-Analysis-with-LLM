find ../data -name '*.csv' > ../data/allcsvs
rm -f ../data/corresult4.csv
rm -f ../data/corresult_output_file.csv
let 'x=0'; while read f; do
    let 'x=x+1'
    python ../src/dp/prep/coranalyze.py "$f" $x >> ../data/corresult5.csv
done < ../data/allcsvs