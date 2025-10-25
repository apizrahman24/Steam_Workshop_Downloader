import streamlit as st
import subprocess
import os
import re

st.set_page_config(page_title="Steam Workshop Downloader", page_icon="🎮", layout="centered")

st.title("🎮 Steam Workshop Downloader (SteamCMD Method)")
st.write("Download Steam Workshop items using SteamCMD (official method).")

url = st.text_input("Enter Steam Workshop URL:")
steamcmd_path = st.text_input("Enter path to SteamCMD executable:", value="C:\\steamcmd\\steamcmd.exe")

def extract_workshop_id(url: str):
    """Extracts the numeric workshop item ID from a Steam Workshop URL."""
    match = re.search(r"id=(\d+)", url)
    return match.group(1) if match else None

def download_workshop_item(app_id: str, item_id: str, steamcmd_path: str):
    """Runs SteamCMD to download a workshop item."""
    cmd = [
        steamcmd_path,
        "+login", "anonymous",
        "+workshop_download_item", app_id, item_id,
        "+quit"
    ]
    try:
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return result.stdout, result.stderr
    except Exception as e:
        return None, str(e)

if st.button("Download"):
    if not url:
        st.warning("Please enter a valid Workshop URL.")
    else:
        item_id = extract_workshop_id(url)
        if not item_id:
            st.error("Could not extract Workshop item ID from URL.")
        else:
            # You must know the appid (game ID)
            app_id = st.text_input("Enter the Steam App ID for this workshop item (e.g., 294100 for RimWorld):", value="")
            if not app_id:
                st.warning("Please enter the Steam App ID of the game.")
            else:
                st.info(f"Downloading item {item_id} from app {app_id} ...")
                stdout, stderr = download_workshop_item(app_id, item_id, steamcmd_path)
                if stdout:
                    st.text_area("SteamCMD Output", stdout, height=200)
                if stderr:
                    st.text_area("Errors", stderr, height=150)
                if "Success" in stdout:
                    st.success("✅ Download completed! Check your steamcmd/workshop/content folder.")
