# !/bin/bash

# - README -
# Preprocessing and Graphing script for Interchunk Dependency Parsed sentences in Indian Language supported by SSF.
# Requires graphviz and wxconv modules installed

filename="${1%.*}"

# - Script to process chunks -

# the below steps extracts words in chunks and puts each sentence in a line
grep -P "[0-9]+\.[1-9]\t" $1 | cut -f 1,2 >> "$filename"_data_temp_1.txt
sed -ri 's|[0-9]+\.[2-9]\t|\t|g' "$filename"_data_temp_1.txt
tr '\n' ' ' < "$filename"_data_temp_1.txt >> "$filename"_data_temp_2.txt
rm "$filename"_data_temp_1.txt
sed -ri 's| 1\.1\t|\n1\.1\t|g' "$filename"_data_temp_2.txt

# store lines in an array
mapfile -t lines < "$filename"_data_temp_2.txt
rm "$filename"_data_temp_2.txt

# iterate over chunks, do some more cleaning, and provide unique IDs
id=0
for x in "${lines[@]}"
do
  ((id++))
  echo "$x" >> "$filename"_sent${id}.txt
  sed -ri "s|.1\t|.${id}@#\t|g" "$filename"_sent${id}.txt
  sed -ri "s| \t|\t|g" "$filename"_sent${id}.txt
  sed -ri "s| |\t|g" "$filename"_sent${id}.txt
  cat "$filename"_sent${id}.txt >> "$filename"_data_temp_wx.txt
  rm "$filename"_sent${id}.txt
done

# Convert to UTF (Hindi)
wxconv -l hin -s wx -i "$filename"_data_temp_wx.txt -o "$filename"_data_utf.txt
rm "$filename"_data_temp_wx.txt

# - Script to process chunks' attributes and relations -

# the below steps extracts attributes of chunks and puts each sentence's attributes in a line
grep -P '^[0-9]+\t' $1 >> "$filename"_attr_temp_1.txt
tr '\n' ' ' < "$filename"_attr_temp_1.txt >> "$filename"_attr_temp_2.txt
sed -ri 's|> 1\t|>\n1\t|g' "$filename"_attr_temp_2.txt
rm "$filename"_attr_temp_1.txt

# store lines in an array
mapfile -t liness < "$filename"_attr_temp_2.txt
rm "$filename"_attr_temp_2.txt

# iterate over chunks', do some more cleaning, attributes and provide mappable IDs
ids=0
for xs in "${liness[@]}"
do
  ((ids++))
  echo "$xs" >> "$filename"_sents${ids}.txt
  sed -ri "s/\t\(\(\t/.${ids}@#\t/g" "$filename"_sents${ids}.txt
  sed -ri "s/<fs//g" "$filename"_sents${ids}.txt
  sed -ri "s/   /\t/g" "$filename"_sents${ids}.txt
  sed -ri "s/  /\t/g" "$filename"_sents${ids}.txt
  sed -ri "s/ /\t/g" "$filename"_sents${ids}.txt
  sed -ri "s/\t\t\t/\t/g" "$filename"_sents${ids}.txt
  sed -ri "s/\t\t/\t/g" "$filename"_sents${ids}.txt
  sed -ri "s/>//g" "$filename"_sents${ids}.txt
  sed -ri "s/\"/'/g" "$filename"_sents${ids}.txt
  cat "$filename"_sents${ids}.txt >> "$filename"_attr_wx.txt
  rm "$filename"_sents${ids}.txt
done

# python file called for mapping the chunks to their attributes, formatting them to .dot files for graphviz per sentence, and store them in a <Dependency_Graphs> folder in the same directory as the scripts

python3 preproc.py "$1" "$filename"_data_utf.txt "$filename"_attr_wx.txt "$filename"
rm "$filename"_attr_wx.txt "$filename"_data_utf.txt

# graphviz called to graph sentences to PNG and store in the same folder

for sent_file in $(find Dependency_Graphs/$filename/ -type f);
do
  f="${sent_file%.*}"
  dot -Tsvg "$sent_file" > $f.svg
done