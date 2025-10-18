// Enhanced scripts for SmartFitStudios

// jquery ready start
$(document).ready(function() {
    // jQuery code

    /* ///////////////////////////////////////
    ENHANCED SCRIPTS FOR BETTER UX
    */ ///////////////////////////////////////
    
    // Prevent closing from click inside dropdown
    $(document).on('click', '.dropdown-menu', function (e) {
        e.stopPropagation();
    });

    // Radio button handling
    $('.js-check :radio').change(function () {
        var check_attr_name = $(this).attr('name');
        if ($(this).is(':checked')) {
            $('input[name='+ check_attr_name +']').closest('.js-check').removeClass('active');
            $(this).closest('.js-check').addClass('active');
        } else {
            item.removeClass('active');
        }
    });

    // Checkbox handling
    $('.js-check :checkbox').change(function () {
        var check_attr_name = $(this).attr('name');
        if ($(this).is(':checked')) {
            $(this).closest('.js-check').addClass('active');
        } else {
            $(this).closest('.js-check').removeClass('active');
        }
    });

    // Bootstrap tooltip
    if($('[data-toggle="tooltip"]').length>0) {
        $('[data-toggle="tooltip"]').tooltip()
    }

    // ==================== ENHANCED FEATURES ====================
    
    // Smooth scroll to top button
    var scrollTopBtn = $('<button class="scroll-to-top" title="Back to top"><i class="fa fa-arrow-up"></i></button>');
    $('body').append(scrollTopBtn);
    
    $(window).scroll(function() {
        if ($(this).scrollTop() > 300) {
            $('.scroll-to-top').addClass('show');
        } else {
            $('.scroll-to-top').removeClass('show');
        }
    });
    
    $('.scroll-to-top').click(function() {
        $('html, body').animate({scrollTop: 0}, 600);
        return false;
    });

    // Add to cart animation
    $('.btn:contains("Add to cart")').click(function(e) {
        var btn = $(this);
        if (!btn.hasClass('disabled')) {
            btn.html('<i class="fas fa-check"></i> Added!');
            setTimeout(function() {
                btn.html('<span class="text">Add to cart</span> <i class="fas fa-shopping-cart"></i>');
            }, 2000);
        }
    });

    // Image preview for file inputs
    $('input[type="file"]').change(function(e) {
        var file = e.target.files[0];
        if (file && file.type.startsWith('image/')) {
            var reader = new FileReader();
            var inputId = $(this).attr('id');
            
            reader.onload = function(e) {
                var previewId = inputId + '-preview';
                var preview = $('#' + previewId);
                
                if (preview.length === 0) {
                    preview = $('<img id="' + previewId + '" class="img-preview mt-2" style="max-width: 200px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">');
                    $(e.target).parent().append(preview);
                }
                
                preview.attr('src', e.target.result);
            };
            
            reader.readAsDataURL(file);
        }
    });

    // Search bar enhancement
    $('.search input[type="text"]').on('focus', function() {
        $(this).parent().addClass('search-focused');
    }).on('blur', function() {
        $(this).parent().removeClass('search-focused');
    });

    // Product card hover effect enhancement
    $('.card-product-grid').hover(
        function() {
            $(this).find('.btn').addClass('btn-hover-effect');
        },
        function() {
            $(this).find('.btn').removeClass('btn-hover-effect');
        }
    );

    // Quantity input validation
    $('.input-spinner input[type="text"]').on('input', function() {
        var value = parseInt($(this).val());
        if (isNaN(value) || value < 1) {
            $(this).val(1);
        }
    });

    // Category dropdown enhancement
    $('.category-wrap .dropdown-toggle').click(function() {
        $(this).toggleClass('active');
    });

    // Alert auto-dismiss
    if ($('.alert').length > 0) {
        setTimeout(function() {
            $('.alert').fadeOut('slow');
        }, 5000);
    }

    // Loading state for forms
    $('form').submit(function() {
        var submitBtn = $(this).find('button[type="submit"]');
        if (!submitBtn.hasClass('no-loading')) {
            submitBtn.prop('disabled', true);
            var originalText = submitBtn.html();
            submitBtn.data('original-text', originalText);
            submitBtn.html('<i class="fas fa-spinner fa-spin"></i> Processing...');
        }
    });

    // Price range filter enhancement
    $('.filter-group select').change(function() {
        $(this).addClass('filter-active');
    });

    // Wishlist functionality (placeholder)
    function addWishlistButton() {
        $('.card-product-grid .img-wrap').each(function() {
            if ($(this).find('.wishlist-btn').length === 0) {
                var wishlistBtn = $('<button class="wishlist-btn" title="Add to wishlist"><i class="far fa-heart"></i></button>');
                $(this).append(wishlistBtn);
            }
        });
    }
    
    addWishlistButton();
    
    $(document).on('click', '.wishlist-btn', function(e) {
        e.preventDefault();
        e.stopPropagation();
        $(this).toggleClass('active');
        var icon = $(this).find('i');
        if ($(this).hasClass('active')) {
            icon.removeClass('far').addClass('fas');
        } else {
            icon.removeClass('fas').addClass('far');
        }
    });

    // Product quick view (placeholder for future implementation)
    function addQuickViewButton() {
        $('.card-product-grid .img-wrap').each(function() {
            if ($(this).find('.quick-view-btn').length === 0) {
                var quickViewBtn = $('<button class="quick-view-btn" title="Quick view"><i class="fas fa-eye"></i></button>');
                $(this).append(quickViewBtn);
            }
        });
    }
    
    addQuickViewButton();

    // Notification system
    window.showNotification = function(message, type = 'success') {
        var notification = $('<div class="custom-notification ' + type + '">' + message + '</div>');
        $('body').append(notification);
        
        setTimeout(function() {
            notification.addClass('show');
        }, 100);
        
        setTimeout(function() {
            notification.removeClass('show');
            setTimeout(function() {
                notification.remove();
            }, 300);
        }, 3000);
    };

}); 
// jquery end



// Product detail page enhancements
$(document).ready(function() {
    // Wishlist button on product detail page
    $('.wishlist-btn-detail').click(function(e) {
        e.preventDefault();
        $(this).toggleClass('active');
        var icon = $(this).find('i');
        if ($(this).hasClass('active')) {
            icon.removeClass('far').addClass('fas');
            showNotification('Added to wishlist!', 'success');
        } else {
            icon.removeClass('fas').addClass('far');
            showNotification('Removed from wishlist', 'success');
        }
    });

    // Image zoom on product detail (simple version)
    $('.gallery-wrap .img-big-wrap img').hover(
        function() {
            $(this).css('transform', 'scale(1.2)');
        },
        function() {
            $(this).css('transform', 'scale(1)');
        }
    );

    // Quantity validation in cart
    $('.input-spinner input').on('change', function() {
        var value = parseInt($(this).val());
        if (isNaN(value) || value < 1) {
            $(this).val(1);
        }
    });

    // Promo code application
    $('.input-group button:contains("Apply")').click(function() {
        var promoCode = $(this).closest('.input-group').find('input').val();
        if (promoCode) {
            showNotification('Promo code applied successfully!', 'success');
        } else {
            showNotification('Please enter a promo code', 'error');
        }
    });

    // Add loading state to checkout button
    $('a:contains("Proceed to Checkout")').click(function(e) {
        var btn = $(this);
        btn.html('<i class="fas fa-spinner fa-spin mr-2"></i> Processing...');
    });
});


// ==================== REVIEWS SECTION ====================
$(document).ready(function() {
    
    // Star Rating Input
    $('.star-rating-input i').on('click', function() {
        var rating = $(this).data('rating');
        $('#ratingValue').val(rating);
        
        // Update star display
        $('.star-rating-input i').each(function(index) {
            if (index < rating) {
                $(this).removeClass('far').addClass('fas');
            } else {
                $(this).removeClass('fas').addClass('far');
            }
        });
    });
    
    // Star Rating Hover Effect
    $('.star-rating-input i').on('mouseenter', function() {
        var rating = $(this).data('rating');
        $('.star-rating-input i').each(function(index) {
            if (index < rating) {
                $(this).addClass('active');
            } else {
                $(this).removeClass('active');
            }
        });
    });
    
    $('.star-rating-input').on('mouseleave', function() {
        var currentRating = $('#ratingValue').val();
        $('.star-rating-input i').removeClass('active');
        if (currentRating) {
            $('.star-rating-input i').each(function(index) {
                if (index < currentRating) {
                    $(this).addClass('active');
                }
            });
        }
    });
    
    // Submit Review
    $('#submitReview').on('click', function() {
        var rating = $('#ratingValue').val();
        var title = $('#reviewTitle').val();
        var text = $('#reviewText').val();
        var name = $('#reviewerName').val();
        var email = $('#reviewerEmail').val();
        
        // Validation
        if (!rating) {
            showNotification('Please select a rating', 'error');
            return;
        }
        
        if (!title || !text || !name || !email) {
            showNotification('Please fill in all required fields', 'error');
            return;
        }
        
        if (text.length < 50) {
            showNotification('Review must be at least 50 characters', 'error');
            return;
        }
        
        // Show loading
        var btn = $(this);
        var originalText = btn.html();
        btn.html('<i class="fas fa-spinner fa-spin mr-2"></i> Submitting...').prop('disabled', true);
        
        // Simulate submission (replace with actual AJAX call)
        setTimeout(function() {
            showNotification('Thank you! Your review has been submitted successfully.', 'success');
            $('#reviewModal').modal('hide');
            $('#reviewForm')[0].reset();
            $('.star-rating-input i').removeClass('fas active').addClass('far');
            $('#ratingValue').val('');
            btn.html(originalText).prop('disabled', false);
        }, 1500);
    });
    
    // Helpful Button
    $('.helpful-btn').on('click', function() {
        var btn = $(this);
        if (!btn.hasClass('active')) {
            btn.addClass('active');
            var currentCount = parseInt(btn.text().match(/\d+/)[0]);
            btn.html('<i class="fas fa-thumbs-up"></i> Helpful (' + (currentCount + 1) + ')');
            showNotification('Thanks for your feedback!', 'success');
        } else {
            btn.removeClass('active');
            var currentCount = parseInt(btn.text().match(/\d+/)[0]);
            btn.html('<i class="far fa-thumbs-up"></i> Helpful (' + (currentCount - 1) + ')');
        }
    });
    
    // Review Filter Buttons
    $('button[data-filter]').on('click', function() {
        $('button[data-filter]').removeClass('active');
        $(this).addClass('active');
        
        var filter = $(this).data('filter');
        // Here you would filter the reviews based on the selected filter
        showNotification('Showing ' + filter + ' reviews', 'success');
    });
    
    // Review Sort
    $('#reviewSort').on('change', function() {
        var sortBy = $(this).val();
        // Here you would sort the reviews based on the selected option
        showNotification('Reviews sorted by ' + sortBy, 'success');
    });
    
    // Load More Reviews
    $('#loadMoreReviews').on('click', function() {
        var btn = $(this);
        var originalText = btn.html();
        btn.html('<i class="fas fa-spinner fa-spin mr-2"></i> Loading...').prop('disabled', true);
        
        // Simulate loading more reviews
        setTimeout(function() {
            btn.html(originalText).prop('disabled', false);
            showNotification('More reviews loaded', 'success');
        }, 1000);
    });
    
    // Custom File Input Label Update
    $('#reviewImages').on('change', function() {
        var fileCount = this.files.length;
        var label = $(this).next('.custom-file-label');
        if (fileCount > 0) {
            label.text(fileCount + ' image(s) selected');
        } else {
            label.text('Choose images...');
        }
    });
    
    // Review Image Click (Lightbox effect)
    $('.review-img').on('click', function() {
        var imgSrc = $(this).attr('src');
        // Create a simple lightbox
        var lightbox = $('<div class="review-lightbox"></div>');
        var img = $('<img src="' + imgSrc + '" class="lightbox-img">');
        var close = $('<button class="lightbox-close">&times;</button>');
        
        lightbox.append(close).append(img);
        $('body').append(lightbox);
        
        setTimeout(function() {
            lightbox.addClass('show');
        }, 10);
        
        // Close lightbox
        close.on('click', function() {
            lightbox.removeClass('show');
            setTimeout(function() {
                lightbox.remove();
            }, 300);
        });
        
        lightbox.on('click', function(e) {
            if (e.target === this) {
                lightbox.removeClass('show');
                setTimeout(function() {
                    lightbox.remove();
                }, 300);
            }
        });
    });
    
    // Character counter for review text
    $('#reviewText').on('input', function() {
        var length = $(this).val().length;
        var minLength = 50;
        var remaining = minLength - length;
        
        var counter = $(this).next('.form-text');
        if (length < minLength) {
            counter.text('Minimum 50 characters (' + remaining + ' more needed)');
            counter.removeClass('text-success').addClass('text-muted');
        } else {
            counter.text('Great! Your review is detailed enough.');
            counter.removeClass('text-muted').addClass('text-success');
        }
    });
    
    // Reset modal on close
    $('#reviewModal').on('hidden.bs.modal', function() {
        $('#reviewForm')[0].reset();
        $('.star-rating-input i').removeClass('fas active').addClass('far');
        $('#ratingValue').val('');
        $('.custom-file-label').text('Choose images...');
    });
});


// ==================== VIRTUAL TRY-ON SECTION ====================
$(document).ready(function() {
    
    // Image-based VTON Form Submission
    $('#image-vton-form').on('submit', function(e) {
        e.preventDefault();
        
        var personImage = $('#person-image')[0].files[0];
        var clothImage = $('#cloth-image')[0].files[0];
        
        // Validation
        if (!personImage || !clothImage) {
            showNotification('Please select both person and cloth images', 'error');
            return;
        }
        
        // Validate file sizes (max 10MB each)
        var maxSize = 10 * 1024 * 1024; // 10MB
        if (personImage.size > maxSize) {
            showNotification('Person image is too large. Max size: 10MB', 'error');
            return;
        }
        if (clothImage.size > maxSize) {
            showNotification('Cloth image is too large. Max size: 10MB', 'error');
            return;
        }
        
        // Create FormData
        var formData = new FormData();
        formData.append('person_image', personImage);
        formData.append('cloth_image', clothImage);
        
        // Show loading state
        var submitBtn = $(this).find('button[type="submit"]');
        var originalText = 'Generate Try-On (Image)';
        submitBtn.html('<i class="fas fa-spinner fa-spin mr-2"></i> Generating...').prop('disabled', true);
        
        // Hide previous result
        $('#image-vton-result').hide();
        
        // Send AJAX request
        $.ajax({
            url: '/vton/generate_vton/',
            type: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            timeout: 60000, // 60 second timeout
            success: function(response) {
                // Restore button first
                submitBtn.html(originalText).prop('disabled', false);
                
                if (response.success && response.image_data) {
                    // Display the generated image
                    $('#image-vton-output').attr('src', 'data:image/jpeg;base64,' + response.image_data);
                    $('#image-vton-result').fadeIn();
                    showNotification('Virtual try-on generated successfully!', 'success');
                    
                    // Scroll to result
                    $('html, body').animate({
                        scrollTop: $('#image-vton-result').offset().top - 100
                    }, 500);
                } else {
                    showNotification('Failed to generate try-on: ' + (response.error || 'Unknown error'), 'error');
                }
            },
            error: function(xhr, status, error) {
                // Restore button
                submitBtn.html(originalText).prop('disabled', false);
                
                var errorMessage = 'Failed to generate try-on';
                if (xhr.responseJSON && xhr.responseJSON.error) {
                    errorMessage = xhr.responseJSON.error;
                } else if (status === 'timeout') {
                    errorMessage = 'Request timed out. Please try again with smaller images.';
                }
                showNotification(errorMessage, 'error');
                console.error('VTON Error:', xhr.responseText);
            }
        });
    });
    
    // Download VTON Image
    $('#download-vton-btn').on('click', function() {
        var imgSrc = $('#image-vton-output').attr('src');
        if (imgSrc) {
            var link = document.createElement('a');
            link.href = imgSrc;
            link.download = 'virtual-tryon-' + Date.now() + '.jpg';
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
            showNotification('Image downloaded successfully!', 'success');
        }
    });
    
    // Video-based VTON Form Submission
    $('#video-vton-form').on('submit', function(e) {
        e.preventDefault();
        
        var personImage = $('#video-person-image')[0].files[0];
        
        // Validation
        if (!personImage) {
            showNotification('Please select a person image', 'error');
            return;
        }
        
        // Validate file size (max 10MB)
        var maxSize = 10 * 1024 * 1024; // 10MB
        if (personImage.size > maxSize) {
            showNotification('Image is too large. Max size: 10MB', 'error');
            return;
        }
        
        // Get the product image from the page
        var productImageUrl = $('.gallery-wrap .img-big-wrap img').attr('src');
        
        // Create FormData
        var formData = new FormData();
        formData.append('person_image', personImage);
        formData.append('prompt', 'Create a video showing the person wearing this clothing item');
        
        // If we can get the product image, add it
        // Note: This requires the product image to be accessible
        // For now, we'll just send the person image
        
        // Show loading state
        var submitBtn = $(this).find('button[type="submit"]');
        var originalText = submitBtn.html();
        submitBtn.html('<i class="fas fa-spinner fa-spin mr-2"></i> Generating video... (this may take several minutes)').prop('disabled', true);
        
        // Hide previous result
        $('#video-vton-result').hide();
        
        // Send AJAX request
        $.ajax({
            url: '/vton/generate_video_vton/',
            type: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            timeout: 300000, // 5 minute timeout for video generation
            success: function(response) {
                if (response.success) {
                    showNotification('Video generation started! Check your n8n workflow for the result.', 'success');
                    // Note: Video generation is async, so we can't display it immediately
                    // You would need to implement a polling mechanism or webhook to get the result
                } else {
                    showNotification('Failed to generate video: ' + (response.error || 'Unknown error'), 'error');
                }
            },
            error: function(xhr, status, error) {
                var errorMessage = 'Failed to generate video';
                if (xhr.responseJSON && xhr.responseJSON.error) {
                    errorMessage = xhr.responseJSON.error;
                } else if (status === 'timeout') {
                    errorMessage = 'Request timed out. Video generation may still be processing in the background.';
                }
                showNotification(errorMessage, 'error');
                console.error('Video VTON Error:', xhr.responseText);
            },
            complete: function() {
                // Restore button
                submitBtn.html(originalText).prop('disabled', false);
            }
        });
    });
    
    // Image preview for VTON uploads
    $('#person-image, #cloth-image, #video-person-image').on('change', function() {
        var file = this.files[0];
        if (file && file.type.startsWith('image/')) {
            var reader = new FileReader();
            var inputId = $(this).attr('id');
            
            reader.onload = function(e) {
                var previewId = inputId + '-preview';
                var preview = $('#' + previewId);
                
                if (preview.length === 0) {
                    preview = $('<div class="mt-2"><img id="' + previewId + '" class="img-thumbnail" style="max-width: 200px;"><p class="text-muted small mt-1">Preview</p></div>');
                    $('#' + inputId).parent().append(preview);
                }
                
                $('#' + previewId).attr('src', e.target.result);
            };
            
            reader.readAsDataURL(file);
        }
    });
});
