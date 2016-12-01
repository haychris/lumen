root=${0%/*}
python ${root}/scraper.py spring 2011
python ${root}/scraper.py fall 2011
python ${root}/scraper.py spring 2012
python ${root}/scraper.py fall 2012
python ${root}/scraper.py spring 2013
python ${root}/scraper.py fall 2013
python ${root}/scraper.py spring 2014
python ${root}/scraper.py fall 2014
python ${root}/scraper.py spring 2015
python ${root}/scraper.py fall 2015
python ${root}/scraper.py spring 2016
python ${root}/scraper.py fall 2016 false
python ${root}/scraper.py spring 2017 false

python ${root}/processor.py
cp ${root}/pickled_data/necessities.pickle ${root}/../web_flask_react/project/static
