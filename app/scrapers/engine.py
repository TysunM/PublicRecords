from playwright.sync_api import sync_playwright, Page, TimeoutError as PlaywrightTimeoutError
from typing import List, Dict, Any, Callable
import time

def run_scraper(address: Dict[str, str], config: Dict[str, Any]) -> List[Dict[str, str]]:
    """
    A generic, robust scraping engine powered by Playwright.
    
    This function navigates a website based on a configuration dictionary,
    performs actions, and hands off the final page content to a specific parser.
    """
    results = []
    
    with sync_playwright() as p:
        # Set headless=False for debugging to see the browser UI
        browser = p.chromium.launch(headless=True) 
        page = browser.new_page()
        
        try:
            print(f"Navigating to {config['base_url']}...")
            page.goto(config['base_url'], timeout=60000)

            # --- Perform Search Actions ---
            print("Performing search...")
            # This sequence is defined in the config for each scraper
            street_num, street_name = address['street_address'].split(' ', 1)
            page.fill(config['selectors']['street_num_input'], street_num)
            page.fill(config['selectors']['street_name_input'], street_name)
            
            page.click(config['selectors']['search_button'])
            
            # --- Wait for Results ---
            print("Waiting for results to load...")
            # Wait for the results table to be visible on the page
            page.wait_for_selector(config['selectors']['results_table'], state="visible", timeout=30000)
            
            # A small, static sleep can help ensure all dynamic JS content has loaded
            time.sleep(5) 

            # --- Extract and Parse ---
            print("Extracting and parsing content...")
            html_content = page.content()
            
            # The config points to a specific parser function for this source
            parser_func: Callable[[str, Dict], List[Dict[str, str]]] = config['parser']
            results = parser_func(html_content, config)

        except PlaywrightTimeoutError:
            print(f"Timeout error while scraping {config['source_name']}. The website might be down or the selectors have changed.")
        except Exception as e:
            print(f"An unexpected error occurred in the scraper engine: {e}")
            # In production, you'd log this error to a monitoring service
        finally:
            browser.close()
            
    return results
