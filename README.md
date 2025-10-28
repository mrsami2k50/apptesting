# League of Legends Data Viewer

A Streamlit application for viewing League of Legends match history and champion mastery data using the Riot Games API.

## Features

- **Match History**: View the last 10 matches with detailed statistics
  - Champion played
  - KDA (Kills/Deaths/Assists)
  - CS (Creep Score)
  - Damage dealt to champions
  - Game mode and duration
  - Win/Loss indicator

- **Champion Mastery**: Display top 10 champions by mastery
  - Champion level
  - Mastery points

- **Multi-Region Support**: Supports all major LoL regions
  - Japan (jp1)
  - Korea (kr)
  - North America (na1)
  - Europe West (euw1)
  - Europe Nordic & East (eun1)
  - And more...

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Get Riot API Key

1. Visit [Riot Developer Portal](https://developer.riotgames.com/)
2. Sign in with your Riot account
3. Generate a Development API Key

### 3. Run the Application

```bash
streamlit run streamlit_app.py
```

## Usage

1. Open the application in your browser
2. Select your region from the sidebar
3. Enter your Riot API Key in the sidebar
4. Enter a summoner name
5. Click "Fetch Data"

## API Rate Limits

Development API keys have rate limits:
- 20 requests every 1 second
- 100 requests every 2 minutes

The app includes a small delay between requests to help avoid rate limiting.

## Note

- Make sure to select the correct region for the summoner you're searching
- API keys expire after 24 hours and need to be regenerated
- For production use, apply for a production API key from Riot

## License

This project is for educational purposes. League of Legends and Riot Games are trademarks or registered trademarks of Riot Games, Inc.
