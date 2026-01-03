# RSS News Intelligence & Keyword Indexer

A professional Python-based data engineering pipeline that automates the fetching, parsing, and analysis of global news trends. This project monitors 10+ major international RSS feeds including NASA, BBC, Al Jazeera, and The Economist.

## 🚀 Project Overview
This system serves as a mini "Search Engine" for global news. It collects raw XML data into a relational database, cleans and parses the content into a searchable format, and performs keyword frequency analysis to detect global trends.

## 🛠️ Technical Features
- **Data Pipeline:** Multi-stage workflow (Fetch -> Parse -> Analyze -> Search).
- **Format Support:** Handles both **RSS  (XML)** and **Atom** formats using `xml.etree.ElementTree`.
- **Web Scraping:** Utilizes `BeautifulSoup` for HTML sanitization and text extraction.
- **Relational Storage:** Uses **SQLite3** for data persistence, maintaining separate tables for raw data and processed info.
- **NLP Analysis:** Custom tokenization, stopword filtering, and keyword matching for news intelligence.

## 📂 Folder Structure
- `fetch_rss.py`: Retrieves data from web sources and handles SSL/User-Agent security.
- `parse_xml.py`: Cleans raw XML/HTML and structures data into a clean database.
- `keyword_analysis.py`: Performs statistical analysis on news trends and keyword hits.
- `search_tool.py`: A CLI interface to query the indexed database by keywords and receive the news stored on database.

## ⚙️ Setup & Installation
1. Clone the repository:
   ```bash
   git clone [https://github.com/YOUR_USERNAME/rss-keyword-indexer.git](https://github.com/YOUR_USERNAME/rss-keyword-indexer.git)

2. Install dependencies:
    ```bash
    pip install -r requirements.txt

3. Run the pipeline:
    ```bash
    python fetch_rss.py
    python parse_xml.py
    python keyword_analysis.py


## ⚖️ License
Copyright (c) 2026 Sai Thuta

This project is licensed under the **MIT License**.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
