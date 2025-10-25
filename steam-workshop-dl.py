import streamlit as st
import subprocess
import re
import os

st.set_page_config(page_title="Steam Workshop Downloader", page_icon="🎮", layout="centered")

st.title("🎮 Steam Workshop Downloader (SteamCMD Method)")
st.write("Download Steam Workshop items using SteamCMD (official Valve-supported method).")

steamcmd_path = st.text_input("Enter path to SteamCMD executable:", value="C:\\steamcmd\\steamcmd.exe")
url = st.text_input("Enter Steam Workshop URL:")

def extract_workshop_id(url: str):
    """Extract the numeric workshop item ID from a Steam Workshop URL."""
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

# Step 1: Extract ID
if st.button("Next"):
    if not url:
        st.warning("Please enter a valid Workshop URL.")
    else:
        item_id = extract_workshop_id(url)
        if not item_id:
            st.error("Could not extract Workshop item ID from the URL.")
        else:
            st.session_state["item_id"] = item_id
            st.success(f"Workshop Item ID detected: {item_id}")

# Step 2: Show App ID + Download only after ID is extracted
if "item_id" in st.session_state:
    st.divider()
    st.subheader("Step 2: Enter App ID and Download")
    app_id = st.text_input("Enter the Steam App ID (e.g. 289070 for Civilization VI):", value="")
    if st.button("Download Item"):
        if not app_id:
            st.warning("Please enter the Steam App ID.")
        else:
            item_id = st.session_state["item_id"]
            st.info(f"Downloading item {item_id} from app {app_id} ...")
            stdout, stderr = download_workshop_item(app_id, item_id, steamcmd_path)
            if stdout:
                st.text_area("SteamCMD Output", stdout, height=200)
            if stderr:
                st.text_area("Errors", stderr, height=150)
            if stdout and "Success" in stdout:
                st.success("✅ Download completed! Check your steamcmd/workshop/content folder.")
