# ChanAnlyzer
queries the 4chan boards and creates a word cloud based on all the active thread titles

## Usage
```python
    chanalyzer = ChanAlyzer('https://boards.4chan.org/pol/', true)
    chanalyzer.word_cloud()
```
Use false to go off snapshot
File saved to 'ChanAlyzer_' + time + '.png'

## run
python chanalyzer.py -s
