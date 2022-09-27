<h1>How to build the image, run the container and use the program.</h1>


<h2>Build the image</h2>
<p>1. Make sure you have docker installed. Download the files from this repo and navigate to the folder from a terminal. Now run the command:     
  "docker build -t texlinter ."</p>


<h2>Start a container from the image</h2>
<p>2. Run the command: "docker run -t -d --name texlinter -v <path to local folder>:/app/tex texlinter"</p>


<h2>Use the program</h2>
<p>3. If you wish to format a file and save it as a new file run the command: 
"docker exec texlinter python main.py /app/tex/<file to be formatted> -n /app/tex/<new file>"

If you wish to format a file and override the old file run the command:
"docker exec texlinter python main.py /app/tex/<file to be formatted>"</p>
