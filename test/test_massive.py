from data.av_massive import query as massive_query
from datetime import datetime

if __name__ == "__main__":
    client = massive_query.get_api_client()
    print("Massive API Client initialized:", client)
    quotes = client.list_aggs("AAPL", 1, "minute", from_="2025-01-01", to="2026-01-02")
    for q in quotes:
        dt = datetime.fromtimestamp(q.timestamp / 1000)  # Convert milliseconds to seconds
        print(f"Timestamp: {dt}, Open: {q.open}, High: {q.high}, Low: {q.low}, Close: {q.close}, Volume: {q.volume}")