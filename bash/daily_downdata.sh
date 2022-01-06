#!/bin/bash
echo start

while getopts d:o:p:k: flag
do
    case "${flag}" in
            d) domain=${OPTARG};;
            o) other=${OPTARG};;
            p) project=${OPTARG};;
	           k) key=${OPTARG};;
    esac
done
#echo "Username: $username";

python sync.py -d $domain -o $other -m downdata -p $project -k $key

res1=($(ls -1t | grep database.zip))

if [[ `diff   <(unzip -vqq ${res1[1]} | awk '{$2=""; $3=""; $4=""; $5=""; $6=""; print}' | sort -k3)   <(unzip -vqq ${res1[0]} | awk '{$2=""; $3=""; $4=""; $5=""; $6=""; print}' | sort -k3)` != "" ]]; then echo "different"; if [[ ${#res1[@]} > 3 ]]; then rm ${res1[-1]}; fi; else echo "equvivalent"; rm ${res1[0]}; fi