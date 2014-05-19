pybabel -v extract -F babel.cfg -o messages.pot ./
mv messages.pot ./dataviva/translations
pybabel update -i dataviva/translations/messages.pot -d dataviva/translations
cd dataviva
pybabel compile -f -d ./translations
cd ..