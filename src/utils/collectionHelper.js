/**
 * Get artist image and URL from collection data
 * @param {string} artistName - Name of the artist to find
 * @param {Array} collection - Collection data array
 * @returns {Object} Object containing artist image and URL
 */
export function getArtistImageFromCollection(artistName, collection) {
  // Find the first album in the collection by this artist
  const artistAlbum = collection.find(item => {
    if (Array.isArray(item.artist)) {
      return item.artist.some(artist => artist === artistName)
    }
    return item.artist === artistName
  })

  if (artistAlbum) {
    return {
      artistImage: artistAlbum.artist_image,
      artistUrl: artistAlbum.artist_url
    }
  }

  return null
}
