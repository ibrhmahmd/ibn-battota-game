
# Game Design Document: Ibn Batota's Journey

## 1. Executive Summary

The project titled **"Ibn Batota's Journey"** is an educational adventure game developed using the **Python pgzrun** library. It aims to provide a beginner-friendly yet immersive experience that retraces the 14th-century travels of the famous Moroccan explorer, Ibn Battuta. The game focuses on cultural authenticity, historical accuracy, and engaging mini-game mechanics that reflect the diverse regions he visited. By integrating traditional music and visual storytelling, the game serves as both an entertainment piece and a hiestorical learning tool.

## 2. Core Gameplay and Level Structure

The gameplay is structured around a linear progression through thirteen historically significant cities. Each city serves as a unique level where the player must complete a specific mini-game to unlock the next destination on the world map. This structure ensures a chronological narrative flow, mirroring the actual timeline of Ibn Battuta's travels from 1325 to 1354.

| Level | City | Regional Focus | Primary Instrument |
| :--- | :--- | :--- | :--- |
| 1 | **Tangier** | Departure & Preparation | Rebab |
| 2 | **Fez** | Academic Scholarship | Oud |
| 3 | **Granada** | Al-Andalus Culture | Guitarra Morisca |
| 4 | **Cairo** | Urban Commerce | Qanun |
| 5 | **Damascus** | Religious Tradition | Ney |
| 6 | **Medina** | Spiritual Reflection | Daff |
| 7 | **Mecca** | The Hajj Pilgrimage | Voice/Chant |
| 8 | **Baghdad** | Intellectual Heritage | Santur |
| 9 | **Persia** | Artistic Expression | Tar |
| 10 | **Istanbul** | Imperial Diplomacy | Baglama |
| 11 | **Delhi** | Judicial Governance | Sitar |
| 12 | **Beijing** | Eastern Trade | Pipa |
| 13 | **Timbuktu** | Saharan Knowledge | Kora |

## 3. Narrative and Visual Storytelling

The narrative is delivered through three major story milestones: the **Opening Cinematic**, the **Mid-game Turning Point**, and the **Final Conclusion**. These levels use static historical illustrations and text to convey the emotional and political weight of Ibn Battuta's experiences.

> "I set out alone, having neither fellow-traveler in whose companionship I might find cheer, nor caravan whose party I might join, but swayed by an overmastering impulse within me and a desire long-cherished in my bosom to visit these illustrious sanctuaries." — *Ibn Battuta, The Rihla*

Visual storytelling is further enhanced by a **Historical Photo Gallery**. As players complete levels, they unlock authentic images and "Did You Know?" facts that provide deeper context into the 14th-century world. This system rewards curiosity and reinforces the educational goals of the project.

## 4. Technical Implementation and Development Phases

The technical framework is designed for **beginner-level Python developers**. It utilizes a simple state machine to switch between the world map and individual mini-games. Data persistence is handled via a basic text-based save system that tracks the player's progress through the city list.

### Development Roadmap

| Phase | Title | Key Activities |
| :--- | :--- | :--- |
| **Phase 1** | **Pre-production** | Historical research, mini-game concepting, and asset sourcing for music and backgrounds. |
| **Phase 2** | **Core Systems** | Implementation of the world map, character movement, and the save/load framework. |
| **Phase 3** | **Content Creation** | Iterative development of the 13 city levels and their respective mini-game mechanics. |
| **Phase 4** | **Polish & UI** | Refinement of the user interface, integration of the gallery, and final bug testing. |

## 5. Visual Asset Descriptions

The visual identity of the game relies on evocative backgrounds and story-driven imagery. Each background is designed to capture the unique architectural and environmental essence of the location.

- **Tangier Background**: A vibrant coastal scene featuring the Strait of Gibraltar, with 14th-century dhows anchored near white-washed Moroccan walls.
- **Cairo Background**: The bustling streets of the Mamluk-era markets, with the distant silhouettes of the Giza pyramids under a hazy desert sun.
- **Delhi Background**: The grand court of Sultan Muhammad bin Tughluq, characterized by Indo-Islamic architecture and opulent decorations.
- **Timbuktu Background**: The iconic mud-brick Sankore Mosque set against a deep orange Saharan sunset, symbolizing the edge of the known world.

The story level images focus on human connection: the sorrowful departure from his parents in Tangier, the high-stakes judicial decisions in the Delhi court, and the final years in Fez where he dictates his life's work to the scholar Ibn Juzayy.
