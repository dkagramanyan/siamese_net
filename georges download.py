import pandas as pd
import urllib
import httplib2
import urllib.request

# georges_path='saint george images/georges'
# path='saint george images/georges/georges.csv'
georges_path = 'saint george images/non georges'
path = 'saint george images/non georges/non_georges.csv'

df = pd.read_csv(path)

for i, url in enumerate(df.values):
    h = httplib2.Http('.cache')
    response, content = h.request(url[0])
    out = open(georges_path + '/' + str(i) + '.jpg', "wb")
    out.write(content)
    out.close()
