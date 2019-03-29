from lib.google_search_results import GoogleSearchResults

# Documentation ~ https://serpapi.com/demo

"""
NOTE ~ Queries should be structured in this format: query city state(abbreviation).
E.g., hardware store Cleveland OH
"""

api_key = open('serp-api-key.txt').read()

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
            "location" : "Cleveland, Ohio, United States",
            "hl" : "en",
            "gl" : "us",
            "google_domain" : "google.com",
            "api_key" : api_key,
        }

        query = GoogleSearchResults(params)
        dictionary_results = query.get_dictionary()
        # print(dictionary_results['knowledge_graph'])

        try:
            name = dictionary_results['knowledge_graph']['title']
            address = dictionary_results['knowledge_graph']['address']
        except KeyError:
            errorType = 'Error'
            row = f'"{line}" ~ No listing exists OR is in local map pack. Perform manual search to verify.\n'
            print(f'{line} ~ No listing exists OR is in local map pack. Perform manual search to verify.')
            file.write(row)

        if errorType != 'Error':
            name = dictionary_results['knowledge_graph']['title']
            address = dictionary_results['knowledge_graph']['address']
            website = dictionary_results['knowledge_graph']['website']

            try:
                listingStatus = dictionary_results['knowledge_graph']['unclaimed_listing']
            except KeyError as e:
                listingStatus = 'FALSE'
                row1 = f'"{line}","{name}","{address}",{website},{listingStatus}\n'
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
