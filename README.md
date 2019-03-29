**SUMMARY\**

These two scripts take in a list of queries to check the SERP and find information about the Google My Business listings
present.

Modules:
1. **serpapi-gmb-crawler-geo-modifier** - This script leverages a static location to query geo-modified terms
from, in this case I've set it by default to be "Cleveland, OH". The reason? I found that geo-modified queries had
a tendency to bring up local 3-packs in search, rather than a singular listing. The presence of 3-packs complicates
the script, so if a local 3-pack is present for a given query, the message shown will say the listing either
does'nt exist or is in a local pack.

2. **serpapi-gmb-crawler-local** - This script leverages a dynamically set location to query non geo-modified
 terms from. This is dependent on adding the comma delimited location to the queries in the TXT file. The script then
 strips these locations from the query and plugs them into the API parameters. The purpose is to allow the user to spoof
 search for locations in those same areas, rather than from somewhere else.