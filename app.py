from flask import Flask, render_template, request
import yfinance as yf
import datetime
import matplotlib.pyplot as plt
from langchain_community.llms import Ollama
import os

app = Flask(__name__)

def fetch_and_plot_stock_data(ticker_symbols):
    # Define the time period
    end_date = datetime.datetime.now()
    start_date = end_date - datetime.timedelta(days=5*365)
    
    plt.figure(figsize=(10, 6))
    
    stock_data = {}
    for ticker_symbol in ticker_symbols:
        try:
            # Fetch the stock data
            ticker_data = yf.Ticker(ticker_symbol)
            stock_data[ticker_symbol] = ticker_data.history(start=start_date, end=end_date)
            
            if not stock_data[ticker_symbol].empty:
                # Plot the stock data
                plt.plot(stock_data[ticker_symbol].index, stock_data[ticker_symbol]['Close'], label=f'{ticker_symbol} Close Price')
            else:
                raise ValueError(f"No data found for ticker symbol: {ticker_symbol}")

        except Exception as e:
            raise ValueError(f"Error fetching data for {ticker_symbol}: {e}")
    
    plt.title(f'{", ".join(ticker_symbols)} Stock Prices Over the Last 5 Years')
    plt.xlabel('Date')
    plt.ylabel('Stock Price (USD)')
    plt.legend()
    plt.grid(True)
    
    plot_filename = f'static/{ticker_symbols[0]}_{ticker_symbols[1]}_stock_price_last_5_years.png'
    plt.savefig(plot_filename)  # Save plot to static directory
    plt.close()  # Close plot to free up memory
    
    return stock_data, plot_filename

def summarize_stock_data(stock_data):
    # Prepare the data summary
    stock_summary = {ticker: data.describe().to_dict() for ticker, data in stock_data.items()}
    return stock_summary

def generate_description(summary_text, base_url='http://localhost:11434', model="llama3"):
    # Initialize the Llama3 instance with the base URL and model name
    llama = Ollama(base_url=base_url, model=model)
    
    # Prepare the input text for the model
    input_text = f"Generate one paragraph description for the following stock summary:\n\n{summary_text}\n But Don't mention total counts each time."
    
    # Generate the description using the model
    generated_description = llama(input_text)
    
    # Format the generated description with headings, paragraphs, and bullet points
    formatted_description = f"""
    <h2>Generated Description:</h2>
    <ul>
        <li>{generated_description}</li>
    </ul>
    """
    
    return formatted_description

@app.route('/', methods=['GET', 'POST'])
def index():
    llm_models = ["gemma2", "llama3", "qwen2", "phi3", "aya", "mistral", "mixtral", "llava", "openchat", "wizardlm2"]
    if request.method == 'POST':
        ticker_symbols = [request.form['ticker_symbol1'].upper(), request.form['ticker_symbol2'].upper()]
        llm_model = request.form['llm_model']
        
        if all(ticker_symbols):
            try:
                # Fetch and plot the stock data
                stock_data, plot_filename = fetch_and_plot_stock_data(ticker_symbols)
                
                # Summarize the stock data
                stock_summary = summarize_stock_data(stock_data)
                
                # Generate a detailed description
                summary_text = f"Summary statistics of {', '.join(ticker_symbols)} stock data over the last 5 years:\n\n{stock_summary}"
                generated_description = generate_description(summary_text, model=llm_model)
                
                return render_template('result.html', ticker_symbols=ticker_symbols, plot_filename=plot_filename, generated_description=generated_description)
            except Exception as e:
                return render_template('index.html', error_message=f"Error fetching data for {', '.join(ticker_symbols)}: {e}", llm_models=llm_models)
        else:
            return render_template('index.html', error_message="Please enter valid ticker symbols.", llm_models=llm_models)
    return render_template('index.html', llm_models=llm_models)

if __name__ == '__main__':
    app.run(debug=True)
