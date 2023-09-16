# 🦥 too lazy to write alt

[![general-english-image-caption-blip-2-6_7B](https://clarifai.com/api/salesforce/blip/models/general-english-image-caption-blip-2-6_7B/badge)](https://clarifai.com/salesforce/blip/models/general-english-image-caption-blip-2-6_7B)

generate and translate alt text using VLP and LLM.

*too lazy...* is mobile-friendly, allows multiple images to be uploaded via URL or directly, offers translation into multiple languages, and includes a "copy to clipboard" button for each generated alt text.

### language model

BLIP-2* OPT 6.7B model is fine-tuned for the image captioning task using the ViT-g image encoder and the [OPT language model](https://arxiv.org/pdf/2205.01068.pdf) with 6.7 billion parameters. The model uses the prompt "a photo of" as an initial input to the language model and is trained to generate the caption with the language modeling loss.

*[BLIP-2](https://arxiv.org/pdf/2301.12597.pdf) is an innovative and resource-efficient approach to vision-language pre-training (VLP) that utilizes frozen pretrained image encoders and large language models (LLMs) (e.g. OPT, FlanT5).

### supported formats

PNG, JPG, JFIF, TIFF, BMP, WEBP, JPEG, TIF

### limit per file

up to 20MB

### roadmap

- [ ] multiple dest langs (multiselect)
- [ ] multiple urls (comma-separated)
- [ ] download all generated alt texts in `txt` format
- [x] url and upload options
- [x] copy to clipboard
- [x] style
- [x] specs
- [ ] code comments

### license

[GNU General Public License v3.0](LICENSE)
