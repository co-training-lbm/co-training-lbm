https://co-training-lbm.github.io/

# A Systematic Study of Data Modalities and Strategies for Co-training Large Behavior Models for Robot Manipulation

This repository contains the website for the paper "A Systematic Study of Data Modalities and Strategies for Co-training Large Behavior Models for Robot Manipulation".

## Running the Website Locally

To view the website locally, you can use Python's built-in HTTP server:

### Python 3
```bash
python3 -m http.server 8000
```

Then open your browser and navigate to:
```
http://localhost:8000
```

The website will be served from the root directory, and `index.html` will be automatically loaded.

## Project Structure

```
lbm1/
├── index.html                          # Main website file
├── images/                             # Images used in the website
│   ├── overview.png
│   ├── useful_cotraining_modalities.png
│   └── combined_modalities.png
├── videos/                             # Video files
│   ├── abstract/                       # Abstract section videos
│   ├── language_following/            # Language following videos
│   │   ├── seen_and_instruction_generalization/
│   │   └── unseen_objects/
│   └── simulation_unseen_tasks/       # Simulation unseen tasks videos
│       └── video_mapping.json         # Video filename mapping
└── README.md                           # This file
```

## Features

- **Interactive Video Selection**: 
  - Language Following section with dropdowns for experiment settings, layouts, and instructions
  - Simulation Unseen Tasks section with task and episode selection
  - Shuffle functionality for random video selection

- **Dynamic Content Loading**: Videos and instructions are loaded dynamically based on user selections

## Requirements

- A modern web browser (Chrome, Firefox, Safari, Edge)
- Python 3 (for local server) - optional, any static file server will work

## Notes

- The website is a static HTML page with embedded JavaScript
- All videos should be in MP4 format for best browser compatibility
- The video mapping file (`videos/simulation_unseen_tasks/video_mapping.json`) contains the mapping between tasks, episodes, and video filenames
