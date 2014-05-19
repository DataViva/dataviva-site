pybabel extract -F babel.cfg -o dataviva/translations/messages.pot dataviva
pybabel update -i dataviva/translations/messages.pot -d dataviva/translations
pybabel compile -f -d dataviva/translations
