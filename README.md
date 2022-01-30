# Tiny Url Project
### For: United Masters
Time Spent: 4 hours

### Prerequisites:
- Docker
- Python 3.8
- Make

### Instructions
#### Starting:
1. For first timers - Execute this action: `make get_redis start_redis`
   - It pulls the Redis docker image, creates a docker container for it, and runs the container.
2. Execute `make run`
    - This action creates the python environment Flask will run in, set the environment variables, and run Flask.
    - From here, you will be able to click the provided url.
#### Stopping:
1. In the same terminal, executing ctrl+C will stop Flask.
2. To stop Redis, execute `make stop_redis`
#### Cleanup:
1. After you are done with this project, execute `make clean`
   - This will stop and delete the Docker container.

### Flask Operations:
This Flask server has 4 endpoints: 
1. "localhost:5000/" GET returns a landing page where a user can enter their url.
2. "localhost:5000/send_url" POST is what receives the form if a user enters a url and presses enter or clicks "submit". The user will receive a url key return.
3. "localhost:5000/[id]" 
   - POST receives a url, stores it, and returns the key to retrieve it. 
   - GET receives a key and retrieves the orginal url.
4. "localhost:5000/send_url_json" POST that is similar to send_url except it receives a json body and looks for the key "url" to get the url.
