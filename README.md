# Vinyl Unwrapped

A Spotify Wrapped-style visualization for vinyl record collections and Last.fm statistics.

## Features

- Display of vinyl collection statistics
- Integration with Last.fm listening data
- Interactive charts showing genre distribution
- Recent additions to your collection
- Responsive design that works on all devices
- Links to russ.fm for more details about each album

## Development

To run the development server:

```bash
npm install
npm run dev
```

## Building for Production

To create a production build:

```bash
npm run build
```

The built files will be in the `dist` directory, ready to be deployed to Cloudflare Pages.

## Deployment

This project is designed to be deployed to Cloudflare Pages. The build command should be set to `npm run build` and the build output directory should be set to `dist`.

## Technologies Used

- Vue 3
- Vite
- TailwindCSS
- Chart.js
- Day.js
