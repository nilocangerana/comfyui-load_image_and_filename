
import os

import numpy as np
import torch
from PIL import Image, ImageOps

import folder_paths
from comfy_api.latest import ComfyExtension, io


def secure_subfolder_path(base_dir: str, folder: str) -> str:
    """Resolve a folder inside ComfyUI's input directory safely."""
    base = os.path.realpath(base_dir)
    target = os.path.realpath(os.path.join(base, folder))

    try:
        if os.path.commonpath([base, target]) != base:
            raise ValueError("Selected folder must be inside the input directory.")
    except ValueError as exc:
        raise ValueError("Invalid input folder.") from exc

    if not os.path.isdir(target):
        raise ValueError(f"Input folder does not exist: {folder}")

    return target


def load_image(image_path: str) -> torch.Tensor:
    """Load one image as a ComfyUI IMAGE tensor: [1, H, W, C]."""
    with Image.open(image_path) as image:
        image = ImageOps.exif_transpose(image)
        image = image.convert("RGB")
        image_array = np.array(image, dtype=np.float32) / 255.0

    return torch.from_numpy(image_array).unsqueeze(0)


class LoadImageAndFilenameDataSetFromFolderNode(io.ComfyNode):

    @classmethod
    def define_schema(cls):
        return io.Schema(
            node_id="Nilo_LoadImageAndFilenameDataSetFromFolder",
            display_name="Load Image and Filename (from Folder)",
            category="image/dataset",
            description=(
                "Load images and their matching filenames from a "
                "ComfyUI input subfolder. Supports PNG, JPG, JPEG, WEBP."
            ),
            inputs=[
                io.Combo.Input(
                    "folder",
                    options=folder_paths.get_input_subfolders(),
                    tooltip="The input subfolder containing the images.",
                )
            ],
            outputs=[
                io.Image.Output(
                    display_name="images",
                    is_output_list=True,
                    tooltip="Images in filename-sorted order.",
                ),
                io.String.Output(
                    display_name="filenames",
                    is_output_list=True,
                    tooltip="Matching filenames, including extensions.",
                ),
            ],
        )

    @classmethod
    def execute(cls, folder) -> io.NodeOutput:
        input_dir = folder_paths.get_input_directory()
        image_dir = secure_subfolder_path(input_dir, folder)

        valid_extensions = (".png", ".jpg", ".jpeg", ".webp")

        filenames = sorted(
            name
            for name in os.listdir(image_dir)
            if name.lower().endswith(valid_extensions)
            and os.path.isfile(os.path.join(image_dir, name))
        )

        images = [
            load_image(os.path.join(image_dir, filename))
            for filename in filenames
        ]

        return io.NodeOutput(images, filenames)


class ImageFilenameDatasetExtension(ComfyExtension):

    async def get_node_list(self) -> list[type[io.ComfyNode]]:
        return [LoadImageAndFilenameDataSetFromFolderNode]


async def comfy_entrypoint() -> ImageFilenameDatasetExtension:
    return ImageFilenameDatasetExtension()
