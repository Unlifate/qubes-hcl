import yaml
import glob
from tabulate import tabulate


def validhardware(doc):
    if len(doc["versions"]) > 1:
        print(doc)
    versions = doc["versions"][0]
    if (cleanStr(versions['qubes']) == ''):
        return False
    elif(

            cleanStr(versions['qubes']).startswith("R4.1") &
            ( not cleanStr(versions['works']).startswith("yes") )&
                (not cleanStr(versions['works']).startswith("partial"))&
                (not cleanStr(versions['works']).startswith("no"))
    ):
        return True
    return False

def cleanStr(cleanMe):
    if isinstance(cleanMe, str):
        cleanMe = cleanMe.strip('\n\' ').replace('\n', ' ')
        return cleanMe
    else:
        return cleanMe

# set table table headers
headers = []
hw = []

# for fileName in glob.glob("*.yml"):
for fileName in ["Hewlett-Packard-Compaq_dc7900_Convertible_Minitower-Nukama.yml", "ASUSTeK-G750JM-20181011-002139.yml"]:
    if not fileName.startswith("."):
        with open(fileName, 'r', encoding="utf8") as filestream:
            docs = yaml.load_all(filestream, Loader=yaml.FullLoader)
            for doc in docs:
                if hasattr(doc, "items"):
                    for i in doc["versions"]:
                        docwithoutversions = {j:doc[j] for j in doc if j!='versions'}
                        # Merge dictionaries, works only in Python 3.9+
                        hw.append(docwithoutversions | i)

# todo: use set instead of list object for header
# get all known columns (headers)
for i in hw:
    currentHeaders = list(i.keys())
    for nowHeader in currentHeaders:
        if not nowHeader in headers:
            headers.append(nowHeader)
headers = sorted(headers)

# write all attributes into a table
toprint = [headers]
for selectedhw in hw:
    newhwentry = []
    for k in headers:
        newhwentry.append(selectedhw.get(k, "undefined"))
    toprint.append(newhwentry)

#print(tabulate(toprint, 'firstline', "pretty"))

for row in toprint:
    print(",".join(map(cleanStr, row)))

"""
hwnew = {}
for header in headers:
    hwnew[header] = []
    for k in hw:
        for l in k["version"]:
            hwnew[header].append(k.get(header) or "undefined")

with open('out.html', 'w', encoding="utf8") as f:
    f.write(tabulate(hw, headers, "html"))
"""