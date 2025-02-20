import requests
from config.config import GRAPHQL_ENDPOINT, HEADERS, UC_MERCED_SCHOOL_ID

def fetch_all_uc_merced_professors():
    """
    Fetches ALL UC Merced professors by doing an empty-text search
    and paginating until no more results.
    Returns a list of professor nodes (dicts).
    """

    all_professors = []
    seen_ids = set() 
    after_cursor = "" 
    has_next = True

    while has_next:
        query = """
        query TeacherSearchResultsPageQuery(
        $query: TeacherSearchQuery!
        $schoolID: ID
        $includeSchoolFilter: Boolean!
        $after: String
        ) {
        search: newSearch {
            teachers(query: $query, first: 50, after: $after) {
            didFallback
            edges {
                cursor
                node {
                __typename
                firstName
                lastName
                legacyId
                avgRating
                avgDifficulty
                numRatings
                school {
                    id
                    name
                }
                wouldTakeAgainPercent
                }
            }
            pageInfo {
                hasNextPage
                endCursor
            }
            resultCount
            }
        }
        school: node(id: $schoolID) @include(if: $includeSchoolFilter) {
            __typename
            ... on School {
            name
            }
            id
        }
        }

        """

        variables = {
            "query": {
                "text": "",
                "schoolID": UC_MERCED_SCHOOL_ID,
                "fallback": False
            },
            "schoolID": UC_MERCED_SCHOOL_ID,
            "includeSchoolFilter": True,
            "after": after_cursor
        }

        payload = {
            "operationName": "TeacherSearchResultsPageQuery",
            "variables": variables,
            "query": query
        }

        # POST Request
        response = requests.post(GRAPHQL_ENDPOINT, headers=HEADERS, json=payload)
        response.raise_for_status()
        print("Status code:", response.status_code)
        print("Response text:", response.text)

        data = response.json()
        print("Parsed JSON:", data)

        teachers_data = data["data"]["search"]["teachers"]
        edges = teachers_data["edges"]

        for edge in edges:
            node = edge["node"]
            if node["legacyId"] not in seen_ids:
                seen_ids.add(node["legacyId"])
                all_professors.append(node)

        page_info = teachers_data["pageInfo"]
        has_next = page_info["hasNextPage"]
        after_cursor = page_info["endCursor"] if has_next else ""

    return all_professors
