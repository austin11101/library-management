document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('search-form');
    const queryInput = document.getElementById('query');
    const resultsDiv = document.getElementById('results');
    
    form.addEventListener('submit', async (event) => {
        event.preventDefault(); // Prevent form submission
        
        const query = queryInput.value;
        const url = `https://www.googleapis.com/books/v1/volumes?q=${encodeURIComponent(query)}`;

        try {
            const response = await fetch(url);
            const data = await response.json();

            // Clear previous results
            resultsDiv.innerHTML = '';

            if (data.items) {
                data.items.forEach(item => {
                    const title = item.volumeInfo.title || 'No title';
                    const authors = item.volumeInfo.authors ? item.volumeInfo.authors.join(', ') : 'Unknown author';
                    const thumbnail = item.volumeInfo.imageLinks ? item.volumeInfo.imageLinks.thumbnail : 'https://via.placeholder.com/128x192?text=No+Image';

                    resultsDiv.innerHTML += `
                        <div class="book">
                            <img src="${thumbnail}" alt="Book cover">
                            <h3>${title}</h3>
                            <p><strong>Author(s):</strong> ${authors}</p>
                        </div>
                    `;
                });
            } else {
                resultsDiv.innerHTML = '<p>No books found.</p>';
            }
        } catch (error) {
            resultsDiv.innerHTML = '<p>Error fetching book data.</p>';
            console.error('Error:', error);
        }
    });
});
