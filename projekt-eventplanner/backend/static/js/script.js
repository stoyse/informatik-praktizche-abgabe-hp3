document.addEventListener('DOMContentLoaded', function() {
    const discountList = document.getElementById('discount-list');
    const addDiscountBtn = document.getElementById('add-discount-btn');
    const discountInfoInput = document.getElementById('discount_info');
    const form = document.querySelector('form');

    // Array to store discount rules
    let discounts = [];

    function renderDiscounts() {
        discountList.innerHTML = '';
        discounts.forEach((discount, index) => {
            const row = document.createElement('div');
            row.style.display = 'flex';
            row.style.gap = '10px';
            row.style.marginBottom = '10px';
            row.style.alignItems = 'center';

            row.innerHTML = `
                <input type="number" placeholder="Personen ab" value="${discount.people}" class="discount-people" data-index="${index}" style="flex:1; padding: 8px; border: 1px solid #ddd; border-radius: 4px;">
                <input type="number" placeholder="Rabatt %" value="${discount.percent}" class="discount-percent" data-index="${index}" style="flex:1; padding: 8px; border: 1px solid #ddd; border-radius: 4px;">
                <button type="button" class="remove-discount" data-index="${index}" style="background: #ff4444; color: white; border: none; border-radius: 4px; padding: 0 10px; cursor: pointer;">&times;</button>
            `;
            discountList.appendChild(row);
        });
        updateHiddenInput();
    }

    function updateHiddenInput() {
        // Serialize to JSON string
        discountInfoInput.value = JSON.stringify(discounts);
    }

    addDiscountBtn.addEventListener('click', function() {
        discounts.push({ people: '', percent: '' });
        renderDiscounts();
    });

    discountList.addEventListener('input', function(e) {
        if (e.target.classList.contains('discount-people')) {
            const index = e.target.dataset.index;
            discounts[index].people = e.target.value;
            updateHiddenInput();
        }
        if (e.target.classList.contains('discount-percent')) {
            const index = e.target.dataset.index;
            discounts[index].percent = e.target.value;
            updateHiddenInput();
        }
    });

    discountList.addEventListener('click', function(e) {
        if (e.target.classList.contains('remove-discount')) {
            const index = e.target.dataset.index;
            discounts.splice(index, 1);
            renderDiscounts();
        }
    });

    // Form Validation before submit
    form.addEventListener('submit', function(e) {
        // Basic validation example
        const price = document.getElementById('price').value;
        if (price < 0) {
            e.preventDefault();
            alert('Der Preis darf nicht negativ sein.');
            return;
        }
        
        // Clean up empty discounts
        discounts = discounts.filter(d => d.people && d.percent);
        updateHiddenInput();
    });
});
