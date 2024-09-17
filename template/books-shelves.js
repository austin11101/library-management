document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('search-form');
    const queryInput = document.getElementById('query');
    const resultsDiv = document.getElementById('results');
    const selectedBooksDiv = document.getElementById('selected-books');
    const viewChartButton = document.getElementById('view-chart');
    const chartDiv = document.getElementById('chart');
    
    let selectedBooks = [];

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
                    
                    // Create a book element
                    const bookElement = document.createElement('div');
                    bookElement.classList.add('book');
                    bookElement.innerHTML = `
                        <img src="${thumbnail}" alt="Book cover">
                        <h3>${title}</h3>
                        <p><strong>Author(s):</strong> ${authors}</p>
                        <button class="select-btn">Select</button>
                    `;

                    // Add event listener to select button
                    bookElement.querySelector('.select-btn').addEventListener('click', () => {
                        if (!selectedBooks.some(book => book.title === title)) {
                            selectedBooks.push({ title, authors, thumbnail });
                            updateSelectedBooks();
                        }
                    });

                    resultsDiv.appendChild(bookElement);
                });
            } else {
                resultsDiv.innerHTML = '<p>No books found.</p>';
            }
        } catch (error) {
            resultsDiv.innerHTML = '<p>Error fetching book data.</p>';
            console.error('Error:', error);
        }
    });

    function updateSelectedBooks() {
        selectedBooksDiv.innerHTML = '';
        selectedBooks.forEach(book => {
            selectedBooksDiv.innerHTML += `
                <div class="selected-book">
                    <img src="${book.thumbnail}" alt="Book cover">
                    <h3>${book.title}</h3>
                    <p><strong>Author(s):</strong> ${book.authors}</p>
                </div>
            `;
        });
    }

    viewChartButton.addEventListener('click', () => {
        chartDiv.innerHTML = '';
        selectedBooks.forEach(book => {
            chartDiv.innerHTML += `
                <div class="chart-item">
                    <img src="${book.thumbnail}" alt="Book cover">
                    <h3>${book.title}</h3>
                    <p><strong>Author(s):</strong> ${book.authors}</p>
                </div>
            `;
        });
        chartDiv.style.display = 'block';
    });
});
