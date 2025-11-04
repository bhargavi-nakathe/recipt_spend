// Main JavaScript for receipt spending tracker
// File upload handling
document.addEventListener('DOMContentLoaded', function() {
    const uploadArea = document.getElementById('uploadArea');
    const fileInput = document.getElementById('fileInput');
    const processBtn = document.getElementById('processBtn');
    const resultsSection = document.getElementById('resultsSection');
    const resultsContent = document.getElementById('resultsContent');

    // Upload area click handler
    uploadArea.addEventListener('click', () => {
        fileInput.click();
    });

    // File selection handler
    fileInput.addEventListener('change', function(e) {
        if (this.files.length > 0) {
            processBtn.style.display = 'block';
            uploadArea.innerHTML = `<p>Selected: ${this.files[0].name}</p>`;
        }
    });

    // Process button handler
    processBtn.addEventListener('click', async function() {
        const file = fileInput.files[0];
        if (!file) return;

        const formData = new FormData();
        formData.append('receipt', file);

        try {
            const response = await fetch('/upload', {
                method: 'POST',
                body: formData
            });

            const result = await response.json();

            if (result.success) {
                displayResults(result);
            } else {
                alert('Error: ' + result.error);
            }
        } catch (error) {
            alert('Error processing receipt: ' + error.message);
        }
    });
});

function displayResults(result) {
    const resultsContent = document.getElementById('resultsContent');
    
    let html = `
        <div class="summary">
            <p><strong>Total Amount:</strong> $${result.total_amount.toFixed(2)}</p>
            <p><strong>Items Found:</strong> ${result.items_count}</p>
        </div>
        <div class="items-list">
            <h4>Items:</h4>
    `;

    result.items.forEach(item => {
        html += `
            <div class="item-row">
                <span>${item.name}</span>
                <span>$${item.amount.toFixed(2)}</span>
                <span class="category-badge">${item.category} (${item.confidence}%)</span>
            </div>
        `;
    });

    html += `</div>`;
    resultsContent.innerHTML = html;
    document.getElementById('resultsSection').style.display = 'block';
}