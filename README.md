# How to build the image, run the container and use the program.


# Build the image
1. Make sure you have docker installed and from a terminal navigate to the folder where the Dockerfile is. Now run the command:     "docker build -t texlinter ."


# Start a container from the image
2. Run the command: "docker run -t -d --name texlinter -v <path to local folder>:/app/tex texlinter"


# Use the program
3. If you wish to format a file and save it as a new file run the command: 
"docker exec texlinter python main.py /app/tex/<file to be formatted> -n /app/tex/<new file>"

If you wish to format a file and override the old file run the command:
"docker exec texlinter python main.py /app/tex/<file to be formatted>"