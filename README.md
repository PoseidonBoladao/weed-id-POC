# WeedID
#### Video Demo:  <URL HERE>
#### Description: My project is a web app that identifies weeds in images using machine learning.

## Introduction
This application aims to assist farmers, gardeners, and agricultural professionals in quickly and accurately detecting weed species, thereby facilitating more effective weed management and control strategies.\
The idea for WeedID came from a talk I had with a farmer who expressed the need for a more efficient way to identify and manage weeds in their fields.\
The application was designed to be used mostly with a mobile device, with in-field identification being the main use case.

## File description

### static/style.css
Contains the CSS styles for the web application's frontend.

### templates/about.html
Provides the HTML template for the 'About' page, detailing the project's purpose.

### templates/index.html
Serves as the main HTML template for the application's homepage.

### templates/layout.html
Provides the HTML layout to be used across all HTML pages within the app.\
It contains a bootstrap nav bar that references to other acessible pages.\
Also contains a flash message giving user feedback on errors and any conveninent message to be displayed.\
At last, it contains a footer crediting the web app author.\

### templates/newID.html
Serves as the HTML template for the new identification page.\
It contains a form that allows Desktop users to upload images and mobile users to either upload an image or capture a photo instantly.\
Image is then analyzed and processed using machine learning tools.

### templates/results.html
HTML template to display results after the image was correctly processed.\
Results are displayed in the form of a table that contains 4 headers and all possible weeds:
- Common names: displays common names of the weed.
- Probability: is the chance of the weed being accurately identified.
- Scientific name: is the universal scientific name of the weed.
- Images: contains a "google search" icon that redirects the user to a google images query containing the specific weed's scientific name.

### .dockerignore
Defines which files should not be stored in the Docker image.

### .gitignore
Defines which files should not be stored in Git Hub.

### app.py
Contains the python code with the Flask application.\
An API was used to process the image.\
The app was developed with the intention to be used mostly in field with mobile phones.\
However, recent Apple phones image capturing outputs a HEIC formatted image, which is not supported by the API.\
Hence, a function was defined to handle this and convert HEIC to JPEG.\
The API requires the use of a key which should be stored in an environment variable.\
With the key and image converted to JPEG, the program requests a response from the API via POST.\
If the response was successful, the results.html template is loaded and the data from response is passed to the page.

### Dockerfile
Defines the environment and instructions for containerizing the WeedID application.

### requirements.txt
Lists the Python dependencies required to run the WeedID application.

## Use of AI
This project utilized OpenAI's GPT-4 to assist in writing and refining code, as well as generating documentation. However, the fundamental logic and conception of the application were developed by the author.

## Hosting
The WeedID application is hosted on [Azure](https://azure.microsoft.com/) with the following URL: https://weed-id-poc-container-c9dgbbcngjfbdnht.northcentralus-01.azurewebsites.net/ \
The hosting environment is configured to use containers as the form of deployment.\
This ensures consistency across different environments and simplifies the deployment process, given that one of the libraries (pyheif) used in the project has specific system dependencies (libheif) that are encapsulated within the container.

## Design Considerations

### Use of API or Training Own Models
I decided to use an API that provides pre-trained machine learning models for image recognition, which is a faster and more practical way to develop the app.\
I plan to explore the possibility of training custom models in the future to improve accuracy and tailor the system to specific agricultural contexts.

### Container publishing
Given the mobile first approach, and Apple's presence in the market, HEIC to JPEG conversion was a big part of the application that could not be neglected.\
However, I had trouble deploying the application due to pyheif library's requirement for specific system-level packages (libheif), which are not included in the default container environment.\
To resolve this problem, containerization was used to encapsulate all dependencies, ensuring a consistent and portable deployment across different environments.