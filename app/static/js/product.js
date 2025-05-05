// JavaScript for product-specific pages

document.addEventListener('DOMContentLoaded', function() {
    // Product image gallery functionality
    const mainImage = document.getElementById('main-image');
    const thumbnails = document.querySelectorAll('.product-thumbnail');
    
    if (mainImage && thumbnails.length > 0) {
        thumbnails.forEach(thumbnail => {
            thumbnail.addEventListener('click', function(e) {
                // Update main image
                mainImage.src = this.querySelector('img').src;
                
                // Update active thumbnail
                thumbnails.forEach(t => t.classList.remove('border-indigo-500'));
                this.classList.add('border-indigo-500');
            });
        });
    }
    
    // Quantity selector
    const quantityInput = document.getElementById('quantity');
    const incrementBtn = document.getElementById('increment-quantity');
    const decrementBtn = document.getElementById('decrement-quantity');
    
    if (quantityInput && incrementBtn && decrementBtn) {
        incrementBtn.addEventListener('click', function() {
            const currentValue = parseInt(quantityInput.value);
            if (currentValue < 5) { // Maximum quantity
                quantityInput.value = currentValue + 1;
            }
        });
        
        decrementBtn.addEventListener('click', function() {
            const currentValue = parseInt(quantityInput.value);
            if (currentValue > 1) { // Minimum quantity
                quantityInput.value = currentValue - 1;
            }
        });
    }
    
    // Product creation/edit form
    const productForm = document.getElementById('product-form');
    
    if (productForm) {
        // Preview uploaded images
        const fileInput = document.getElementById('file-input');
        const previewContainer = document.getElementById('preview-container');
        
        if (fileInput && previewContainer) {
            fileInput.addEventListener('change', function() {
                previewContainer.innerHTML = '';
                
                if (this.files.length > 0) {
                    previewContainer.classList.remove('hidden');
                    
                    for (let i = 0; i < Math.min(this.files.length, 5); i++) {
                        const file = this.files[i];
                        if (!file.type.startsWith('image/')) continue;
                        
                        const reader = new FileReader();
                        reader.onload = function(e) {
                            const preview = document.createElement('div');
                            preview.className = 'w-1/2 sm:w-1/3 md:w-1/4 px-2 mb-4';
                            preview.innerHTML = `
                                <div class="border rounded overflow-hidden">
                                    <img src="${e.target.result}" alt="Preview" class="w-full h-32 object-cover">
                                </div>
                            `;
                            previewContainer.appendChild(preview);
                        }
                        reader.readAsDataURL(file);
                    }
                } else {
                    previewContainer.classList.add('hidden');
                }
            });
        }
    }
});