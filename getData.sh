#!/bin/bash
#recuperation des donnees
echo "requete https://www.google.com/finance/quote/PX1:INDEXEURO?hl=fr"
res=$(curl -L https://www.google.com/finance/quote/PX1:INDEXEURO?hl=fr)
today=($(grep -Po '(?<=<div class="YMlKec fxKbKc">)+(.{0,10})(?=<.*div>)' <<<"$res") )
last=($(grep -Po '(?<=<div class="P6K39c">)(.{0,8})(?=<.*div>)' <<<"$res") )
other=($(grep -Po '(?<=<div class="P6K39c">)(.{0,20})(?=<.*div>)' <<<"$res") )
#formatage des donnees
now=$(echo ${today[0]} | sed 's/,/./g' )
close=$(echo ${last[0]} | sed 's/,/./g')
daymin=$(echo ${other[1]} | sed 's/,/./g')
daymax=$(echo ${other[3]} | sed 's/,/./g')
yearmin=$(echo ${other[4]} | sed 's/,/./g')
yearmax=$(echo ${other[6]} | sed 's/,/./g')
#affichage
echo "now : $now"
echo "last close : $close"
echo "variation of the day : $daymin - $daymax"
echo "year range : $yearmin - $yearmax"
#verification de l existance du fichier
if [ ! -f ./data.csv ]
then 
	#creer un fichier csv et insert les headers et les donnees
	{ 
		echo "timestamp,now,close,daymin,daymax,yearmin,yearmax";
		echo "$(date +%s),$now,$close,$daymin,$daymax,$yearmin,$yearmax"; 
	} > data.csv
else
	#insert les headers et les donnees
	{ 
		cat data.csv; 
		echo "$(date +%s),$now,$close,$daymin,$daymax,$yearmin,$yearmax"; 
	} > dataBuf.csv
	#stockage dans un buffer temporaire
	#copie du buffer dans le fichier d origine
	cp -f dataBuf.csv data.csv
	#supprime le buffer
	rm dataBuf.csv
fi
