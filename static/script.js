document.addEventListener('DOMContentLoaded', function() {
    const searchForm = document.getElementById('search-form');
    const searchInput = document.getElementById('search-input');
    const searchButton = document.getElementById('search-button');
    const table = document.querySelector('table tbody');
    
    searchButton.addEventListener('click', function() {
        const searchText = searchInput.value.toLowerCase();
        
        for (const row of table.rows) {
            const studentName = row.cells[1].textContent.toLowerCase();
            if (studentName.includes(searchText)) {
                row.style.display = '';
            } else {
                row.style.display = 'none';
            }
        }
    });
});
