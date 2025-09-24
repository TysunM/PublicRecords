from .parsers import parse_contra_costa_epermits

# This is the data-driven configuration store for all scrapers.
# To add a new data source, you simply add a new entry to this dictionary.
SCRAPER_CONFIGS = {
    "contra_costa_epermits": {
        "source_name": "contra_costa_epermits",
        "base_url": "https://epermits.cococounty.us/citizenaccess/Cap/CapHome.aspx?module=Permits",
        "selectors": {
            "street_num_input": "#ctl00_PlaceHolderMain_generalSearchForm_txtGSStrtNum",
            "street_name_input": "#ctl00_PlaceHolderMain_generalSearchForm_txtGSStrtName",
            "search_button": "#ctl00_PlaceHolderMain_btnNewSearch",
            "results_table": "#ctl00_PlaceHolderMain_dgvPermitList_gdvPermitList",
        },
        "parser": parse_contra_costa_epermits,
    }
    # Add configurations for other counties or data sources here
    # "another_county_deeds": { ... }
}
