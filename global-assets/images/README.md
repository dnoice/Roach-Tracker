# Global Assets - Images Documentation

**File**: `README.md`
**Path**: `global-assets/images/README.md`
**Directory**: `global-assets/images/`
**Purpose**: Global brand images and assets used across the project
**Author**: dnoice + Claude AI
**Version**: 1.2.0
**Created**: 2025-10-31
**Updated**: 2025-11-01

---

## Overview

The `global-assets/images/` directory contains brand images, logos, banners, and other visual assets that are used globally across the Roach Tracker project. Unlike user-uploaded photos (stored in `static/uploads/`), these assets are part of the application's branding and documentation infrastructure.

---

## Directory Structure

```
global-assets/
└── images/
    ├── roach-tracker-banner.png    # GitHub repository banner/hero image
    └── README.md                    # This file
```

---

## Assets Inventory

### `roach-tracker-banner.png`

**Purpose**: Main banner image for GitHub repository and project documentation
**Dimensions**: 1280×640 pixels (2:1 aspect ratio)
**File Size**: ~2.1 MB (2,126,911 bytes)
**Format**: PNG (Portable Network Graphics)
**Color Mode**: RGB with transparency (alpha channel)
**Usage**: GitHub README header, documentation covers, promotional materials

#### Visual Description

The banner features the "Roach Tracker" branding and serves as the visual identity for the project. This image is prominently displayed at the top of the main README.md file to provide immediate visual context for repository visitors.

#### Technical Specifications

```
Filename: roach-tracker-banner.png
Dimensions: 1280 × 640 pixels
Aspect Ratio: 2:1 (standard GitHub social preview ratio)
File Size: 2,126,911 bytes (~2.1 MB)
Format: PNG
Bit Depth: 24-bit RGB or 32-bit RGBA
Compression: PNG lossless compression
Created: 2025-10-31
```

#### Usage in Project

**Main README.md**:
```markdown
![Roach Tracker Banner](https://github.com/dnoice/Roach-Tracker/blob/main/global-assets/images/roach-tracker-banner.png)
```

**Rendered URL**:
```
https://github.com/dnoice/Roach-Tracker/blob/main/global-assets/images/roach-tracker-banner.png
```

**Alternative Local Usage** (if serving locally):
```html
<img src="/global-assets/images/roach-tracker-banner.png" alt="Roach Tracker Banner">
```

#### Design Guidelines

**Recommended Specifications for Banner Images**:
- **Aspect Ratio**: 2:1 (width:height) - Standard GitHub social preview
- **Minimum Dimensions**: 1280×640 px
- **Maximum Dimensions**: 1920×960 px (for high-DPI displays)
- **File Format**: PNG (for transparency) or JPG (for smaller file size)
- **File Size**: < 5MB (GitHub limit is 25MB, but smaller is better for load times)
- **Color Space**: sRGB (standard web color space)
- **Accessibility**: Include descriptive alt text in markdown

**Safe Zones** (areas to avoid placing important content):
- **Top/Bottom**: 40px margin from edges (GitHub crops on mobile)
- **Left/Right**: 60px margin from edges
- **Center**: Primary branding and text should be centered

---

## Adding New Global Assets

### Process for Adding Images

**Step 1**: Create/obtain image file
- Follow design guidelines (dimensions, format, file size)
- Optimize image for web delivery
- Name file descriptively (lowercase, hyphens for spaces)

**Step 2**: Place in `global-assets/images/` directory
```bash
cp /path/to/new-image.png global-assets/images/
```

**Step 3**: Optimize file size (optional but recommended)
```bash
# Using ImageMagick
convert roach-tracker-logo.png -strip -quality 85 roach-tracker-logo-optimized.png

# Using pngquant (lossless PNG compression)
pngquant --quality=85-95 roach-tracker-logo.png -o roach-tracker-logo.png
```

**Step 4**: Add to git and commit
```bash
git add global-assets/images/new-image.png
git commit -m "Add new global asset: new-image.png"
```

**Step 5**: Reference in documentation
```markdown
![Description](global-assets/images/new-image.png)
```

### Naming Conventions

**Format**: `project-element-descriptor.ext`

**Good Examples**:
- `roach-tracker-banner.png` ✓
- `roach-tracker-logo-square.png` ✓
- `roach-tracker-icon-512.png` ✓
- `feature-screenshot-dashboard.png` ✓

**Bad Examples**:
- `banner.png` ✗ (too generic)
- `RTbanner_FINAL_v3.PNG` ✗ (not descriptive, version numbers)
- `My Banner Image.png` ✗ (spaces, capitalization)
- `Screenshot 2025-10-31 at 2.30 PM.png` ✗ (auto-generated, not descriptive)

---

## Asset Types and Use Cases

### Banner Images

**Purpose**: Repository headers, social media previews
**Recommended Dimensions**: 1280×640 px (2:1 ratio)
**Format**: PNG or JPG
**Examples**:
- `roach-tracker-banner.png` - Main repository banner

**GitHub Social Preview**:
GitHub automatically uses the first image in README.md as the social preview when shared on Twitter, Facebook, etc. Ensure your banner looks good at small sizes.

### Logos

**Purpose**: Branding, favicons, app icons
**Recommended Dimensions**:
- Square: 512×512 px, 256×256 px, 128×128 px
- Rectangular: 300×100 px (3:1 ratio for horizontal logos)
**Format**: PNG with transparency (for overlays on different backgrounds)
**Examples** (not currently in repo, but recommended):
- `roach-tracker-logo-square-512.png`
- `roach-tracker-logo-horizontal-300.png`
- `roach-tracker-favicon-32.png`

### Icons

**Purpose**: Favicons, app icons, UI elements
**Recommended Dimensions**: 16×16, 32×32, 64×64, 128×128, 256×256, 512×512 px
**Format**: PNG or ICO (for favicon), SVG (for scalable UI icons)
**Examples** (not currently in repo):
- `roach-tracker-icon-16.png` - Favicon small
- `roach-tracker-icon-32.png` - Favicon standard
- `roach-tracker-icon-192.png` - Android Chrome icon
- `roach-tracker-icon-512.png` - High-res app icon

### Screenshots

**Purpose**: Documentation, tutorials, feature showcases
**Recommended Dimensions**: 1920×1080 px or actual application viewport size
**Format**: PNG (for UI screenshots with text), JPG (for photos)
**Examples** (not currently in repo, but recommended):
- `screenshot-dashboard.png`
- `screenshot-log-sighting-form.png`
- `screenshot-statistics-page.png`
- `screenshot-mobile-navigation.png`

### Diagrams and Infographics

**Purpose**: Architecture diagrams, flowcharts, process illustrations
**Recommended Format**: SVG (scalable, small file size), PNG (raster fallback)
**Examples** (not currently in repo):
- `architecture-diagram.svg`
- `authentication-flow.svg`
- `database-schema.png`

---

## Image Optimization

### File Size Optimization Techniques

**1. Choose the Right Format**:
- **PNG**: Logos, icons, UI screenshots (supports transparency, lossless)
- **JPG**: Photos, complex images with gradients (smaller file size, lossy)
- **SVG**: Scalable graphics, logos, icons (vector, infinite scaling)
- **WebP**: Modern format (better compression than JPG/PNG, but less universal support)

**2. Compress Images**:

**Using ImageMagick** (command-line tool):
```bash
# PNG compression (lossless)
convert input.png -strip -quality 95 output.png

# JPG compression (lossy, 85% quality is good balance)
convert input.jpg -strip -quality 85 output.jpg

# Resize large images
convert input.png -resize 1280x640 -strip -quality 90 output.png
```

**Using pngquant** (PNG-specific compressor):
```bash
# Install pngquant
sudo apt-get install pngquant  # Debian/Ubuntu
brew install pngquant          # macOS

# Compress PNG
pngquant --quality=85-95 input.png -o output.png
```

**Using online tools**:
- [TinyPNG](https://tinypng.com/) - Excellent PNG/JPG compression
- [Squoosh](https://squoosh.app/) - Google's image optimizer
- [ImageOptim](https://imageoptim.com/) - macOS app for image optimization

**3. Strip Metadata**:
```bash
# Remove EXIF metadata (reduces file size, improves privacy)
exiftool -all= image.jpg

# Or using ImageMagick
convert input.jpg -strip output.jpg
```

**4. Use Appropriate Dimensions**:
- Don't upload 4K images for a 400px display
- Match image dimensions to actual usage size
- Provide multiple sizes if needed (@2x for Retina displays)

### Optimization Checklist

Before committing new images to the repository:

- [ ] Image dimensions appropriate for use case
- [ ] File format optimized (PNG for transparency, JPG for photos)
- [ ] File size < 1MB (ideally < 500KB for fast loading)
- [ ] Metadata stripped (EXIF data removed for privacy)
- [ ] Compression applied (80-90% quality for JPG, pngquant for PNG)
- [ ] Filename descriptive and follows naming convention
- [ ] Alt text planned for accessibility

---

## Web Optimization

### Serving Images Efficiently

**Lazy Loading** (for images below the fold):
```html
<img src="global-assets/images/roach-tracker-banner.png"
     alt="Roach Tracker Banner"
     loading="lazy">
```

**Responsive Images** (serve different sizes for different screens):
```html
<picture>
    <source srcset="global-assets/images/banner-1920.png" media="(min-width: 1200px)">
    <source srcset="global-assets/images/banner-1280.png" media="(min-width: 768px)">
    <source srcset="global-assets/images/banner-640.png" media="(max-width: 767px)">
    <img src="global-assets/images/banner-1280.png" alt="Roach Tracker Banner">
</picture>
```

**Retina/High-DPI Support**:
```html
<img src="global-assets/images/logo.png"
     srcset="global-assets/images/logo@2x.png 2x,
             global-assets/images/logo@3x.png 3x"
     alt="Roach Tracker Logo">
```

**CDN Integration** (for production):
```html
<!-- Serve from GitHub raw URL (not recommended for production) -->
<img src="https://raw.githubusercontent.com/dnoice/Roach-Tracker/main/global-assets/images/roach-tracker-banner.png" alt="Roach Tracker Banner">

<!-- Better: Serve from CDN like jsDelivr -->
<img src="https://cdn.jsdelivr.net/gh/dnoice/Roach-Tracker/global-assets/images/roach-tracker-banner.png" alt="Roach Tracker Banner">
```

---

## Accessibility Guidelines

### Alt Text Best Practices

**Good Alt Text**:
- Describes the image content and context
- Concise but informative (< 125 characters ideal)
- Omits redundant phrases like "image of" or "picture of"
- Provides equivalent information to what the image conveys

**Examples**:

```markdown
<!-- Banner -->
![Roach Tracker - Professional pest documentation application](global-assets/images/roach-tracker-banner.png)

<!-- Logo -->
![Roach Tracker logo](global-assets/images/roach-tracker-logo.png)

<!-- Screenshot -->
![Dashboard showing recent sightings table and statistics cards](global-assets/images/screenshot-dashboard.png)

<!-- Decorative image (no information conveyed) -->
![](global-assets/images/decorative-divider.png)
<!-- OR in HTML: -->
<img src="decorative-divider.png" alt="" role="presentation">
```

### Color and Contrast

**Ensure images with text meet WCAG standards**:
- Text on image background: minimum 4.5:1 contrast ratio
- Large text (18pt+): minimum 3:1 contrast ratio
- Use [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/)

**Don't rely solely on color**:
- If color conveys meaning, provide alternative indication (text, icon, pattern)
- Example: Instead of red=bad, green=good, use icons or labels as well

---

## Version Control Best Practices

### Git Considerations for Images

**Binary Files**:
- Images are binary files (not text-based)
- Git stores full copy of each version (file size adds up quickly)
- Minimize frequent changes to large images

**Git LFS (Large File Storage)**:
For projects with many large images (>5MB), consider Git LFS:

```bash
# Install Git LFS
git lfs install

# Track PNG files
git lfs track "*.png"

# Track JPG files
git lfs track "*.jpg"

# Commit .gitattributes
git add .gitattributes
git commit -m "Configure Git LFS for images"
```

**Best Practices**:
- Optimize images before committing (reduce file size)
- Don't commit multiple versions (v1, v2, v3) - replace the file
- Use descriptive commit messages: "Update banner with new branding"
- Consider using external asset hosting for very large files (>25MB)

### Commit Message Examples

**Good Commit Messages**:
```
Add main repository banner image
Update logo with new color scheme
Add dashboard screenshot for documentation
Optimize banner image file size (2.5MB → 800KB)
```

**Bad Commit Messages**:
```
Add image
Update banner.png
Image changes
asd
```

---

## Legal and Licensing

### Image Rights and Attribution

**Original Assets Created for Roach Tracker**:
- Banner, logos, icons created specifically for this project
- Copyright: dnoice + Claude AI
- License: Same as project license (see root LICENSE file)

**Third-Party Assets** (if using):
- Must have appropriate license (CC0, CC-BY, MIT, etc.)
- Provide attribution in README or CREDITS file
- Check license allows commercial use (if applicable)
- Include license text or link

**Example Attribution**:
```markdown
## Image Credits

- Roach icon by [Icon Author](link) - License: CC-BY 4.0
- Banner background texture from [Source](link) - License: CC0 (Public Domain)
```

### Stock Photos and Icons

**Free Resources** (with attribution):
- [Unsplash](https://unsplash.com/) - Free high-quality photos (CC0)
- [Pexels](https://www.pexels.com/) - Free stock photos (Custom license, commercial OK)
- [Font Awesome](https://fontawesome.com/) - Free icons (SIL OFL 1.1 license)
- [Heroicons](https://heroicons.com/) - Free SVG icons (MIT license)
- [Undraw](https://undraw.co/) - Free illustrations (Open-source, MIT)

**Premium Resources** (paid, but high quality):
- [Adobe Stock](https://stock.adobe.com/)
- [Shutterstock](https://www.shutterstock.com/)
- [iStock](https://www.istockphoto.com/)

---

## Recommended Future Assets

The following assets would enhance the project but are not yet created:

### Branding Assets

1. **Logo Variations**
   - `roach-tracker-logo-square-512.png` - Square logo for app icons
   - `roach-tracker-logo-horizontal-300.png` - Horizontal logo for headers
   - `roach-tracker-logo-white.png` - White version for dark backgrounds
   - `roach-tracker-logo.svg` - Scalable vector version

2. **Favicons**
   - `favicon.ico` - 16×16 and 32×32 multi-resolution ICO
   - `favicon-192.png` - Android Chrome icon
   - `apple-touch-icon.png` - iOS home screen icon (180×180)
   - `favicon.svg` - Modern SVG favicon

3. **Social Media Assets**
   - `social-preview.png` - 1200×630 for Facebook/Twitter cards
   - `social-square.png` - 1080×1080 for Instagram/LinkedIn

### Documentation Assets

4. **Screenshots**
   - `screenshot-dashboard.png` - Dashboard overview
   - `screenshot-log-sighting.png` - Sighting form
   - `screenshot-statistics.png` - Analytics page
   - `screenshot-mobile.png` - Mobile responsive view
   - `screenshot-pdf-report.png` - Example PDF export

5. **Diagrams**
   - `architecture-diagram.svg` - System architecture
   - `database-schema.png` - Database ER diagram
   - `authentication-flow.svg` - Login/auth flowchart
   - `data-flow-diagram.svg` - Data processing flow

### Marketing Assets

6. **Promotional Materials**
   - `feature-graphic-1024x500.png` - Google Play feature graphic
   - `promo-video-thumbnail.png` - YouTube thumbnail
   - `comparison-chart.png` - Feature comparison with alternatives

---

## Troubleshooting

### Image Not Displaying in README

**Issue**: Markdown image not showing on GitHub
**Solutions**:
1. Check file path is correct (case-sensitive!)
2. Verify file is committed and pushed to GitHub
3. Try absolute GitHub URL instead of relative path
4. Check if file size exceeds GitHub limits (25MB max)
5. Ensure image format is supported (PNG, JPG, GIF, SVG)

**Test with absolute URL**:
```markdown
![Banner](https://raw.githubusercontent.com/dnoice/Roach-Tracker/main/global-assets/images/roach-tracker-banner.png)
```

### Image File Too Large

**Issue**: Image takes too long to load or exceeds GitHub file size limit
**Solutions**:
1. Compress image with TinyPNG or Squoosh
2. Reduce dimensions if larger than needed
3. Convert PNG to JPG (if transparency not needed)
4. Use Git LFS for files > 5MB
5. Host on external CDN (Imgur, Cloudinary)

### Image Quality Loss

**Issue**: Image looks blurry or pixelated after optimization
**Solutions**:
1. Increase compression quality (85-95% for JPG)
2. Use PNG instead of JPG for text/logos
3. Ensure source image is high enough resolution
4. Export at 2x dimensions for Retina displays
5. Use SVG for logos/icons (scalable without quality loss)

---

## Related Documentation

- [Static Assets README](../../static/README.md) - User-uploaded images and photos
- [Main README](../../README.md) - Project overview (uses banner image)

---

## Contact & Support

For issues, questions, or contributions:
- GitHub Issues: https://github.com/dnoice/Roach-Tracker/issues
- Main README: [../../README.md](../../README.md)

---

**Version**: 1.2.0
**Created**: 2025-10-31
**Updated**: 2025-11-01
**Author**: dnoice + Claude AI
