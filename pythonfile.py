import urllib.request
from bs4 import BeautifulSoup

#html van de webpagina nemen
fp = urllib.request.urlopen("https://staticimagesfortodoapp.s3.amazonaws.com/")
mybytes = fp.read()
mystr = mybytes.decode("utf8")
fp.close()


#de html code omzetten naar xml
bs_data = BeautifulSoup(mystr, 'xml')
#alle elementen nemen van Key
b_unique = bs_data.find_all('Key')
#het eerste Key element wegnemen omdat dit de folder is
image_names = b_unique[1:]


#links worden toegevoegd aan een array en al in het juiste formaat geplaats voor carrousel.json
links = []
for image_name in image_names:
    image = image_name.contents
    image_name_without_key = image[0].lstrip("<Key>").lstrip("</Key>")
    source = "{\"url\": " + "\"https://staticimagesfortodoapp.s3.amazonaws.com/" + image_name_without_key + "\"" + "},"
    links.append(source)

#laatste formateren voor het in het documenten te plaatsen
links.insert(0,"[")
last_index = len(links) - 1
links[last_index] = links[last_index][:len(links[last_index]) - 1]
links.insert(len(links),"]")

#list uitschrijven naar file
textfile = open("/var/lib/docker/volumes/todoapp/_data/carrousel.json", "w")
for element in links:
    textfile.write(element + "\n")
textfile.close()