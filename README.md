# Vinyl Unwrapped 💿

A Spotify Wrapped-style visualization for vinyl record collections and Last.fm statistics. Check it out at [unwrapped.russ.fm](https://unwrapped.russ.fm)! 🎵

## Features 🌟

- 📊 Display of vinyl collection statistics
- 🎧 Integration with Last.fm listening data
- 📈 Interactive charts showing genre distribution
- 🆕 Recent additions to your collection
- 📱 Responsive design that works on all devices
- 🔗 Links to russ.fm for more details about each album

## Collection Generation 🛠️

The project uses `generate_collection.py` to fetch your vinyl collection data from Discogs. To set this up:

1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and add your Discogs credentials:
   - `DISCOGS_TOKEN`: Your Discogs API token
   - `DISCOGS_USERNAME`: Your Discogs username
   - `DISCOGS_RATE_LIMIT_DELAY`: Delay between API calls (default: 2 seconds)
   - `ENABLE_DEBUG`: Set to true for verbose output

3. Run the script:
   ```bash
   # Generate current year's collection
   python generate_collection.py

   # Generate collection for a specific year
   python generate_collection.py --year 2020
   ```

The script will generate a JSON file (e.g., `collection_2020.json`) in the `public` directory containing all records added to your collection during that year.

## Development 👨‍💻

To run the development server:

```bash
npm install
npm run dev
```

## Building for Production 🏗️

To create a production build:

```bash
npm run build
```

The built files will be in the `dist` directory, ready to be deployed to Cloudflare Pages.

## Deployment 🚀

This project is designed to be deployed to Cloudflare Pages. The build command should be set to `npm run build` and the build output directory should be set to `dist`.

## Technologies Used ⚡

- Vue 3
- Vite
- TailwindCSS
- Chart.js
- Day.js
