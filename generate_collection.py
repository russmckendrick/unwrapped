import os
import json
import time
from datetime import datetime
from dotenv import load_dotenv
import discogs_client
import logging
import requests
import argparse

# Load environment variables
load_dotenv()

# Configuration
USERNAME = os.getenv('DISCOGS_USERNAME', 'russmck')
MAX_RETRIES = 3
RETRY_DELAY = int(os.getenv('DISCOGS_RATE_LIMIT_DELAY', '2'))  # seconds between retries

# Set up logging based on environment variable
log_level = logging.DEBUG if os.getenv('ENABLE_DEBUG', 'false').lower() == 'true' else logging.INFO
logging.basicConfig(level=log_level)
logger = logging.getLogger(__name__)

def get_discogs_client():
    """Initialize and return Discogs client"""
    token = os.getenv('DISCOGS_TOKEN')
    if not token:
        raise ValueError("Please set DISCOGS_TOKEN in your .env file")
    
    return discogs_client.Client(
        'VinylUnwrapped/1.0',
        user_token=token
    )

def get_format_info(format_obj):
    """Safely extract format information"""
    if isinstance(format_obj, dict):
        return {
            'name': format_obj.get('name', 'Unknown Format'),
            'qty': format_obj.get('qty', '1'),
            'text': format_obj.get('text', ''),
            'descriptions': format_obj.get('descriptions', [])
        }
    return {
        'name': getattr(format_obj, 'name', 'Unknown Format'),
        'qty': getattr(format_obj, 'qty', '1'),
        'text': getattr(format_obj, 'text', ''),
        'descriptions': getattr(format_obj, 'descriptions', [])
    }

def get_label_info(label):
    """Safely extract label information"""
    if isinstance(label, dict):
        return label.get('name', 'Unknown Label')
    return getattr(label, 'name', 'Unknown Label')

def fetch_russ_fm_data():
    """Fetch image data from russ.fm"""
    try:
        response = requests.get('https://www.russ.fm/index.json')
        response.raise_for_status()
        return response.json().get('documents', [])
    except Exception as e:
        logger.error(f"Error fetching russ.fm data: {str(e)}")
        return []

def create_image_lookup(russ_fm_data):
    """Create lookup tables for cover and artist images"""
    cover_images = {}
    artist_images = {}
    album_uris = {}
    artist_uris = {}
    
    for item in russ_fm_data:
        discogs_id = item.get('discogsRelease')
        if discogs_id:
            cover_images[discogs_id] = item.get('coverImage')
            artist_images[discogs_id] = item.get('artistImage')
            album_uris[discogs_id] = item.get('albumUri')
            artist_uris[discogs_id] = item.get('artistUri')
    
    return cover_images, artist_images, album_uris, artist_uris

def fetch_collection(year):
    """Fetch collection items added in specified year"""
    d = get_discogs_client()
    user = d.user(USERNAME)
    collection = user.collection_folders[0].releases
    
    # Get image lookups from russ.fm
    cover_images, artist_images, album_uris, artist_uris = create_image_lookup(fetch_russ_fm_data())
    
    items = []
    page = 1
    
    while True:
        try:
            logger.debug(f"Fetching page {page}")
            releases = collection.page(page)
            if not releases:
                logger.debug("No more releases found")
                break
                
            for item in releases:
                try:
                    # Get the date added - it's already a datetime object
                    date_added = item.date_added
                    
                    # Check if it was added in the specified year
                    if date_added.year == year:
                        logger.debug(f"Processing release: {item.release.title}")
                        logger.debug(f"Format data: {item.release.formats}")
                        
                        release_data = {
                            'id': item.id,
                            'title': item.release.title,
                            'artist': [artist.name for artist in item.release.artists],
                            'date_added': item.date_added.isoformat(),
                            'year': item.release.year,
                            'formats': [get_format_info(format_obj) for format_obj in item.release.formats],
                            'labels': [get_label_info(label) for label in item.release.labels],
                            'genres': item.release.genres,
                            'styles': item.release.styles if hasattr(item.release, 'styles') else [],
                            'cover_image': cover_images.get(str(item.release.id)),
                            'artist_image': artist_images.get(str(item.release.id)),
                            'album_uri': album_uris.get(str(item.release.id)),
                            'artist_uri': artist_uris.get(str(item.release.id))
                        }
                        items.append(release_data)
                except Exception as e:
                    logger.error(f"Error processing item: {str(e)}")
                    continue
            
            # Add delay between pages to respect rate limits
            time.sleep(RETRY_DELAY)
            page += 1
            
        except discogs_client.exceptions.HTTPError as e:
            if e.status_code == 429:  # Rate limit exceeded
                retry_after = int(e.response.headers.get('Retry-After', RETRY_DELAY))
                logger.warning(f"Rate limit hit, waiting {retry_after} seconds...")
                time.sleep(retry_after)
                continue
            elif e.status_code == 404:  # Page not found - we've reached the end
                logger.debug("Reached the last page")
                break
            else:
                raise
    
    logger.info(f"Found {len(items)} items from {year}")
    return items

def save_collection(items, output_file):
    """Save collection to JSON file"""
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(items, f, indent=2, ensure_ascii=False)
    logger.info(f"Saved {len(items)} items to {output_file}")

def main():
    """Main function to fetch and save collection data"""
    parser = argparse.ArgumentParser(description='Generate Discogs collection JSON for a specific year')
    parser.add_argument('--year', type=int, default=datetime.now().year,
                      help='Year to generate collection data for (default: current year)')
    args = parser.parse_args()
    
    output_file = f"public/collection_{args.year}.json"
    
    # Ensure public directory exists
    os.makedirs('public', exist_ok=True)
    
    print(f"Fetching {args.year} collection for user: {USERNAME}")
    items = fetch_collection(args.year)
    save_collection(items, output_file)
    print(f"Successfully saved {len(items)} items to {output_file}")
    
    return items

if __name__ == "__main__":
    main()
