# ./gera_rais.sh en/pt output_path select(1,2,3,4)
# ./scripts/data_download/gera_rais.sh en ~/files_rais/en/ &> out scripts/data_download/out_rais_years_4.txt&
# gerando 4

if [[ $@ != 2 ]]; then
    echo "Error, use:"
    echo "./scripts/data_download/gera_rais.sh en/pt output_path 1/2/3/4 &> out scripts/data_download/out_rais_years.txt&"
    echo -e " 1 = rais-2003-microregions-classes-families\n 2 = rais-2013-municipalities-classes\n 3 = rais-2013-municipalities-classes-main_groups\n 4 = rais-2013-municipalities-classes-families\n"
    exit
fi

for year in  {2013..2002}; 
	do echo $1 $2 $year;
	#python scripts/data_download/rais.py $1 $2 $year $3
	sleep 5
done
	
