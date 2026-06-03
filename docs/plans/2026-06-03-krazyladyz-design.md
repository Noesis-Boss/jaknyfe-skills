# Design Specification: krazyladyz.com

## Overview
A greeting-card and poster sales site for Krazy Ladyz, focusing on a curated gallery with an underlying catalog, integrated with character stories for the three "Krazy Ladyz".

## Visual Identity: Maximalist Boho
- **Palette**: Deep teal background (#004d4d), neon pink (#ff1493), mustard yellow (#ffdb58).
- **Patterns**: Intricate floral and geometric patterns (inspired by ref image) used as living backgrounds.
- **Tone**: Vibrant, artistic, bold, and pattern-rich.

## The Trio (Characters)
1. **Lola (The Pattern Queen)**: Middle character. Vibe: "Bold & Clashing". Assigned Color: Teal. Focus: High-contrast posters and neon cards.
2. **Zelda (The Whimsical Soul)**: Left character. Vibe: "Vintage Garden". Assigned Color: Mustard Yellow. Focus: Botanical designs and nostalgic cards.
3. **Moxie (The Edgy Creator)**: Right character. Vibe: "Modern Geometric". Assigned Color: Neon Pink. Focus: Sharp lines, vibrant color blocks, minimalist-yet-loud posters.

## Homepage Structure
### 1. Interactive Triptych Hero
- 3-column layout featuring Zelda, Lola, and Moxie.
- Hover effects: Specific background patterns bloom, character story snippets appear.
- Click action: Filters the gallery below to that character's curated collection.

### 2. Curated Gallery / Catalog
- **Masonry Grid**: Art-gallery style layout.
- **Character Badging**: "Hand-picked by Moxie", etc.
- **Styling**: Product cards with thick, character-colored borders.
- **Catalog Toggle**: Switch between "Curated" and "All Treasures".
- **Filters**: Type (Card/Poster), Artist, Occasion.

### 3. Lore Integration
- Character story excerpts integrated into the hero and product views.

## Technical Plan
- **Framework**: Zo Site (React + Vite + Bun).
- **Styling**: Tailwind CSS 4.
- **Icons**: Lucide React / Tabler Icons.
- **Cart**: Stripe integration (slide-out cart).
