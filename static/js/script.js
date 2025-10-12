// Enhanced scripts for GreatKart

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
