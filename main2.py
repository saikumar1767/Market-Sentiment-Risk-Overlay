import pandas as pd
import feedparser
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt
import seaborn as sns
import random
import os

tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META', 'NVDA', 'TSLA', 'BRK-B', 'JPM', 'JNJ']

def generate_mock_factor_exposures(tickers):
    data = {
        "Ticker": tickers,
        "Size": [round(random.uniform(-1, 1), 2) for _ in tickers],
        "Value": [round(random.uniform(-1, 1), 2) for _ in tickers],
        "Momentum": [round(random.uniform(-1, 1), 2) for _ in tickers],
        "Quality": [round(random.uniform(-1, 1), 2) for _ in tickers],
        "Volatility": [round(random.uniform(-1, 1), 2) for _ in tickers]
    }
    return pd.DataFrame(data)

def fetch_rss_news(ticker):
    rss_url = f"https://feeds.finance.yahoo.com/rss/2.0/headline?s={ticker}&region=US&lang=en-US"
    feed = feedparser.parse(rss_url)
    return [entry.title for entry in feed.entries[:5]]

def get_sentiment_score(headlines):
    analyzer = SentimentIntensityAnalyzer()
    if not headlines:
        return 0.0
    scores = [analyzer.polarity_scores(h)['compound'] for h in headlines]
    return round(sum(scores) / len(scores), 3)

def risk_flag(row):
    if row["Sentiment"] < -0.3 and row["Momentum"] > 0.5:
        return "Watchlist: Negative sentiment despite high momentum"
    elif row["Sentiment"] > 0.3 and row["Momentum"] < -0.5:
        return "Watchlist: Positive sentiment but losing momentum"
    else:
        return "Normal"

def main():
    factor_df = generate_mock_factor_exposures(tickers)
    news_data = {ticker: fetch_rss_news(ticker) for ticker in tickers}
    
    print("\n------ Ticker Headlines ------")
    for ticker, headlines in news_data.items():
        print(f"\n{ticker}:")
        for h in headlines:
            print(f"- {h}")
    
    sentiment_scores = {ticker: get_sentiment_score(news_data[ticker]) for ticker in tickers}
    sentiment_df = pd.DataFrame(list(sentiment_scores.items()), columns=["Ticker", "Sentiment"])
    overlay_df = pd.merge(factor_df, sentiment_df, on="Ticker")
    overlay_df["Insight"] = overlay_df.apply(risk_flag, axis=1)

    #outputs
    os.makedirs("outputs", exist_ok=True)
    overlay_df.to_excel("outputs/overlay_results.xlsx", index=False)

    headlines_expanded = [{"Ticker": t, "Headline": h} for t in tickers for h in news_data[t]]
    headlines_df = pd.DataFrame(headlines_expanded)
    headlines_df.to_excel("outputs/headlines_raw.xlsx", index=False)

    # Plot
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=overlay_df, x='Momentum', y='Sentiment', hue='Insight', style='Ticker', s=100)
    plt.axhline(0, linestyle='--', color='gray')
    plt.axvline(0, linestyle='--', color='gray')
    plt.title('Sentiment vs Momentum Overlay')
    plt.xlabel('Momentum Exposure')
    plt.ylabel('Sentiment Score')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("outputs/sentiment_vs_momentum_plot.png")
    plt.close()

if __name__ == "__main__":
    main()