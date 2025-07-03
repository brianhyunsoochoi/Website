# QSOC-Website

This is the QSOC-Website application.

## Cloning the Repository

Clone the repository using:
git clone https://github.com/samwp95/QSOC-Website.git
cd QSOC-Website

## Installing Requirements

Install the dependencies:
pip install -r requirements.txt

## Running the Web App

Start the application with:
uvicorn main:app --reload

## Exporting the Website to Static Files

To export the fastAPI app into static files to host on Github Pages:
```zsh
python export_static.py
```

Refer to the documentation for more details.
