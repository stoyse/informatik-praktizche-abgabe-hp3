document.addEventListener('DOMContentLoaded', function() {
    const participantsInput = document.getElementById('participants');
    const discountDisplay = document.getElementById('discount-display');
    const totalPriceDisplay = document.getElementById('total-price-display');
    const subtotalDisplay = document.getElementById('subtotal-display');

    if (!participantsInput) return; // If form is not present (e.g. sold out)

    function calculatePrice() {
        const count = parseInt(participantsInput.value) || 0;
        let currentDiscount = 0;

        // Find applicable discount
        // Sort discounts by people count descending to find the highest applicable tier
        const sortedDiscounts = discountInfo.sort((a, b) => b.people - a.people);
        
        for (const rule of sortedDiscounts) {
            if (count >= parseInt(rule.people)) {
                currentDiscount = parseFloat(rule.percent);
                break;
            }
        }

        const totalBase = basePrice * count;
        const discountAmount = totalBase * (currentDiscount / 100);
        const finalPrice = totalBase - discountAmount;

        // Update UI
        if (subtotalDisplay) {
            subtotalDisplay.textContent = `${totalBase.toFixed(2)} €`;
        }
        discountDisplay.textContent = `${currentDiscount}% (-${discountAmount.toFixed(2)} €)`;
        totalPriceDisplay.textContent = `${finalPrice.toFixed(2)} €`;
    }

    participantsInput.addEventListener('input', calculatePrice);
    
    // Initial calculation
    calculatePrice();

    // Handle Form Submission via AJAX
    const reservationForm = document.getElementById('reservation-form');
    if (reservationForm) {
        reservationForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(reservationForm);
            
            fetch(reservationForm.action, {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    alert(data.error);
                } else if (data.success) {
                    window.location.reload();
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Ein Fehler ist aufgetreten.');
            });
        });
    }
});
