
for year in  {2002..2013}; 
	do echo $1 $2 $year;
	python scripts/data_download/rais_create_files.py $1 $2 $year 
	sleep 5
done
	