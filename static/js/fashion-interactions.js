// StyleAI Fashion Assistant Interactive Features

$(document).ready(function() {
    // Initialize all functionality
    initializeDragAndDrop();
    initializeVTONForms();
    initializeProductEffects();
    initializeSmoothScrolling();
    
    console.log('StyleAI Fashion Assistant loaded successfully!');
});

// Drag and Drop for Virtual Try-On
function initializeDragAndDrop() {
    $('.upload-area').on('dragover', function(e) {
        e.preventDefault();
        e.stopPropagation();
        $(this).addClass('dragover');
    });

    $('.upload-area').on('dragleave', function(e) {
        e.preventDefault();
        e.stopPropagation();
        $(this).removeClass('dragover');
    });

    $('.upload-area').on('drop', function(e) {
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

    // Handle click to open file dialog
    $('.upload-area').on('click', function(e) {
        e.preventDefault();
        e.stopPropagation();
        const fileInput = $(this).find('input[type="file"]')[0];
        if (fileInput) {
            fileInput.click();
        }
    });

    // Handle file selection
    $(document).on('change', 'input[type="file"]', function() {
        const uploadArea = $(this).closest('.upload-area');
        if (uploadArea.length > 0) {
            handleFileUpload(this, uploadArea);
        }
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
    `)
    .appendTo('head');