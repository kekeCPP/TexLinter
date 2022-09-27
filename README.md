<h1>How to build the image, run the container and use the program.</h1>


<h2>Install and start the program</h2>
<p>1. Make sure you have docker installed. Download the files from this repo and change the local directory in the docker-compose.yml to a local directory on your computer which has the .tex files you want to format. Now navigate to the folder from a terminal and run the command: "docker compose run --rm app"</p>

<h2>Use the program</h2>
<p>3. If you wish to format a file and save it as a new file make sure you are in the /app directory and run the command: 
"python main.py ./tex/<file to be formatted> -n ./tex/<new file>"

If you wish to format a file and override the old file make sure you are in the /app directory and run the command:
"python main.py ./tex/<file to be formatted>"</p>
