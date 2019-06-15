
ID0001 = {
    'name': "stenoptinea cyan",
    'd_name': "azuurblauwmot",
    "rank": "soort",
    "super": "tineidea"
}

ID0002 = {
    "name": "thyris fenestrella",
    "d_name": "bosrankvlinder",
    "rank": "soort",
    "super": "thyrididae"
}

ID0003 = {
    "name": "tineidea",
    "d_name": "echte motten",
    "rank": "familie",
    "super": "lepidoptera"
}

ID0004 = {
    "name": "thyrididae",
    "d_name": "venstervlekjes",
    "rank": "familie",
    "super": "lepidoptera"
}

soorten = [ID0001, ID0002]
families = [ID0003, ID0004]

i=0
for soort in soorten:
    i += 1
    print(i, soort["name"])
