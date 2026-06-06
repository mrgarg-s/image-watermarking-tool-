# Secure Watermarking Software

A comprehensive, dual-application suite for applying secure, highly customizable watermarks to documents and images, and securely verifying/decrypting them. 

This suite consists of two Python GUI applications:

1. **Watermark Software - Secure Edition**: A powerful creator tool for applying text/logo watermarks, editing images, and encrypting exports.

2. **Watermark Verifier - Secure Edition**: A companion decryption and verification tool to safely open encrypted files and read hidden, secure metadata.

---

## Overview

This project is a Python-based secure watermarking desktop application designed for protecting digital content using visible and encrypted watermarking techniques.

The software supports:

* Text watermarking
* Logo watermarking
* Metadata protection
* AES-GCM encryption
* PDF watermarking
* Batch processing
* Secure verification system

The project also includes a separate verifier application used to decrypt and verify protected metadata.

---

# Main Features

## Text Watermarking

* Multi-line watermark text
* Adjustable font size
* Rotation controls
* Opacity adjustment
* Stroke / outline effect
* Custom colors
* Custom font loading

## Logo Watermarking

* Upload logo images
* Resize and rotate logos
* Opacity controls
* Tiled watermark patterns

## PDF Support

* Multi-page PDF watermarking
* Apply watermark to all pages
* Custom page-by-page settings

## Image Enhancement

* Brightness adjustment
* Contrast adjustment
* Sharpness controls

## Security Features

* AES-GCM encryption
* SHA-256 password hashing
* Metadata encryption
* Full file encryption
* Password-protected verification

## Export Formats

* PNG
* JPEG
* PDF
* DOCX

## Batch Processing

* Process multiple files
* Folder watermarking
* Bulk export support

## User Interface

* Dark themed interface
* Drag & drop support
* Zoom and pan controls
* Undo / Redo system
* Interactive watermark editing

---

# Verifier Application

The verifier software allows users to:

* Read embedded metadata
* Decrypt protected information
* Verify ownership details
* Open encrypted files
* Validate watermark authenticity

Supported formats:

* PNG
* JPG
* PDF
* DOCX
* ENC encrypted files

---

# Technologies Used

* Python
* Tkinter
* Pillow (PIL)
* Cryptography
* PyMuPDF
* python-docx
* tkinterdnd2

---

# Installation

## Install Required Libraries

```bash
pip install pillow cryptography pymupdf python-docx tkinterdnd2
```

---

# Run Application

## Watermark Software

```bash
python "Watermark software.py"
```

## Watermark Verifier

```bash
python "Watermark verifier.py"
```

---

# Security

The software uses:

* AES-GCM encryption
* SHA-256 hashing
* Secure metadata storage
* Password-based encryption system

Encrypted files require the correct password for decryption and verification.

---

# Disclaimer

This software is developed for educational and security purposes only.

The author is not responsible for misuse, unauthorized distribution, or illegal activities performed using this software.

---

# Copyright

Copyright (c) 2026 Mr Garg
All Rights Reserved.
