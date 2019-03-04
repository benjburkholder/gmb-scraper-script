from lib.google_search_results import GoogleSearchResults

# Documentation ~ https://serpapi.com/demo

"""
Local txt file will hold composite of dealer name, city, state: e.g bob's satellites lexington kentucky
This should ensure the knowledge graph/listing will be pulled up in SERP

For loop will perform each call with different query parameter.
JSON results are filtered to only contain knowledge graph results.
We can filter out these results down to just the most important fields as well:
- Name
- Address
- Website
- GMB Claim status
- For chain locations, will need to specify city and state in query parameters.
- Create input area where the user will specify whether or not the locations being scraped are chain/franchise
    or if they are uniquely named locations. This will govern how the program works.
"""

print('Are the locations chains or uniquely named?')
print('Chain/Franchise Names (A)')
print('Unique Names (B)')
print('-' * 20)
choice = input('Enter Letter of Choice: ')

downloadFile = 'gmb-status-crawl.csv'
file = open(downloadFile, 'w')

columnHeader = 'Query,Name,Address,Website,GMB Unclaimed?\n'
file.write(columnHeader)

with open('serp_urls.txt') as content, open('serp_locations.txt') as location:
    content = [line.rstrip('\n') for line in content]
    location = [line.rstrip('\n') for line in location]

    for line in content:
        for loc in location:
            errorType = ''
            if choice == 'B':
                params = {
                    "q" : str(line),
                    "location" : "United States",
                    "hl" : "en",
                    "gl" : "us",
                    "google_domain" : "google.com",
                    "api_key" : "Enter own API Key from SERP API",
                }

            elif choice == 'A':
                params = {
                    "q": str(line),
                    "location": f'{loc}, United States',
                    "hl": "en",
                    "gl": "us",
                    "google_domain": "google.com",
                    "api_key": "32b9a805adc53cc21080d4f3c5a2d7f23f22ea53eeb3875e9b912a73eb794765",
                }
        query = GoogleSearchResults(params)
        dictionary_results = query.get_dictionary()
        # print(dictionary_results['knowledge_graph'])

        try:
            name = dictionary_results['knowledge_graph']['title']
        except KeyError:
            errorType = 'Error'
            row = f'{line} ~ No Listing Exists\n'
            print(f'{line} ~ No Listing Exists')
            file.write(row)

        if errorType != 'Error':
            name = dictionary_results['knowledge_graph']['title']
            address = dictionary_results['knowledge_graph']['address']
            website = dictionary_results['knowledge_graph']['website']

            try:
                listingStatus = dictionary_results['knowledge_graph']['unclaimed_listing']
            except KeyError as e:
                listingStatus = 'FALSE'
                row1 = f'{line},"{name}","{address}",{website},{listingStatus}\n'
                file.write(row1)
                print(row1)
            else:
                name = dictionary_results['knowledge_graph']['title']
                address = dictionary_results['knowledge_graph']['address']
                website = dictionary_results['knowledge_graph']['website']
                listingStatus = dictionary_results['knowledge_graph']['unclaimed_listing']

                row = f'{line},"{name}","{address}",{website},{listingStatus}\n'
                file.write(row)
                print(row)
