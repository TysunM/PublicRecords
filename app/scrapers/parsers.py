from bs4 import BeautifulSoup
from typing import List, Dict, Any

def parse_contra_costa_epermits(html_content: str, config: Dict[str, Any]) -> List[Dict[str, str]]:
    """
    Parses the HTML content from the Contra Costa County ePermits search results page.
    
    This function is highly specific to the structure of the target website. If the
    website changes its HTML layout, this is the function that will need to be updated.
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    results: List[Dict[str, str]] = []

    # Select the main results table using the selector from the config
    table = soup.select_one(config['selectors']['results_table'])
    
    # If the table isn't found, it means there are no results, so we return an empty list.
    if not table:
        print("No results table found on page.")
        return []

    # Find all table rows, skipping the first one which is the header row ([1:])
    for row in table.find_all('tr')[1:]:
        cells = row.find_all('td')
        
        # Ensure the row has the expected number of columns to avoid errors
        if len(cells) > 5:
            # Extract text from specific cells based on their column index
            date = cells[1].get_text(strip=True)
            permit_number = cells[2].get_text(strip=True)
            description = cells[4].get_text(strip=True)
            status = cells[5].get_text(strip=True)
            
            # Construct a clean title for the record
            title = f"{permit_number}: {description}"
            
            # Find the hyperlink within the permit number cell to get a direct URL
            link_tag = cells[2].find('a')
            base_url = "https://epermits.cococounty.us"
            url = base_url + link_tag['href'] if link_tag and link_tag.has_attr('href') else base_url
            
            # Append the structured data to our results list
            results.append({
                "source": config['source_name'],
                "record_type": "Permit",
                "title": title,
                "summary": f"Status: {status}. Date Filed: {date}.",
                "url": url,
            })
            
    print(f"Parser found {len(results)} records.")
    return results
