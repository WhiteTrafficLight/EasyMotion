# Animated NFT Creator Prototype

This project is a prototype tool designed for NFT artists to streamline the creation of animated art pieces. Developed under **Turing AI Cultures**, it explores advanced image segmentation and animation techniques to automate repetitive tasks and enhance creativity.

---

## Features
1. **Automasking**:
   - Reduces time spent on manual masking by leveraging Meta's [Segment Anything Model](https://github.com/facebookresearch/segment-anything).
2. **Background Autofill** *(Planned)*:
   - Automatically fills in the background after segmentation.
3. **Layer Animation**:
   - Animates segmented image layers based on sample MIDI data.

---

## Installation
1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/animated-nft-creator.git
   cd animated-nft-creator
   ```

2. **Set up the environment**:
   - Create the `conda` environment from the `environment.yml` file:
     ```bash
     conda env create -f environment.yml
     ```
   - Activate the environment:
     ```bash
     conda activate yolo
     ```

3. **Run the application**:
   ```bash
   python main.py
   ```

---

## Usage
1. **Run the program**:
   - Start the application with:
     ```bash
     python main.py
     ```
2. **Tested Features**:
   - Automasking of art images using the Segment Anything Model.
   - Animation of segmented layers based on sample MIDI data.

---

## Acknowledgments
This project uses the [Segment Anything Model](https://github.com/facebookresearch/segment-anything) by Meta for automasking.

---

