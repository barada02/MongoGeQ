document.addEventListener('DOMContentLoaded', function() {
    const API_URL = 'http://localhost:8000';
    const itemForm = document.getElementById('itemForm');
    const itemsList = document.getElementById('itemsList');
    const refreshBtn = document.getElementById('refreshBtn');
    
    // Load items when page loads
    fetchItems();
    
    // Event listeners
    itemForm.addEventListener('submit', addItem);
    refreshBtn.addEventListener('click', fetchItems);
    
    // Fetch all items from the API
    function fetchItems() {
        fetch(`${API_URL}/items`)
            .then(response => response.json())
            .then(data => {
                displayItems(data);
            })
            .catch(error => {
                console.error('Error fetching items:', error);
                itemsList.innerHTML = '<p>Error loading items. Please try again later.</p>';
            });
    }
    
    // Display items in the list
    function displayItems(items) {
        if (items.length === 0) {
            itemsList.innerHTML = '<p>No items found. Add some items!</p>';
            return;
        }
        
        let html = '';
        items.forEach(item => {
            html += `
                <div class="item-card">
                    <h3>${item.name}</h3>
                    <p>${item.description || 'No description'}</p>
                    <p class="price">$${item.price.toFixed(2)}</p>
                    <small>ID: ${item._id}</small>
                </div>
            `;
        });
        
        itemsList.innerHTML = html;
    }
    
    // Add a new item
    function addItem(e) {
        e.preventDefault();
        
        const name = document.getElementById('name').value;
        const description = document.getElementById('description').value;
        const price = parseFloat(document.getElementById('price').value);
        
        const newItem = {
            name,
            description,
            price
        };
        
        fetch(`${API_URL}/items`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(newItem)
        })
        .then(response => response.json())
        .then(data => {
            console.log('Success:', data);
            itemForm.reset();
            fetchItems();
        })
        .catch(error => {
            console.error('Error adding item:', error);
        });
    }
});