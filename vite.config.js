import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import fs from 'fs'
import path from 'path'

export default defineConfig({
  plugins: [vue()],
  build: {
    outDir: 'dist',
    assetsDir: 'assets'
  },
  server: {
    middleware: [
      {
        name: 'years-api',
        configureServer(server) {
          server.middlewares.use('/api/years', (req, res) => {
            // Set CORS headers
            res.setHeader('Access-Control-Allow-Origin', '*')
            res.setHeader('Access-Control-Allow-Methods', 'GET')
            res.setHeader('Access-Control-Allow-Headers', 'Content-Type')
            
            if (req.method === 'OPTIONS') {
              res.statusCode = 204
              res.end()
              return
            }

            try {
              const publicDir = path.resolve(__dirname, 'public')
              if (!fs.existsSync(publicDir)) {
                throw new Error('Public directory not found')
              }

              const files = fs.readdirSync(publicDir)
              const years = files
                .filter(file => file.startsWith('collection_') && file.endsWith('.json'))
                .map(file => file.replace('collection_', '').replace('.json', ''))
                .sort((a, b) => b - a)
              
              if (years.length === 0) {
                console.warn('No collection files found in public directory')
              }

              res.setHeader('Content-Type', 'application/json')
              res.end(JSON.stringify(years))
            } catch (error) {
              console.error('Error reading collection files:', error)
              res.statusCode = 500
              res.end(JSON.stringify({ 
                error: 'Failed to load years',
                details: error.message 
              }))
            }
          })
        }
      }
    ]
  }
})
