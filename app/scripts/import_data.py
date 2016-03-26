import urllib2
import json
import calendar
import csv


header = ['name', 'from_team', 'team', 'player_id', 'note', 'transaction_id', 'year']

teams = ["Atlanta Braves","Miami Marlins","New York Mets","Philadelphia Phillies","Washington Nationals","Chicago Cubs","Cincinnati Reds","Milwaukee Brewers","Pittsburgh Pirates","St. Louis Cardinals","Arizona Diamondbacks","Colorado Rockies","Los Angeles Dodgers","San Diego Padres","San Francisco Giants","Baltimore Orioles","Boston Red Sox","New York Yankees","Tampa Bay Rays","Toronto Blue Jays","Chicago White Sox","Cleveland Indians","Detroit Tigers","Kansas City Royals","Minnesota Twins","Houston Astros","Los Angeles Angels","Oakland Athletics","Seattle Mariners","Texas Rangers"]

def scrapetocsv():
  for year in range(2013,2016):
    file_name = str(year) + '.csv'
    fout = csv.DictWriter(open(file_name,'w'), header)
    fout.writeheader()
    for month in range(1,13):
      getmonth(year,month,fout)

def getmonth(year,month, fout):
  print year, month
  maxday = calendar.monthrange(year,month)[1]
  monthstr = str(month)
  if len(monthstr) < 2:
    monthstr = '0' + monthstr
  start = '%s%s01' % (year,monthstr)
  end = '%s%s%02d' % (year,monthstr,maxday)
  url = "http://mlb.mlb.com/lookup/json/named.transaction_all.bam?start_date=%s&end_date=%s&sport_code='mlb'" % (start,end)

  response = urllib2.urlopen(url).read()
  data = json.loads(response)['transaction_all']['queryResults']

  if 'row' in data.keys():
    if type(data['row']) is dict:
      rows = [data['row'], ]
    else:
      rows = data['row']
      for row in rows:
        descrip = row['note'].lower()
        if 'trade' in descrip and len(row['player']) > 0:
          write_row = "{0},{1},{2},{3}".format(str(row['player']), str(row['from_team']), str(row['team']), str(row['player_id']), str(row['note']), str(row['transaction_id']), year)
          fout.writerow(
            {
              'name' : row['player'],
              'from_team' : row['from_team'],
              'team' : row['team'],
              'player_id' : row['player_id'],
              'note' : row['note'],
              'transaction_id' : row['transaction_id'],
              'year' : year
            }
          )
scrapetocsv()