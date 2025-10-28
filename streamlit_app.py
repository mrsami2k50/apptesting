import streamlit as st
import requests
import time
from typing import Optional, List, Dict

# Riot API Configuration
RIOT_API_KEY = st.secrets.get("RIOT_API_KEY", "")

class RiotAPI:
    """Riot Games API Client"""

    def __init__(self, api_key: str, region: str = "jp1", routing: str = "asia"):
        self.api_key = api_key
        self.region = region  # Platform routing (jp1, kr, na1, etc.)
        self.routing = routing  # Regional routing (asia, americas, europe, sea)
        self.headers = {"X-Riot-Token": api_key}

    def get_summoner_by_name(self, summoner_name: str) -> Optional[Dict]:
        """Get summoner information by summoner name"""
        url = f"https://{self.region}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summoner_name}"
        try:
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                return response.json()
            else:
                st.error(f"Error fetching summoner: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            st.error(f"Exception: {str(e)}")
            return None

    def get_champion_mastery(self, puuid: str, count: int = 10) -> Optional[List[Dict]]:
        """Get champion mastery for a summoner"""
        url = f"https://{self.region}.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-puuid/{puuid}/top"
        try:
            response = requests.get(url, headers=self.headers, params={"count": count})
            if response.status_code == 200:
                return response.json()
            else:
                st.error(f"Error fetching champion mastery: {response.status_code}")
                return None
        except Exception as e:
            st.error(f"Exception: {str(e)}")
            return None

    def get_match_ids(self, puuid: str, count: int = 10) -> Optional[List[str]]:
        """Get match IDs for a summoner"""
        url = f"https://{self.routing}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids"
        try:
            response = requests.get(url, headers=self.headers, params={"count": count})
            if response.status_code == 200:
                return response.json()
            else:
                st.error(f"Error fetching match IDs: {response.status_code}")
                return None
        except Exception as e:
            st.error(f"Exception: {str(e)}")
            return None

    def get_match_details(self, match_id: str) -> Optional[Dict]:
        """Get match details by match ID"""
        url = f"https://{self.routing}.api.riotgames.com/lol/match/v5/matches/{match_id}"
        try:
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                return response.json()
            else:
                st.error(f"Error fetching match details: {response.status_code}")
                return None
        except Exception as e:
            st.error(f"Exception: {str(e)}")
            return None


def display_champion_mastery(mastery_data: List[Dict]):
    """Display champion mastery information"""
    st.subheader("🏆 Champion Mastery Top 10")

    if not mastery_data:
        st.warning("No champion mastery data available")
        return

    for idx, champ in enumerate(mastery_data, 1):
        col1, col2, col3, col4 = st.columns([1, 3, 2, 2])
        with col1:
            st.write(f"**#{idx}**")
        with col2:
            st.write(f"Champion ID: {champ['championId']}")
        with col3:
            st.write(f"Level: {champ['championLevel']}")
        with col4:
            st.write(f"Points: {champ['championPoints']:,}")


def display_match_history(match_data: List[Dict], summoner_puuid: str):
    """Display match history"""
    st.subheader("📊 Recent Match History")

    if not match_data:
        st.warning("No match history available")
        return

    for match in match_data:
        info = match.get('info', {})
        participants = info.get('participants', [])

        # Find the player's data in participants
        player_data = None
        for participant in participants:
            if participant.get('puuid') == summoner_puuid:
                player_data = participant
                break

        if not player_data:
            continue

        # Display match info
        game_mode = info.get('gameMode', 'Unknown')
        game_duration = info.get('gameDuration', 0) // 60  # Convert to minutes
        win = player_data.get('win', False)

        # Create expandable section for each match
        with st.expander(f"{'✅ Victory' if win else '❌ Defeat'} - {game_mode} ({game_duration} min)"):
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric("Champion", player_data.get('championName', 'Unknown'))
            with col2:
                kills = player_data.get('kills', 0)
                deaths = player_data.get('deaths', 0)
                assists = player_data.get('assists', 0)
                st.metric("KDA", f"{kills}/{deaths}/{assists}")
            with col3:
                cs = player_data.get('totalMinionsKilled', 0) + player_data.get('neutralMinionsKilled', 0)
                st.metric("CS", cs)
            with col4:
                damage = player_data.get('totalDamageDealtToChampions', 0)
                st.metric("Damage", f"{damage:,}")


# Main App
st.title("⚔️ League of Legends Data Viewer")
st.write("View match history and champion mastery for any summoner")

# Sidebar for configuration
with st.sidebar:
    st.header("Settings")

    # Region selection
    region = st.selectbox(
        "Region",
        ["jp1", "kr", "na1", "euw1", "eun1", "br1", "la1", "la2", "oc1", "ru", "tr1"],
        index=0
    )

    # Routing mapping
    routing_map = {
        "jp1": "asia", "kr": "asia",
        "na1": "americas", "br1": "americas", "la1": "americas", "la2": "americas",
        "euw1": "europe", "eun1": "europe", "ru": "europe", "tr1": "europe",
        "oc1": "sea"
    }
    routing = routing_map.get(region, "asia")

    # API Key input
    api_key_input = st.text_input("Riot API Key", value=RIOT_API_KEY, type="password")

    st.info("Get your API key from [Riot Developer Portal](https://developer.riotgames.com/)")

# Main content
summoner_name = st.text_input("Enter Summoner Name", placeholder="Hide on bush")

if st.button("Fetch Data") and summoner_name and api_key_input:
    api = RiotAPI(api_key_input, region=region, routing=routing)

    with st.spinner("Fetching summoner data..."):
        summoner = api.get_summoner_by_name(summoner_name)

    if summoner:
        st.success(f"Found summoner: {summoner['name']}")

        # Display basic info
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Summoner Level", summoner['summonerLevel'])
        with col2:
            st.metric("Profile Icon", summoner['profileIconId'])
        with col3:
            st.write(f"**PUUID:** {summoner['puuid'][:8]}...")

        st.divider()

        # Fetch and display champion mastery
        with st.spinner("Fetching champion mastery..."):
            mastery_data = api.get_champion_mastery(summoner['puuid'], count=10)

        if mastery_data:
            display_champion_mastery(mastery_data)

        st.divider()

        # Fetch and display match history
        with st.spinner("Fetching match history..."):
            match_ids = api.get_match_ids(summoner['puuid'], count=10)

        if match_ids:
            matches = []
            progress_bar = st.progress(0)
            for idx, match_id in enumerate(match_ids):
                match_details = api.get_match_details(match_id)
                if match_details:
                    matches.append(match_details)
                progress_bar.progress((idx + 1) / len(match_ids))
                time.sleep(0.1)  # Rate limiting

            progress_bar.empty()
            display_match_history(matches, summoner['puuid'])

elif summoner_name and not api_key_input:
    st.warning("⚠️ Please enter your Riot API Key in the sidebar")

# Instructions
with st.expander("ℹ️ How to use"):
    st.markdown("""
    ### Steps:
    1. Get your Riot API Key from [Riot Developer Portal](https://developer.riotgames.com/)
    2. Enter your API key in the sidebar
    3. Select your region
    4. Enter a summoner name
    5. Click "Fetch Data"

    ### Features:
    - 📊 View recent match history (last 10 games)
    - 🏆 View top 10 champion masteries
    - 📈 Detailed match statistics (KDA, CS, damage, etc.)

    ### Note:
    - Development API keys are rate-limited
    - Make sure to select the correct region for the summoner
    """)
