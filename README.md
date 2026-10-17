# ComfyUI Image Filename Dataset

A ComfyUI custom node that loads images from an input subfolder and returns
two aligned lists:

- `images`: individual ComfyUI IMAGE tensors
- `filenames`: original filenames, including file extensions

## Features

- Supports PNG, JPG, JPEG, and WEBP
- Sorts filenames alphabetically for deterministic ordering
- Preserves image-to-filename correspondence
- Supports images with different dimensions
- Uses ComfyUI's V3 node API

## Installation

Clone this repository into your ComfyUI `custom_nodes` directory:

```bash
git clone https://github.com/YOUR_USERNAME/comfyui-image-filename-dataset.git
```

Restart ComfyUI.

## Usage

1. Place images in a subfolder of ComfyUI's `input` directory.
2. Add the "Load Image and Filename (from Folder)" node.
3. Select the folder.
4. Connect the `images` and `filenames` outputs to downstream nodes.

The items at the same list index correspond to each other.

## Requirements

Uses ComfyUI's Python environment and its installed dependencies.