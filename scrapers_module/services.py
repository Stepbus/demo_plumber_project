proxies = [
    {'http': 'http://11.111.11.11:00000',
     'https': 'http://11.111.11.11:00000'},
]

variables_newjobslist = {
    "first": 30,
    "filters":
        {
            "distance":
                {
                    "value": 65,
                    "unitSymbol": "km"
                }},
    "coordinates": {
        "latitude": 52.37276,
        "longitude": 4.893604
    },
    "sortBy": "DATE"}

variables_myproposalslist = {
    "filters": {
        "archived": False,
        "proposalStatuses": [
            "MUTUAL_INTEREST",
            "HIRED",
            "REVIEW_RECEIVED"
        ]
    }
}

headers = {
    'authority': 'api',
    'accept': '*/*',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'authorization': 'authorization',
    'client-id': 'client',
}

query_newjobslist = """query NewJobsList($filters: FilterList, $first: Int, 
$endCursor: String, $sortBy: ServiceRequestListSortedByEnum!)}
"""

query_myproposalslist = """query MyProposalsList($filters: FilterList, $cursor: String)"""

query_chat = """
query Chat($id: Int!)"""
