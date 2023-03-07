#!/bin/bash
res=$(curl -L https://www.google.com/finance/quote/PX1:INDEXEURO?hl=fr)
#echo "$res"
today=($(grep -Po '(?<=<div class="YMlKec fxKbKc">)+(.{0,10})(?=<.*div>)' <<<"$res") )
last=($(grep -Po '(?<=<div class="P6K39c">)(.{0,8})(?=<.*div>)' <<<"$res") )
other=($(grep -Po '(?<=<div class="P6K39c">)(.{0,20})(?=<.*div>)' <<<"$res") )
echo "Aujourd'hui : ${today[0]}"
echo "Derniere Cloture : ${last[0]}"
echo "Variation Journee : ${other[1]} - ${other[3]}"
echo "Plage Annee : ${other[4]} - ${other[6]}"