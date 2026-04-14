# 🤖 AI Quant Analyst Bot (Bloomberg Terminal Lite)

## Overview
An automated AI-powered financial analyst built with Python. This project scrapes real-time market data, analyzes financial news using a highly optimized LLM, and automatically generates professional PowerPoint briefing decks. 

## Key Features
* **Market Data Pipeline:** Retrieves real-time pricing and fundamental news using `yfinance` and `BeautifulSoup`.
* **Cost-Optimized AI Engine:** Integrated with Moonshot AI (Kimi) via API. By bypassing standard western APIs (GPT-4/Claude) and leveraging this model, the bot processes massive contexts (entire financial articles) at a fraction of the cost, ensuring high ROI for the tool.
* **Automated Reporting:** Replaces junior analyst grunt work by instantly formatting the AI's quantitative analysis into a clean, auto-sized `.pptx` presentation using `python-pptx`.

## Architecture
* `quant_automatisation.py` : The backend "Brain". Handles data scraping, prompt engineering, error handling (429 status codes), and API calls.
* `quant_ppt.py` : The frontend "Display". Takes the AI's output and formats it into a ready-to-use presentation.

## Roadmap (Next Steps)
* Implement `asyncio` for scalable, asynchronous API calls across larger portfolios.
* Add `Matplotlib` to generate and embed price trend charts directly into the PowerPoint slides.
* Build a lightweight web interface using `Streamlit`.
