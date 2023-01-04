import urllib.request
from bs4 import BeautifulSoup
import sys

#take to html from the webpage
fp = urllib.request.urlopen("https://jens-his-bucket-for-cloud-pe-that-is-very-hard.s3.amazonaws.com/")
mybytes = fp.read()
mystr = mybytes.decode("utf8")
fp.close()


#convert the html code to xml
bs_data = BeautifulSoup(mystr, 'xml')
#alle elementen nemen van Key
b_unique = bs_data.find_all('Key')
#het eerste Key element wegnemen omdat dit de folder is
image_names = b_unique[1:]


#links get converted to array and put in the right format for carrousel.json
links = []
for image_name in image_names:
    image = image_name.contents
    image_name_without_key = image[0].lstrip("<Key>").lstrip("</Key>")
    source = "{\"url\": " + "\"https://staticimagesfortodoapp.s3.amazonaws.com/" + image_name_without_key + "\"" + "},"
    links.append(source)

#last formatting for putting it in the document
links.insert(0,"[")
last_index = len(links) - 1
links[last_index] = links[last_index][:len(links[last_index]) - 1]
links.insert(len(links),"]")

#writing the list to the carrousel.json file
textfile = open("/var/lib/docker/volumes/todoapp/_data/carrousel.json", "w")
for element in links:
    textfile.write(element + "\n")
textfile.close()
