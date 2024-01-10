from data.HdRezkaApiMain.HdRezkaApi.HdRezkaApi import *
url = "https://rezka.ag/series/fantasy/45-igra-prestolov-2011.html"

rezka = HdRezkaApi(url)
print(rezka.seriesInfo)
print(rezka)
print(rezka.translators)
print(rezka.getStream(season=1,episode=1 )('1080p'))
