# Stock Comparison Tool Powered by 10 Open Source LLMs

This repository contains a web application built with Flask that allows users to compare and visualize the historical stock prices of two ticker symbols over the past five years. Additionally, it generates a summary description of the stock data using one of 10 open-source language models.

https://github.com/user-attachments/assets/34ee7f50-a62f-4df5-b8e1-1ead1e557500

## Features

- **Fetch Historical Stock Data**: Query stock prices for any two ticker symbols using the Yahoo Finance API.
- **Visualize Stock Data**: Plot the closing prices of the queried stocks over the past five years.
- **Generate Descriptions**: Summarize the stock data using AI-powered language models.
- **Interactive Web Interface**: Simple and user-friendly web interface to input ticker symbols and select a language model.

## Installation and Setup

1. **Clone the Repository**
   ```bash
   git clone https://github.com/HussainNasirKhan/Stock-Comparison-Tool-Powered-by-10-Open-Source-LLMs
   cd Stock-Comparison-Tool-Powered-by-10-Open-Source-LLMs
2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
3. **Setting Up Ollama**

- Download Ollama from the following link: [Ollama Download](https://ollama.com/)

- Install all the models on your local system:
    ```bash
    ollama run llama3
    ollama run gemma2
    ollama run qwen2
    ollama run phi3
    ollama run aya
    ollama run mistral
    ollama run mixtral
    ollama run llava
    ollama run openchat
    ollama run wizardlm2
    ```
4. **Run the Application**
- Start the Flask server:
   ```bash
   python app.py
- Open your web browser and navigate to http://127.0.0.1:5000/

## Usage
-  Enter two ticker symbols and select a language model, then click "Submit".

## Technologies Used
- **Flask**: Web framework for building the application.
- **yfinance**: Library for fetching historical stock data.
- **matplotlib**: Plotting library for generating stock charts.
- **langchain_community.llms**: Language model for generating descriptive text.
- **HTML/CSS**: For the frontend templates.
