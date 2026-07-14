import xml.etree.ElementTree as ET
import pandas as pd
from openai import OpenAI  # Ollama uses the official OpenAI compatibility layer
import os
import json

# --- CONFIGURATION ---
XML_INPUT_PATH = "rekordbox_collection.xml"
EXCEL_OUTPUT_PATH = "missing_genres_suggestions.xlsx"
XML_OUTPUT_PATH = "rekordbox_genres_updated.xml"
BATCH_SIZE = 15  # Slightly lower batch size for local LLMs to manage context window context easily
OLLAMA_MODEL = "llama3"  # Change to your local model, e.g., "mistral", "gemma"

# Point the OpenAI client to your local Ollama server instance
client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"  # Required field, but ignored by Ollama
)

def parse_rekordbox_xml(xml_path):
    print("Parsing Rekordbox XML...")
    tree = ET.parse(xml_path)
    root = tree.getroot()
    
    collection = root.find('COLLECTION')
    missing_genre_tracks = []
    all_tracks_dict = {}
    
    for track in collection.findall('TRACK'):
        attrib = track.attrib
        track_id = attrib.get('TrackID')
        genre = attrib.get('Genre', '').strip()
        
        all_tracks_dict[track_id] = attrib
        
        if not genre:
            missing_genre_tracks.append({
                'TrackID': track_id,
                'Name': attrib.get('Name', ''),
                'Artist': attrib.get('Artist', ''),
                'Album': attrib.get('Album', ''),
                'Original_Genre': genre
            })
            
    print(f"Found {len(missing_genre_tracks)} tracks missing a genre.")
    return missing_genre_tracks, tree, all_tracks_dict

def get_llm_genre_suggestions_batched(tracks):
    print(f"Consulting local Ollama ({OLLAMA_MODEL}) in batches of {BATCH_SIZE}...")
    updated_tracks = []
    
    for i in range(0, len(tracks), BATCH_SIZE):
        batch = tracks[i:i + BATCH_SIZE]
        print(f"Processing tracks {i+1} to {min(i + BATCH_SIZE, len(tracks))}...")
        
        batch_input = [{"TrackID": t["TrackID"], "Artist": t["Artist"], "Title": t["Name"], "Album": t["Album"]} for t in batch]
        
        prompt = f"""Identify the primary electronic music/DJ genre for these tracks. 
Return a JSON object with a 'genres' key mapping TrackID to the genre string (max 3 words, e.g., 'House', 'Techno', 'Drum & Bass').

Tracks:
{json.dumps(batch_input, indent=2)}"""
        
        try:
            response = client.chat.completions.create(
                model=OLLAMA_MODEL,
                response_format={"type": "json_object"},  # Forces Ollama to reply in JSON
                messages=[
                    {"role": "system", "content": "You are an expert DJ and music archivist. You always respond with valid JSON matching the requested schema. Do not include conversational text or explanations."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2
            )
            
            result_json = json.loads(response.choices[0].message.content)
            genre_map = result_json.get("genres", {})
            
            for track in batch:
                track['Suggested_Genre'] = genre_map.get(track['TrackID'], "Unknown").strip()
                updated_tracks.append(track)
                
        except Exception as e:
            print(f"Error processing batch starting at {i}: {e}")
            for track in batch:
                track['Suggested_Genre'] = "Unknown"
                updated_tracks.append(track)
                
    return updated_tracks

def generate_excel_and_xml(updated_tracks, tree):
    df = pd.DataFrame(updated_tracks)
    df.to_excel(EXCEL_OUTPUT_PATH, index=False)
    print(f"Saved suggestions spreadsheet to: {EXCEL_OUTPUT_PATH}")

    # Build lookup of suggested genres
    genre_lookup = {
        track["TrackID"]: track["Suggested_Genre"]
        for track in updated_tracks
    }

    root = tree.getroot()
    collection = root.find("COLLECTION")

    # Update only tracks that received suggestions
    for track in collection.findall("TRACK"):
        track_id = track.attrib.get("TrackID")
        if track_id in genre_lookup:
            track.attrib["Genre"] = genre_lookup[track_id]

    tree.write(XML_OUTPUT_PATH, encoding="utf-8", xml_declaration=True)
    print(f"Saved updated Rekordbox XML to: {XML_OUTPUT_PATH}")

if __name__ == "__main__":
    if not os.path.exists(XML_INPUT_PATH):
        print(f"Error: Missing '{XML_INPUT_PATH}'")
    else:
        missing_tracks, original_tree, full_dict = parse_rekordbox_xml(XML_INPUT_PATH)
        if missing_tracks:
            # SAFETY TEST: Run just the first batch (e.g., [:15]) to check formatting compatibility with your local model
            completed_tracks = get_llm_genre_suggestions_batched(missing_tracks[:15])
            generate_excel_and_xml(completed_tracks, original_tree)
            print("\nDone!")
        else:
            print("No tracks missing a genre found!")