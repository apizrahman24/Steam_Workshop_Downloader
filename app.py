import streamlit as st
import requests
import os

st.set_page_config(page_title="Steam Workshop Downloader", page_icon="🎮", layout="centered")

st.title("🎮 Steam Workshop Downloader")
st.write("Download public items from the Steam Workshop easily.")

url = st.text_input("Enter Steam Workshop URL:")

def extract_workshop_id(url: str):
    if "?id=" in url:
        return url.split("?id=")[-1].split("&")[0]
    elif "/filedetails/" in url:
        return url.split("/filedetails/")[1].split("/")[0]
    return None

if st.button("Download"):
    if not url:
        st.warning("Please enter a valid Workshop URL.")
    else:
        item_id = extract_workshop_id(url)
        if not item_id:
            st.error("Could not extract Workshop item ID from the URL.")
        else:
            st.info(f"Fetching item {item_id}...")
            api_url = f"https://api.steamworkshopdownloader.io/api/download/item"
            payload = {"publishedFileId": item_id, "collectionId": None, "hidden": False}

            try:
                response = requests.post(api_url, json=payload)
                if response.status_code == 200:
                    data = response.json()
                    if "url" in data:
                        download_url = data["url"]
                        st.success("✅ Item ready for download!")
                        st.markdown(f"[Click here to download]({download_url})")
                    else:
                        st.error("No downloadable link returned by the API.")
                else:
                    st.error(f"API error: {response.status_code}")
            except Exception as e:
                st.error(f"Error: {e}")
