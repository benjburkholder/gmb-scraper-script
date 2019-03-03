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
"""

downloadFile = 'gmb-status-crawl.csv'
file = open(downloadFile, 'w')

columnHeader = 'Query,Name,Address,Website,GMB Unclaimed?\n'
file.write(columnHeader)

with open('serp_urls.txt') as content:
    content = [line.rstrip('\n') for line in content]

    for line in content:
        errorType = ''
        params = {
            "q" : str(line),
            "location" : "United States",
            "hl" : "en",
            "gl" : "us",
            "google_domain" : "google.com",
            "api_key" : "Purchase API key from SERPApi.com",
        }

        query = GoogleSearchResults(params)
        dictionary_results = query.get_dictionary()
        #print(dictionary_results['knowledge_graph'])

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
