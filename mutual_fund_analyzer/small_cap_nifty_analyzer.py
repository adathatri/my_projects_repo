import requests
from bs4 import BeautifulSoup
import re
import json
import pandas as pd
import os

def get_fund_details(url):
    # Risk appetite
    beta_w = 0.10
    sd_w = 0.10
    sr_w = 0.25
    tr_w = 0.15
    ja_w = 0.15
    mr_w = 0.20
    er_w = 0.05

    response = requests.get(url)
    if response.status_code != 200:
        print("Failed to retrieve the webpage")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')
    details = {}

    # Extract fund name
    script_tags = soup.find_all('script', {"type": "application/ld+json"})
    fund_name = None
    # Parse the JSON content of the script tag
    try:
        fund_name = json.loads(script_tags[1].string)['name']
        details["Fund name"] = fund_name
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        return None
    
    # Find the <p> tag with class "fs13 bold" containing "Expense Ratio:"
    expense_ratio_tag = soup.find('p', string="Expense Ratio:")
    
    if not expense_ratio_tag:
        print("Expense Ratio not found.")
        return None

    # Extract the text inside <br> tag
    expense_ratio = expense_ratio_tag.find_next_sibling('p').text.strip()
    details["Expense Ratio"] = float(expense_ratio.strip('%'))    

    # Other values
    to_find = ['Standard Deviation', 'Beta', 'Sharpe Ratio', "Treynor's Ratio", "Jensen's Alpha", 'Mean Return']
    for value in to_find:
        try:
            values = soup.find('h4', class_='ratioName', string=value).find_parent().find('div', class_='values')
            sd_fund, sd_avg = [span.text.strip() for span in values.find_all('span')]
            details[value + ' Fund'] = float(sd_fund)
            details[value + ' Avg'] = float(sd_avg)
        except AttributeError:
            details[value + ' Fund'] = 0.00
            details[value + ' Avg'] = 0.00
        
    # Normalized weighed values
    try:
        sd_norm = details["Standard Deviation Avg"]/details["Standard Deviation Fund"]*sd_w
    except ZeroDivisionError:
        sd_norm = 0.00
    
    try:
        beta_norm = details["Beta Avg"]/details["Beta Fund"]*beta_w
    except ZeroDivisionError:
        beta_norm = 0.00

    try:
        sr_norm = details["Sharpe Ratio Fund"]/details["Sharpe Ratio Avg"]*sr_w
    except ZeroDivisionError:
        sr_norm = 0.00

    try:
        tr_norm = details["Treynor's Ratio Fund"]/details["Treynor's Ratio Avg"]*tr_w
    except ZeroDivisionError:
        tr_norm = 0.00

    try:
        ja_norm = details["Jensen's Alpha Fund"]/details["Jensen's Alpha Avg"]*ja_w
    except ZeroDivisionError:
        ja_norm = 0.00

    try:
        mr_norm = details["Mean Return Fund"]/details["Mean Return Avg"]*mr_w
    except ZeroDivisionError:
        mr_norm = 0.00 

    er_norm = details["Expense Ratio"]*er_w

    score = sd_norm + beta_norm + sr_norm + tr_norm + ja_norm + mr_norm + er_norm

    details["Score"] = score
    
    return details

def save_or_append_to_html(fund_data, filename="fund_details.html"):
    if os.path.exists(filename):
        # Read the existing data from the file and ensure proper headers
        existing_df = pd.read_html(filename, header=0)[0]
        # Append the new data
        updated_df = pd.concat([existing_df, pd.DataFrame([fund_data])], ignore_index=True)
    else:
        # Create a new DataFrame with proper headers
        updated_df = pd.DataFrame([fund_data])

    # Remove any "Unnamed" columns caused by HTML formatting issues
    updated_df = updated_df.loc[:, ~updated_df.columns.str.contains('^Unnamed')]

    # Sort the DataFrame by "Score" in descending order
    updated_df = updated_df.sort_values(by="Score", ascending=False, ignore_index=True)

    # Style the DataFrame with borders
    df_styled = updated_df.style.set_table_styles(
        [{'selector': 'table', 'props': [('border', '2px solid black')]},
         {'selector': 'th', 'props': [('border', '1px solid black')]},
         {'selector': 'td', 'props': [('border', '1px solid black')]}]
    )

    # Save to the HTML file
    with open(filename, "w") as f:
        f.write(df_styled.to_html())

if __name__ == "__main__":
    # Remove the file if it exists
    filename = "small_cap_fund_details.html"
    if os.path.exists(filename):
        os.remove(filename)
        print(f"{filename} removed successfully.")

    urls = ["https://economictimes.indiatimes.com/motilal-oswal-nifty-smallcap-250-index-fund-direct-plan/mffactsheet/schemeid-40244.cms?from=mdr",
            "https://economictimes.indiatimes.com/icici-prudential-nifty-smallcap-250-index-fund/mffactsheet/schemeid-41787.cms?from=mdr",
            "https://economictimes.indiatimes.com/nippon-india-nifty-smallcap-250-index-fund-direct-plan/mffactsheet/schemeid-41131.cms?from=mdr",
            "https://economictimes.indiatimes.com/aditya-birla-sun-life-nifty-smallcap-50-index-fund-direct-plan/mffactsheet/schemeid-41389.cms?from=mdr",
            "https://economictimes.indiatimes.com/sbi-nifty-smallcap-250-index-fund-direct-plan/mffactsheet/schemeid-42581.cms?from=mdr",
            "https://economictimes.indiatimes.com/bandhan-nifty-smallcap-250-index-fund-direct-plan/mffactsheet/schemeid-43958.cms?from=mdr",
            "https://economictimes.indiatimes.com/edelweiss-nifty-smallcap-250-index-fund-direct-plan/mffactsheet/schemeid-42808.cms?from=mdr",
            "https://economictimes.indiatimes.com/hdfc-nifty-smallcap-250-index-fund-direct-plan/mffactsheet/schemeid-43484.cms?from=mdr",
            "https://economictimes.indiatimes.com/quant-small-cap-fund-direct-plan/mffactsheet/schemeid-17366.cms?from=mdr",
            "https://economictimes.indiatimes.com/nippon-india-small-cap-fund-direct-plan/mffactsheet/schemeid-16182.cms?from=mdr",
            "https://economictimes.indiatimes.com/tata-small-cap-fund-direct-plan/mffactsheet/schemeid-37991.cms?from=mdr",
            "https://economictimes.indiatimes.com/canara-robeco-small-cap-fund-direct-plan/mffactsheet/schemeid-38817.cms?from=mdr",
            "https://economictimes.indiatimes.com/axis-small-cap-fund-direct-plan/mffactsheet/schemeid-22335.cms?from=mdr",
            "https://economictimes.indiatimes.com/kotak-small-cap-fund-direct-plan/mffactsheet/schemeid-16382.cms?from=mdr",
            "https://economictimes.indiatimes.com/quant-small-cap-fund-direct-plan/mffactsheet/schemeid-17366.cms?from=mdr"
        
    ]
    for url in urls:
        fund_details = get_fund_details(url)
        if fund_details:
            df = pd.DataFrame([fund_details])
            df_styled = df.style.set_table_styles(
                [{'selector': 'table', 'props': [('border', '2px solid black')]},
                {'selector': 'th', 'props': [('border', '1px solid black')]},
                {'selector': 'td', 'props': [('border', '1px solid black')]}]
            )
            save_or_append_to_html(fund_details, filename)
            print(f"Fund details for {fund_details['Fund name']} added.")

