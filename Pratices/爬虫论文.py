import requests
import pandas as pd
import time

# Define the query parameters
journals = ["Journal of Management Information Systems",
            "Journal of Management Studies",
            "Journal of Marketing"]
query_keywords = "natural experiment"
base_url = "https://api.crossref.org/works"

# Iterate over each journal to construct and send the API request
for journal in journals:
    query = f"{query_keywords} {journal}"
    params = {
        "query.bibliographic": query,
        "filter": "from-pub-date:2010-01-01,until-pub-date:2024-12-31",
        "rows": 500  # Adjust the number of results per request
    }

    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        items = response.json().get("message", {}).get("items", [])

        # Create a DataFrame for the current journal
        columns = ["Title", "Authors", "Year", "Journal", "DOI", "URL"]
        journal_df = pd.DataFrame(columns=columns)

        for item in items:
            title = item.get("title", [""])[0]
            authors = ", ".join([author.get("family", "") for author in item.get("author", [])])
            year = item.get("published-print", {}).get("date-parts", [[None]])[0][0]
            journal_name = item.get("container-title", [""])[0]
            doi = item.get("DOI", "")
            url = item.get("URL", "")

            # Create a new DataFrame row and concatenate it to the journal-specific DataFrame
            new_row = pd.DataFrame({
                "Title": [title],
                "Authors": [authors],
                "Year": [year],
                "Journal": [journal_name],
                "DOI": [doi],
                "URL": [url]
            })
            journal_df = pd.concat([journal_df, new_row], ignore_index=True)

        # Save the journal-specific DataFrame to a CSV file
        file_name = f"{journal.replace(' ', '_')}_natural_experiment_papers.csv"
        journal_df.to_csv(file_name, index=False)
        print(f"Results for {journal} saved to {file_name}")
    else:
        print(f"Failed to fetch data for {journal}: HTTP {response.status_code}")

    # To avoid hitting rate limits, pause between requests
    time.sleep(2)
