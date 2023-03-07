#!/bin/bash
#recuperation des donnees
echo "requete https://www.google.com/finance/quote/PX1:INDEXEURO?hl=fr"
res=$(curl -L https://www.google.com/finance/quote/PX1:INDEXEURO?hl=fr)

today=($(grep -Po '(?<=<div class="YMlKec fxKbKc">)+(.{0,10})(?=<.*div>)' <<<"$res") )
last=($(grep -Po '(?<=<div class="P6K39c">)(.{0,8})(?=<.*div>)' <<<"$res") )
other=($(grep -Po '(?<=<div class="P6K39c">)(.{0,20})(?=<.*div>)' <<<"$res") )

#affichage
echo "now : ${today[0]}"
echo "last close : ${last[0]}"
echo "variation of the day : ${other[1]} - ${other[3]}"
echo "year range : ${other[4]} - ${other[6]}"

#verification de l existance du fichier
if [ ! -f ./data.csv ]
then 
	#creer un fichier csv et insert les headers et les donnees
	{ 
		echo "timestamp,now,close,daymin,daymax,yearmin,yearmax";
		echo "$(date +%s),'${today[0]}','${last[0]}','${other[1]}','${other[3]}','${other[4]}','${other[6]}'"; 
	} > data.csv
else
	#insert les headers et les donnees
	{ 
		cat data.csv; 
		echo "$(date +%s),'${today[0]}','${last[0]}','${other[1]}','${other[3]}','${other[4]}','${other[6]}'"; 
	} > dataBuf.csv
	#stockage dans un buffer temporaire
	#copie du buffer dans le fichier d origine
	cp -f dataBuf.csv data.csv
	#supprime le buffer
	rm dataBuf.csv
fi
