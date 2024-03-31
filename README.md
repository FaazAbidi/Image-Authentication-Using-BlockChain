# Image Authentication Using BlockChain

A Python-based web application that combines blockchain and image hashing technologies to authenticate images. This project is a proof of concept for enhancing image authenticity by creating a minimal blockchain database and implementing image hashing for similarity checks.

## Abstract
With the rise of digital media, image tampering has become a prevalent issue. Our project addresses this by utilizing a blockchain system to maintain the authenticity of stored images. By hashing images and comparing them using a distance technique, we can assess the similarity between two separate images. This project aims to prove the concept of combining image hashing methods with blockchain for image authentication.

## Installation
Clone the repository to your local machine:
```
git clone https://github.com/yourgithub/image-authentication-blockchain.git
cd image-authentication-blockchain
```

## Requirements
- Python 3.8 or higher
- Django 3.2 or higher
- Other dependencies listed in requirements.txt

Install the required packages:
```
pip install -r requirements.txt
```

## Usage
To run the Django web application:
```
python manage.py runserver
```
Navigate to http://127.0.0.1:8000/ in your web browser to access the application.

## Features
Image Hashing Algorithms: Implements several image hashing algorithms, including Difference Hash, Average Hash, Perceptual Hash, Wavelet Hash, and Color Hash, to generate unique identifiers for images.
Blockchain Database: A minimal blockchain database that stores image hashes as data. It implements a proof of work concept to add new blocks, ensuring the authenticity and integrity of stored images.
Web Interface: A user-friendly web application to authenticate and search for images stored in the blockchain. It includes features for uploading images, viewing image details, and visualizing the blockchain structure.
Three.js Blockchain Visualization: Utilizes Three.js to create dynamic 3D visuals of the blockchain, enhancing the user experience.
Experimental Results
The application successfully verifies the authenticity of images with separate hash codes for even slight variations in image characteristics. This validates our approach to secure image authentication using blockchain and image hashing.

## Conclusion
Our project demonstrates the feasibility of using blockchain technology combined with image hashing to authenticate images. While the current system is a proof of concept, it lays the groundwork for further development in this promising area.

## Acknowledgements
Special thanks to Professor Muhammad Mobeen Movania for his invaluable guidance and support throughout the development of this project.

## Contact
For any queries regarding this project, please contact:

- Syed Hasan Faaz Abidi - sa06195@st.habib.edu.pk
- Hussain Abbass - ha06228@st.habib.edu.pk

Research Paper Link: [HERE](https://drive.google.com/file/d/1fhxjLytcjnbZvvV8jQZW_VXod4cN81SD/view?usp=sharing)
