#!/usr/bin/env python3
"""
Vinyl Collection Generator for Unwrapped

This script generates a JSON file containing information about vinyl records added to a
Discogs collection during a specified year. It interfaces with both the Discogs API
and a custom russ.fm API to gather comprehensive record information including cover art
and artist images.

Environment Variables:
    DISCOGS_TOKEN: Your Discogs API token (required)
    DISCOGS_USERNAME: Your Discogs username (default: russmck)
    ENABLE_DEBUG: Set to 'true' for debug logging (default: false)
    DISCOGS_RATE_LIMIT_DELAY: Delay between API calls in seconds (default: 2)

Usage:
    python generate_collection.py --year YYYY

Example:
    python generate_collection.py --year 2024

The script will create a JSON file named 'YYYY_collection.json' containing all vinyl
records added to your collection in the specified year.
"""

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
    """
    Initialize and return a Discogs API client.
    
    Returns:
        discogs_client.Client: Authenticated Discogs client instance
        
    Raises:
        ValueError: If DISCOGS_TOKEN environment variable is not set
    """
    token = os.getenv('DISCOGS_TOKEN')
    if not token:
        raise ValueError("Please set DISCOGS_TOKEN in your .env file")
    
    return discogs_client.Client(
        'VinylUnwrapped/1.0',
        user_token=token
    )

def get_format_info(format_obj):
    """
    Safely extract format information from a Discogs format object.
    
    Args:
        format_obj (Union[dict, object]): Format information from Discogs API
        
    Returns:
        dict: Normalized format information containing:
            - name: Format name (e.g., 'Vinyl')
            - qty: Quantity of items in this format
            - text: Additional format text (e.g., 'Crystal Clear')
            - descriptions: List of format descriptions (e.g., ['LP', 'Album'])
    """
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
    """
    Extract relevant information from a Discogs label object.
    
    Args:
        label (Union[dict, object]): Label information from Discogs API
        
    Returns:
        str: Label name
    """
    if isinstance(label, dict):
        return label.get('name', 'Unknown Label')
    return getattr(label, 'name', 'Unknown Label')

def fetch_russ_fm_data():
    """
    Fetch image data from russ.fm API.
    
    Returns:
        list: List of image data from russ.fm API
    """
    try:
        response = requests.get('https://www.russ.fm/index.json')
        response.raise_for_status()
        return response.json().get('documents', [])
    except Exception as e:
        logger.error(f"Error fetching russ.fm data: {str(e)}")
        return []

def create_image_lookup(russ_fm_data):
    """
    Create lookup tables for cover and artist images.
    
    Args:
        russ_fm_data (list): List of image data from russ.fm API
        
    Returns:
        tuple: Tuple containing:
            - cover_images: Dictionary mapping Discogs IDs to cover image URLs
            - artist_images: Dictionary mapping Discogs IDs to artist image URLs
            - album_uris: Dictionary mapping Discogs IDs to album URIs
            - artist_uris: Dictionary mapping Discogs IDs to artist URIs
    """
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
    """
    Fetch collection items added in specified year.
    
    Args:
        year (int): Year to fetch collection data for
        
    Returns:
        list: List of collection items added in the specified year
    """
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
                    # Get the date added from the data property
                    date_added = datetime.strptime(item.data['date_added'], "%Y-%m-%dT%H:%M:%S%z")
                    
                    # Check if it was added in the specified year
                    if date_added.year == year:
                        basic_info = item.data['basic_information']
                        logger.debug(f"Processing release: {basic_info['title']}")
                        logger.debug(f"Format data: {basic_info['formats']}")
                        
                        release_data = {
                            'id': item.data['id'],
                            'title': basic_info['title'],
                            'artist': [artist['name'] for artist in basic_info['artists']],
                            'date_added': item.data['date_added'],
                            'year': basic_info['year'],
                            'formats': [get_format_info(format_obj) for format_obj in basic_info['formats']],
                            'labels': [get_label_info(label) for label in basic_info['labels']],
                            'genres': basic_info['genres'],
                            'styles': basic_info.get('styles', []),
                            'cover_image': cover_images.get(str(basic_info['id'])),
                            'artist_image': artist_images.get(str(basic_info['id'])),
                            'album_uri': album_uris.get(str(basic_info['id'])),
                            'artist_uri': artist_uris.get(str(basic_info['id']))
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
    """
    Save collection to JSON file.
    
    Args:
        items (list): List of collection items to save
        output_file (str): Path to output JSON file
    """
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(items, f, indent=2, ensure_ascii=False)
    logger.info(f"Saved {len(items)} items to {output_file}")

def main():
    """
    Main function to fetch and save collection data.
    
    This function:
    1. Parses command line arguments
    2. Fetches collection data for the specified year
    3. Saves the data to a JSON file named 'collection_YYYY.json'
    
    Command Line Arguments:
        --year: Year to generate collection data for (default: current year)
    
    Returns:
        None
    
    Raises:
        ValueError: If DISCOGS_TOKEN is not set
        requests.exceptions.RequestException: If API requests fail
        IOError: If there are issues writing the output file
    """
    parser = argparse.ArgumentParser(
        description='Generate Discogs collection JSON for a specific year',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    parser.add_argument('--year', type=int, default=datetime.now().year,
                      help='Year to generate collection data for (default: current year)')
    
    args = parser.parse_args()
    
    logger.info(f"Fetching {args.year} collection for user: {USERNAME}")
    
    # Fetch and save collection data
    output_file = f"{args.year}_collection.json"
    items = fetch_collection(args.year)
    save_collection(items, output_file)
    
    return items

if __name__ == "__main__":
    main()
