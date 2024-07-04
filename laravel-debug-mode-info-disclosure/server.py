from bottle import route, run, HTTPResponse, static_file
import logging
import pathlib

logger = logging.getLogger(__name__)

filename = pathlib.Path()
root_folder= filename.parent

@route(f'/upload', method='POST')
def upload():
	env = filename / ".env"
	if env.exists():
		return static_file(env.name, root=root_folder)
	else:
		return HTTPResponse(status=404, body=f"Sorry, Dave, the file {env.resolve()}\n\r") 

if __name__ == "__main__":
	run(host="172.16.10.117", port=80, debug=True)
