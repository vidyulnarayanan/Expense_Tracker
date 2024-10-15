document.getElementById('add-expense-form').addEventListener('submit', function(event) {
    event.preventDefault();

    // Validate fields
    const description = document.getElementById('description').value;
    const amount = document.getElementById('amount').value;
    const date = document.getElementById('date').value;
    const category = document.getElementById('category').value;

    // Ensure all fields are filled and amount is greater than 0
    if (description && amount > 0 && date && category) {
        // Post data to the server
        fetch('/add-expense/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector('input[name="csrfmiddlewaretoken"]').value
            },
            body: JSON.stringify({
                description: description,
                amount: parseFloat(amount),
                date: date,
                category: category
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Show confirmation message
                document.getElementById('confirmation-message').style.display = 'block';
                document.getElementById('error-message').style.display = 'none';

                // Clear form fields
                document.getElementById('add-expense-form').reset();
            } else {
                // Show error message
                document.getElementById('confirmation-message').style.display = 'none';
                document.getElementById('error-message').style.display = 'block';
            }
        })
        .catch(error => {
            console.error('Error:', error);
            document.getElementById('error-message').style.display = 'block';
            document.getElementById('confirmation-message').style.display = 'none';
        });
    } else {
        // Show error message for validation issues
        document.getElementById('error-message').style.display = 'block';
        document.getElementById('confirmation-message').style.display = 'none';
    }
});
