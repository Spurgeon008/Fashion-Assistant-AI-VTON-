// StyleAI Fashion Assistant Interactive Features

$(document).ready(function() {
    console.log('StyleAI Fashion Assistant loading...');
    
    // Wait for DOM to be fully loaded
    setTimeout(function() {
        initializeDragAndDrop();
        initializeVTONForms();
        initializeProductEffects();
        initializeSmoothScrolling();
        initializeProductVTON();
        
        console.log('StyleAI Fashion Assistant loaded successfully!');
        console.log('Upload areas found:', $('.upload-area').length);
        console.log('File inputs found:', $('input[type="file"]').length);
        
        // Debug: Log each file input
        $('input[type="file"]').each(function(index) {
            console.log('File input ' + index + ':', this.id, 'visible:', $(this).is(':visible'));
        });
    }, 500);
});

// Enhanced Drag and Drop for Virtual Try-On
function initializeDragAndDrop() {
    console.log('Initializing drag and drop...');
    
    // Remove any existing event handlers
    $('.upload-area').off('click dragover dragleave drop');
    $('input[type="file"]').off('change');
    
    // Drag and drop events
    $(document).on('dragover', '.upload-area', function(e) {
        e.preventDefault();
        e.stopPropagation();
        $(this).addClass('dragover');
    });

    $(document).on('dragleave', '.upload-area', function(e) {
        e.preventDefault();
        e.stopPropagation();
        $(this).removeClass('dragover');
    });

    $(document).on('drop', '.upload-area', function(e) {
        e.preventDefault();
        e.stopPropagation();
        $(this).removeClass('dragover');
        
        const files = e.originalEvent.dataTransfer.files;
        if (files.length > 0) {
            const fileInput = $(this).find('input[type="file"]')[0];
            if (fileInput) {
                fileInput.files = files;
                handleFileUpload(fileInput, $(this));
            }
        }
    });

    // Click to open file dialog - Simplified approach
    $(document).on('click', '.upload-area', function(e) {
        // Only trigger if the click wasn't on the file input itself
        if (e.target.type !== 'file') {
            e.preventDefault();
            e.stopPropagation();
            console.log('Upload area clicked');
            
            const fileInput = $(this).find('input[type="file"]')[0];
            if (fileInput) {
                console.log('File input found, triggering click');
                fileInput.click();
            } else {
                console.log('No file input found in upload area');
            }
        }
    });

    // Handle file selection
    $(document).on('change', 'input[type="file"]', function() {
        console.log('File selected:', this.files[0]?.name);
        const uploadArea = $(this).closest('.upload-area');
        if (uploadArea.length > 0) {
            handleFileUpload(this, uploadArea);
        }
    });
    
    // Prevent file input clicks from bubbling
    $(document).on('click', 'input[type="file"]', function(e) {
        e.stopPropagation();
    });
}

function handleFileUpload(input, uploadArea) {
    if (input.files && input.files[0]) {
        const file = input.files[0];
        const reader = new FileReader();
        
        reader.onload = function(e) {
            const preview = `
                <div class="upload-preview">
                    <img src="${e.target.result}" alt="Preview" style="max-width: 100%; max-height: 150px; border-radius: 8px; margin-bottom: 10px;">
                    <p style="color: var(--text-primary); margin: 10px 0; font-size: 0.9rem;"><strong>${file.name}</strong></p>
                    <button type="button" class="btn btn-sm btn-outline-danger remove-file">
                        <i class="fas fa-times"></i> Remove
                    </button>
                </div>
            `;
            uploadArea.html(preview);
        };
        
        reader.readAsDataURL(file);
    }
}

// Remove uploaded file
$(document).on('click', '.remove-file', function() {
    const uploadArea = $(this).closest('.upload-area');
    const originalContent = `
        <div class="upload-icon">
            <i class="fas fa-cloud-upload-alt"></i>
        </div>
        <h6>Upload your photo</h6>
        <p>Drop image here or click to browse</p>
        <input type="file" class="file-input" accept="image/*">
    `;
    uploadArea.html(originalContent);
});

// VTON Form Enhancement
function initializeVTONForms() {
    // Image VTON Form
    $('#image-vton-form').on('submit', function(e) {
        e.preventDefault();
        
        const formData = new FormData();
        const personImage = $('#person-image')[0].files[0];
        const clothImage = $('#cloth-image')[0].files[0];
        
        if (!personImage || !clothImage) {
            showNotification('Please select both person and cloth images.', 'warning');
            return;
        }
        
        formData.append('person_image', personImage);
        formData.append('cloth_image', clothImage);
        
        const submitButton = $(this).find('button[type="submit"]');
        const originalText = submitButton.html();
        submitButton.html('<i class="fas fa-spinner fa-spin"></i> Processing...').prop('disabled', true);
        
        $.ajax({
            url: '/vton/generate_vton/',
            type: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            timeout: 60000,
            success: function(response) {
                if (response.success) {
                    if (response.image_data) {
                        $('#image-vton-result').show().addClass('fade-in');
                        $('#image-vton-output').attr('src', 'data:image/jpeg;base64,' + response.image_data);
                        showNotification('Virtual try-on completed successfully!', 'success');
                    } else {
                        showNotification('Try-on completed but no image returned.', 'info');
                    }
                } else {
                    showNotification('Error: ' + (response.error || 'Unknown error occurred'), 'error');
                }
            },
            error: function(xhr, status, error) {
                let errorMessage = 'Error generating virtual try-on: ';
                if (xhr.responseJSON && xhr.responseJSON.error) {
                    errorMessage += xhr.responseJSON.error;
                } else {
                    errorMessage += error || 'Unknown error occurred';
                }
                showNotification(errorMessage, 'error');
            },
            complete: function() {
                submitButton.html(originalText).prop('disabled', false);
            }
        });
    });

    // Video VTON Form
    $('#video-vton-form').on('submit', function(e) {
        e.preventDefault();
        
        const formData = new FormData();
        const personImage = $('#video-person-image')[0].files[0];
        
        if (!personImage) {
            showNotification('Please select a person image.', 'warning');
            return;
        }
        
        formData.append('person_image', personImage);
        
        const submitButton = $(this).find('button[type="submit"]');
        const originalText = submitButton.html();
        submitButton.html('<i class="fas fa-spinner fa-spin"></i> Generating Video...').prop('disabled', true);
        
        $.ajax({
            url: '/vton/generate_video_vton/',
            type: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            timeout: 120000,
            success: function(response) {
                if (response.success) {
                    if (response.video_data) {
                        $('#video-vton-result').show().addClass('fade-in');
                        $('#video-vton-output').attr('src', 'data:video/mp4;base64,' + response.video_data);
                        showNotification('Video generation completed successfully!', 'success');
                    } else {
                        showNotification('Video completed but no data returned.', 'info');
                    }
                } else {
                    showNotification('Error: ' + (response.error || 'Unknown error occurred'), 'error');
                }
            },
            error: function(xhr, status, error) {
                let errorMessage = 'Error generating video: ';
                if (xhr.responseJSON && xhr.responseJSON.error) {
                    errorMessage += xhr.responseJSON.error;
                } else {
                    errorMessage += error || 'Unknown error occurred';
                }
                showNotification(errorMessage, 'error');
            },
            complete: function() {
                submitButton.html(originalText).prop('disabled', false);
            }
        });
    });
}

// Product hover effects
function initializeProductEffects() {
    $('.product-card').hover(
        function() {
            $(this).find('.product-overlay').fadeIn(300);
        },
        function() {
            $(this).find('.product-overlay').fadeOut(300);
        }
    );

    // Try-on button click
    $('.btn-try-on').on('click', function(e) {
        e.preventDefault();
        e.stopPropagation();
        
        // Scroll to VTON section
        $('html, body').animate({
            scrollTop: $('#vton-section').offset().top - 100
        }, 800);
        
        showNotification('Scroll up to use Virtual Try-On with your own images!', 'info');
    });
}

// Smooth scrolling for navigation
function initializeSmoothScrolling() {
    $('a[href^="#"]').on('click', function(e) {
        e.preventDefault();
        
        const target = $(this.getAttribute('href'));
        if (target.length) {
            $('html, body').animate({
                scrollTop: target.offset().top - 80
            }, 800);
        }
    });
}

// Notification system
function showNotification(message, type = 'info') {
    const alertClass = {
        'success': 'alert-success',
        'error': 'alert-danger',
        'warning': 'alert-warning',
        'info': 'alert-info'
    }[type] || 'alert-info';

    const notification = `
        <div class="alert ${alertClass} alert-dismissible fade show notification-toast" role="alert" 
             style="position: fixed; top: 20px; right: 20px; z-index: 9999; min-width: 300px; max-width: 400px;">
            ${message}
            <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                <span aria-hidden="true">&times;</span>
            </button>
        </div>
    `;
    
    $('body').append(notification);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        $('.notification-toast').alert('close');
    }, 5000);
}

// Product page VTON functionality
function initializeProductVTON() {
    // Product Image VTON Form
    $('#product-image-vton-form').on('submit', function(e) {
        e.preventDefault();
        
        const formData = new FormData();
        const personImage = $('#person-image-product')[0].files[0];
        const productImageUrl = $('#product-image-url').val();
        
        if (!personImage) {
            showNotification('Please select your photo.', 'warning');
            return;
        }
        
        formData.append('person_image', personImage);
        // For product page, we'll use the product image URL
        formData.append('cloth_image_url', productImageUrl);
        
        const submitButton = $(this).find('button[type="submit"]');
        const originalText = submitButton.html();
        submitButton.html('<i class="fas fa-spinner fa-spin"></i> Processing...').prop('disabled', true);
        
        $.ajax({
            url: '/vton/generate_vton/',
            type: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            timeout: 60000,
            success: function(response) {
                if (response.success) {
                    if (response.image_data) {
                        $('#product-image-vton-result').show().addClass('fade-in');
                        $('#product-image-vton-output').attr('src', 'data:image/jpeg;base64,' + response.image_data);
                        showNotification('Virtual try-on completed successfully!', 'success');
                    } else {
                        showNotification('Try-on completed but no image returned.', 'info');
                    }
                } else {
                    showNotification('Error: ' + (response.error || 'Unknown error occurred'), 'error');
                }
            },
            error: function(xhr, status, error) {
                let errorMessage = 'Error generating virtual try-on: ';
                if (xhr.responseJSON && xhr.responseJSON.error) {
                    errorMessage += xhr.responseJSON.error;
                } else {
                    errorMessage += error || 'Unknown error occurred';
                }
                showNotification(errorMessage, 'error');
            },
            complete: function() {
                submitButton.html(originalText).prop('disabled', false);
            }
        });
    });

    // Product Video VTON Form
    $('#product-video-vton-form').on('submit', function(e) {
        e.preventDefault();
        
        const formData = new FormData();
        const personImage = $('#video-person-image-product')[0].files[0];
        
        if (!personImage) {
            showNotification('Please select your photo.', 'warning');
            return;
        }
        
        formData.append('person_image', personImage);
        
        const submitButton = $(this).find('button[type="submit"]');
        const originalText = submitButton.html();
        submitButton.html('<i class="fas fa-spinner fa-spin"></i> Generating Video...').prop('disabled', true);
        
        $.ajax({
            url: '/vton/generate_video_vton/',
            type: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            timeout: 120000,
            success: function(response) {
                if (response.success) {
                    if (response.video_data) {
                        $('#product-video-vton-result').show().addClass('fade-in');
                        $('#product-video-vton-output').attr('src', 'data:video/mp4;base64,' + response.video_data);
                        showNotification('Video generation completed successfully!', 'success');
                    } else {
                        showNotification('Video completed but no data returned.', 'info');
                    }
                } else {
                    showNotification('Error: ' + (response.error || 'Unknown error occurred'), 'error');
                }
            },
            error: function(xhr, status, error) {
                let errorMessage = 'Error generating video: ';
                if (xhr.responseJSON && xhr.responseJSON.error) {
                    errorMessage += xhr.responseJSON.error;
                } else {
                    errorMessage += error || 'Unknown error occurred';
                }
                showNotification(errorMessage, 'error');
            },
            complete: function() {
                submitButton.html(originalText).prop('disabled', false);
            }
        });
    });
}

// Scroll to VTON section function
function scrollToVTON() {
    $('html, body').animate({
        scrollTop: $('#vton-section').offset().top - 100
    }, 800);
}

// Product page utility functions
function downloadProductImage() {
    const imgSrc = $('#product-image-vton-output').attr('src');
    if (imgSrc) {
        const link = document.createElement('a');
        link.href = imgSrc;
        link.download = 'virtual-try-on-result.jpg';
        link.click();
    }
}

function shareProductResult() {
    if (navigator.share) {
        navigator.share({
            title: 'My Virtual Try-On Result',
            text: 'Check out how this looks on me!',
            url: window.location.href
        });
    } else {
        // Fallback - copy URL to clipboard
        navigator.clipboard.writeText(window.location.href);
        showNotification('Link copied to clipboard!', 'success');
    }
}

function addToCartAfterTryOn() {
    // Find the add to cart form and submit it
    const addToCartForm = $('form[action*="add_cart"]');
    if (addToCartForm.length > 0) {
        addToCartForm.submit();
    } else {
        showNotification('Add to cart functionality not available', 'warning');
    }
}

function downloadProductVideo() {
    const videoSrc = $('#product-video-vton-output').attr('src');
    if (videoSrc) {
        const link = document.createElement('a');
        link.href = videoSrc;
        link.download = 'virtual-try-on-video.mp4';
        link.click();
    }
}

function shareProductVideo() {
    if (navigator.share) {
        navigator.share({
            title: 'My Fashion Video',
            text: 'Check out my virtual try-on video!',
            url: window.location.href
        });
    } else {
        navigator.clipboard.writeText(window.location.href);
        showNotification('Link copied to clipboard!', 'success');
    }
}

// Add fade-in animation class
$('<style>')
    .prop('type', 'text/css')
    .html(`
        .fade-in {
            animation: fadeIn 0.5s ease-in;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .upload-preview {
            text-align: center;
            padding: 20px;
            color: var(--text-primary);
        }
        
        .remove-file {
            background: #dc3545;
            border: 1px solid #dc3545;
            color: white;
            padding: 5px 10px;
            border-radius: 4px;
            font-size: 12px;
            cursor: pointer;
        }
        
        .remove-file:hover {
            background: #c82333;
            border-color: #bd2130;
            color: white;
        }
        
        .file-input {
            position: absolute !important;
            opacity: 0 !important;
            width: 100% !important;
            height: 100% !important;
            cursor: pointer !important;
            z-index: 1 !important;
        }
        
        .upload-area {
            position: relative !important;
            cursor: pointer !important;
        }
        
        .upload-area:hover {
            background-color: rgba(255, 255, 255, 0.05) !important;
        }
        
        .dragover {
            background-color: rgba(74, 144, 226, 0.1) !important;
            border-color: var(--accent-color) !important;
        }
    `)
    .appendTo('head');
// S
imple test function to verify file inputs work
function testFileInputs() {
    console.log('Testing file inputs...');
    $('input[type="file"]').each(function() {
        console.log('Testing input:', this.id);
        $(this).on('click', function() {
            console.log('File input clicked:', this.id);
        });
    });
}

// Add test button for debugging (remove in production)
$(document).ready(function() {
    setTimeout(function() {
        testFileInputs();
        
        // Add a test button for debugging
        if ($('#debug-test').length === 0) {
            $('body').append('<button id="debug-test" style="position: fixed; top: 10px; right: 10px; z-index: 9999; background: red; color: white; padding: 10px;">Test File Inputs</button>');
            $('#debug-test').on('click', function() {
                console.log('Manual test - triggering first file input');
                const firstInput = $('input[type="file"]').first();
                if (firstInput.length > 0) {
                    firstInput[0].click();
                } else {
                    console.log('No file inputs found');
                }
            });
        }
    }, 1000);
});