# Mutual Fund Analyzer

A simple tool which helps you to select mutual funds based on your risk appetite.

This project retrieves mutual fund details from specified URLs, processes and normalizes the data, and assigns a score based on various financial metrics. The data is then saved to a HTML file for easy visualization and comparison.

## Features:

Extracts mutual fund details such as:
- Risk appetite (Beta, Standard Deviation)
- Performance ratios (Sharpe Ratio, Treynor's Ratio, Jensen's Alpha)
- Return metrics (Mean Return)
- Expense Ratio

Normalizes the extracted metrics and computes a score based on pre-defined weights.
Saves and appends fund data to a HTML file for further analysis.
Automatically removes any existing file before adding new fund data.

## Project Setup
### Prerequisites

You need the following Python libraries:

- requests (for fetching web pages)
- beautifulsoup4 (for parsing HTML)
- pandas (for storing and manipulating the fund data)
- json (for parsing structured data)
- re (for regular expression operations)
- os (for file operations)

You can install the required libraries using pip:

    pip install requests beautifulsoup4 pandas

### How It Works
**Fetching Fund Data:** The get_fund_details(url) function takes a mutual fund URL, scrapes the page, and extracts key financial metrics including:
    Beta
    Standard Deviation
    Sharpe Ratio
    Treynor's Ratio
    Jensen's Alpha
    Mean Return
    Expense Ratio
Each metric is then normalized using predefined weights to compute a total score for the fund.

**Data Normalization and Scoring:**
    Each metric is assigned a weight, and the values are normalized (compared to the average) to calculate a weighted score for each fund.
    The overall score is the sum of all the normalized scores.

**Saving Fund Data:**
    The save_or_append_to_html(fund_data) function saves the fund data to a HTML table. If the file already exists, the new data is appended to the existing table.
    The table is sorted by the computed score in descending order, making it easy to compare fund performance.

### Example Usage
Running the Script

- Clone or download the repository.

      git clone git@github.com:adathatri/my_projects_repo.git
- In the terminal, navigate to the project folder and run the script:
    - NIFTY Next 50 funds
 
          python next_50_nifty_analyzer.py
    - NIFTY Small cap funds

          python small_cap_nifty_analyzer.py
This will fetch data from the predefined URLs, calculate the scores, and save them to an HTML file named next_50_fund_details.html or small_cap_fund_details.html.

### Data Sources

The fund details are fetched from the Economic Times website. A list of mutual fund URLs is provided in the script, and it will scrape the data for each URL.

Here are some sample URLs:

[Kotak Nifty Next 50 Index Fund](https://economictimes.indiatimes.com/kotak-nifty-next-50-index-fund-direct-plan/mffactsheet/schemeid-41327.cms?from=mdr)

[Motilal Oswal Nifty Next 50 Index Fund](https://economictimes.indiatimes.com/motilal-oswal-nifty-next-50-index-fund-direct-plan/mffactsheet/schemeid-40469.cms?from=mdr)

[SBI Nifty Next 50 Index Fund](https://economictimes.indiatimes.com/sbi-nifty-next-50-index-fund-direct-plan/mffactsheet/schemeid-41492.cms?from=mdr)

# License and Contact Information

## License

This project is licensed under the [MIT License](LICENSE), which means you can freely use, modify, and distribute the code as long as you include the original copyright and license notice. For more details, see the [LICENSE](LICENSE) file.

If you're unsure about how to apply the license or have specific use cases in mind, feel free to contact me.

---

### License Summary:
- **Free for personal and commercial use**
- **Modifications and distribution allowed**
- **Attribution required**

Please refer to the full [MIT License](LICENSE) text for complete details.

---

## Contact Me

If you have any questions, issues, suggestions or need a personalised data for a nominal amount, feel free to reach out to me! Here's how you can contact me:

- **Email**: [anusha.dathatri@gmail.com](mailto:your-email@example.com)
- **GitHub Issues**: If you're facing a bug or have a feature request, feel free to open an issue in the repository.
- **LinkedIn**: [My LinkedIn Profile](https://www.linkedin.com/in/anusha-dathatri-03803695/)

I’d love to hear from you, whether it's feedback on the project or just a casual conversation. Happy coding!
