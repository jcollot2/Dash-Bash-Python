# Dash-Bash-Python

## Virtual Machine
For this project, we used amazon which offers a service to host applications on an ubuntu virtual machine in the cloud.
## Bash
Our goal is to design a scraping script of a website offering financial information. For this, I chose to scrape  : [google finance](https://www.google.com/finance/quote/PX1:INDEXEURO?hl=fr) with the data of CAC 40

I first studied the code of the site to identify syntax or regular expressions (regex). Using the [regex101](https://regex101.com/) website, I forged my regex to efficiently extract information from the website.

Then I was able to write a first code allowing me to launch a query with CURL and extract my data with my regex :

    res=$(curl -L https://www.google.com/finance/quote/PX1:INDEXEURO?hl=fr)
    today=($(grep -Po '(?<=<div class="YMlKec fxKbKc">)+(.{0,10})(?=<.*div>)' <<<"$res") )
    last=($(grep -Po '(?<=<div class="P6K39c">)(.{0,8})(?=<.*div>)' <<<"$res") )
	other=($(grep -Po '(?<=<div class="P6K39c">)(.{0,20})(?=<.*div>)' <<<"$res") )

I formated the data so it would be easy to save in a CSV file which will be generated if it does not already exist. If the file already exists then it will be modified.

    now=$(echo ${today[0]} | sed 's/,/./g' )
	close=$(echo ${last[0]} | sed 's/,/./g')
	daymin=$(echo ${other[1]} | sed 's/,/./g')
	daymax=$(echo ${other[3]} | sed 's/,/./g')
	yearmin=$(echo ${other[4]} | sed 's/,/./g')
	yearmax=$(echo ${other[6]} | sed 's/,/./g')


	if [ ! -f ./data.csv ]
	then
	{
		echo "timestamp,now,close,daymin,daymax,yearmin,yearmax";
		echo "$(date +%s),$now,$close,$daymin,$daymax,$yearmin,$yearmax";
	} > data.csv
	else
	{
		cat data.csv;
		echo "$(date +%s),$now,$close,$daymin,$daymax,$yearmin,$yearmax";
	} > dataBuf.csv
	cp -f dataBuf.csv data.csv
	rm dataBuf.csv

The output of my script is then a CSV file, as shown below:
|timestamp| now | close | daymin | daymax | yearmin | yearmax |
|--|--|--|--|--|--|--|
|1678201388|7 371.95|7 373.21|7 347.31|7 398.03|5 628.42|7 398.03|
|1678201390|7 371.95|7 373.21|7 347.31|7 398.03|5 628.42|7 398.03|
|1678201392|7 371.95|7 373.21|7 347.31|7 398.03|5 628.42|7 398.03|
|...|...|...|...|...|...|...|


## Crontab

Now that the bash script is complete, we need to use this data to design the python Dashboard. For the script to generate data, it would have to run every 5 mins, for that, I use Crontab.

In order to add a task to the Crontab, I use the following command :    `crontab -e`
So this is the job i used :
`*/5 * * * * cd /home/ubuntu/Dash-Bash-Python/ && /bin/bash -c ./getData.sh`
for resume, we say to crontab, to execute each 5 min the command. And this command say to go to the project folder and then execute our bash script.

## Dash
We have designed a python script that will :

 - retrieve and format the information stored in the data.csv file
 - display a graphs with plotly, where we plot the price variations, the value of the day before's closing and the day before's range (min-max).
 - use dash library to put it in a dash board using layout.
 - refresh the dashboard using interval so it is refresh every 5 minutes
 - At 8 p.m., the program will run a script that will create the daily report of the day and compute : Opening price, Closing price, Daily variation, Daily maximum, Daily minimum.

http://http://13.50.224.228:8050/
 
