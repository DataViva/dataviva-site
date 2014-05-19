pybabel extract -F babel.cfg -o messages.pot dataviva
pybabel update -i dataviva/translations/messages.pot -d dataviva/translations
pybabel compile -f -d dataviva/translations
