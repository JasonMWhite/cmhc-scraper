# cmhc-scraper
## Scraper for CMHC Housing Market Information Portal

CircleCI Status: [![CircleCI](https://circleci.com/gh/JasonMWhite/cmhc-scraper.svg?style=svg)](https://circleci.com/gh/JasonMWhite/cmhc-scraper)

Requirements: Python 3.5+
Virtual environment recommended

To install:
```
pip install -r requirements.txt
```

To use:
```
cd cmhc
scrapy crawl stats -o output.json
```

To run tests:
```
make test
```
