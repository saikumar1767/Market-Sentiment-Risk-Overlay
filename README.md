# Daily Market Sentiment Risk Overlay Agent (v1 as of now)

This AI agent fetches news headlines for major tickers, analyzes sentiment using VADER, overlays it with factor exposure data, and flags misalignments for risk insights.

## Features
- News sentiment scoring per ticker
- Mocked factor exposures for testing
- Real-time headline logging
- Risk insight classification
- Excel reports and visualization

## How to Run

```bash
pip install -r requirements.txt
python main.py
```

## Output
- `outputs/overlay_results.xlsx`
- `outputs/headlines_raw.xlsx`
- `outputs/sentiment_vs_momentum_plot.png`
