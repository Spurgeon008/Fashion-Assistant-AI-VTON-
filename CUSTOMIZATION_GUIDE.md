# Customization Guide

## 🎨 Easy Customization

This guide shows you how to customize the look and feel of your SmartFitStudios website without breaking anything.

## 🌈 Color Customization

### Primary Colors
Edit these in `static/css/custom.css` at the top:

```css
:root {
    /* Main brand color - used for buttons, links, highlights */
    --primary-color: #3b82f6;
    --primary-hover: #2563eb;
    
    /* Success/positive actions - used for "in stock", success messages */
    --secondary-color: #10b981;
    
    /* Danger/negative actions - used for delete, out of stock */
    --danger-color: #ef4444;
    
    /* Warnings - used for low stock, alerts */
    --warning-color: #f59e0b;
    
    /* Dark text and backgrounds */
    --dark-color: #1f2937;
    
    /* Light backgrounds */
    --light-bg: #f9fafb;
    
    /* Borders */
    --border-color: #e5e7eb;
    
    /* Muted text */
    --text-muted: #6b7280;
}
```

### Popular Color Schemes

#### 1. **Purple Theme** (Elegant)
```css
--primary-color: #8b5cf6;
--primary-hover: #7c3aed;
```

#### 2. **Green Theme** (Eco-friendly)
```css
--primary-color: #10b981;
--primary-hover: #059669;
```

#### 3. **Orange Theme** (Energetic)
```css
--primary-color: #f97316;
--primary-hover: #ea580c;
```

#### 4. **Pink Theme** (Fashion)
```css
--primary-color: #ec4899;
--primary-hover: #db2777;
```

#### 5. **Teal Theme** (Modern)
```css
--primary-color: #14b8a6;
--primary-hover: #0d9488;
```

## 🖼️ Logo & Branding

### Change Logo
Replace the file at: `static/images/logo.png`

Recommended size: 200x50 pixels (or similar aspect ratio)

### Change Favicon
Replace the file at: `static/images/favicon.ico`

Recommended size: 32x32 pixels

### Change Banner
Replace the file at: `static/images/banners/1.jpg`

Recommended size: 1920x600 pixels

## 📝 Text Customization

### Site Name
Edit in `templates/base.html`:
```html
<title>SmartFitStudios | One of the Biggest Online Shopping Platform</title>
```

### Footer Copyright
Edit in `templates/includes/footer.html`:
```html
<p class="text-muted mb-0">
    <i class="far fa-copyright"></i> 2024 SmartFitStudios. All rights reserved.
</p>
```

### Contact Information
Edit in `templates/includes/navbar.html`:
```html
<a href="mailto:support@SmartFitStudios.com" class="nav-link">
    <i class="fas fa-envelope mr-1"></i> support@SmartFitStudios.com
</a>
<a href="tel:+1234567890" class="nav-link">
    <i class="fas fa-phone mr-1"></i> +1 (234) 567-890
</a>
```

## 🎭 Typography

### Change Font
Edit in `static/css/custom.css`:

```css
body {
    font-family: 'Your Font', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}
```

Popular free fonts:
- **Inter** (current) - Modern, clean
- **Poppins** - Friendly, rounded
- **Roboto** - Professional, neutral
- **Montserrat** - Bold, impactful
- **Open Sans** - Classic, readable

To use a Google Font, add to `templates/base.html`:
```html
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet">
```

### Font Sizes
```css
/* Headings */
h1 { font-size: 2.5rem; }
h2 { font-size: 2rem; }
h3 { font-size: 1.75rem; }
h4 { font-size: 1.5rem; }
h5 { font-size: 1.25rem; }

/* Body */
body { font-size: 15px; }
```

## 🎨 Button Styles

### Rounded Buttons
```css
.btn {
    border-radius: 50px; /* Change from 8px to 50px for pill shape */
}
```

### Button Sizes
```css
.btn {
    padding: 0.625rem 1.5rem; /* Adjust padding */
    font-size: 1rem; /* Adjust font size */
}
```

## 📦 Card Styles

### Card Border Radius
```css
.card {
    border-radius: 12px; /* Change from 12px to your preference */
}
```

### Card Shadow
```css
.card {
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); /* Adjust shadow */
}
```

## 🎯 Spacing

### Global Spacing
```css
:root {
    --spacing-sm: 0.5rem;
    --spacing-md: 1rem;
    --spacing-lg: 2rem;
    --spacing-xl: 4rem;
}
```

## 🌟 Animation Speed

### Transition Duration
```css
:root {
    --transition: all 0.3s ease; /* Change 0.3s to your preference */
}
```

Faster: `0.15s`
Slower: `0.5s`
No animation: `0s`

## 🎨 Gradient Backgrounds

### Hero Section Gradient
Edit in `static/css/custom.css`:

```css
.section-intro {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}
```

Popular gradients:
```css
/* Sunset */
background: linear-gradient(135deg, #ff6b6b 0%, #feca57 100%);

/* Ocean */
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);

/* Forest */
background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);

/* Fire */
background: linear-gradient(135deg, #ee0979 0%, #ff6a00 100%);
```

## 📱 Responsive Breakpoints

```css
/* Mobile */
@media (max-width: 768px) {
    /* Your mobile styles */
}

/* Tablet */
@media (max-width: 991px) {
    /* Your tablet styles */
}

/* Desktop */
@media (min-width: 1200px) {
    /* Your desktop styles */
}
```

## 🎭 Feature Toggles

### Disable Scroll-to-Top Button
In `static/js/script.js`, comment out:
```javascript
// var scrollTopBtn = $('<button class="scroll-to-top"...
```

### Disable Wishlist Feature
In `static/js/script.js`, comment out:
```javascript
// addWishlistButton();
```

### Disable Animations
```css
* {
    transition: none !important;
    animation: none !important;
}
```

## 🎨 Social Media Links

Edit in `templates/includes/footer.html`:

```html
<a href="https://facebook.com/yourpage" class="btn btn-sm btn-outline-light mr-2">
    <i class="fab fa-facebook-f"></i>
</a>
<a href="https://twitter.com/yourhandle" class="btn btn-sm btn-outline-light mr-2">
    <i class="fab fa-twitter"></i>
</a>
<a href="https://instagram.com/yourhandle" class="btn btn-sm btn-outline-light mr-2">
    <i class="fab fa-instagram"></i>
</a>
```

## 📊 Product Card Layout

### Change Products Per Row

In `templates/store/store.html` and `templates/home.html`:

```html
<!-- 3 per row -->
<div class="col-lg-4 col-md-6 col-sm-6 mb-4">

<!-- 4 per row -->
<div class="col-lg-3 col-md-4 col-sm-6 mb-4">

<!-- 2 per row -->
<div class="col-lg-6 col-md-6 col-sm-12 mb-4">
```

## 🎯 Quick Customization Checklist

- [ ] Change primary color
- [ ] Update logo
- [ ] Update favicon
- [ ] Change site name/title
- [ ] Update contact information
- [ ] Update footer copyright
- [ ] Add social media links
- [ ] Change hero banner image
- [ ] Customize font (optional)
- [ ] Adjust button styles (optional)
- [ ] Modify gradient colors (optional)

## 💡 Pro Tips

1. **Test changes locally** before deploying
2. **Keep backups** of original files
3. **Use browser DevTools** to test CSS changes live
4. **Clear cache** after making changes
5. **Test on mobile** after customization
6. **Use consistent colors** throughout
7. **Don't change too many things at once**

## 🚫 What NOT to Change

To keep everything working:
- Don't modify class names
- Don't remove required HTML elements
- Don't change JavaScript function names
- Don't modify VTON-related code
- Don't change Django template tags ({% %})

## 📚 Resources

### Color Palettes
- [Coolors.co](https://coolors.co) - Color scheme generator
- [Adobe Color](https://color.adobe.com) - Color wheel tool

### Fonts
- [Google Fonts](https://fonts.google.com) - Free fonts
- [Font Pair](https://fontpair.co) - Font combinations

### Gradients
- [UI Gradients](https://uigradients.com) - Beautiful gradients
- [Gradient Hunt](https://gradienthunt.com) - Gradient collection

### Icons
- [Font Awesome](https://fontawesome.com) - Icon library (already included)
- [Heroicons](https://heroicons.com) - Additional icons

## 🆘 Need Help?

If something breaks:
1. Check browser console for errors
2. Clear browser cache
3. Revert to backup files
4. Check this guide for correct syntax
5. Ask for help!

---

**Happy Customizing! 🎨**
