# ./gera_rais.sh en/pt output_path 

for year in  {2002..2013}; 
	do echo $1 $2 $year;
	# python scripts/data_download/rais.py $1 $2 $year 4
	sleep 5
done
	
