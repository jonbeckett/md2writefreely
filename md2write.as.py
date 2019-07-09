# Script         : Markdown to Write.As Uploader
#                  Recursively reads a directory containing markdown files, and uploads them to write.as
#                  Designed to work with the output of wp2md (see https://github.com/jonbeckett/wp2md)
# Author         : Jonathan Beckett (jonbeckett@outlook.com)
# Compatibility  : Python 3.x
# Pre-Requisites : None


# path where markdown files reside
root_path = "c:\\temp\\output"

# write.as credentials
username = "username"
password = "password"

# collection (blog) to post to
collection_name = "username"


# Import modules
import os
import os.path
import json
import time
from urllib.parse import urlencode
from urllib.request import Request, urlopen

print('Authenticating...')
url = 'https://write.as/api/auth/login'
data = ('{"alias":"' + username + '","pass":"' + password + '"}').encode()
auth_request = Request(url, data)
auth_request.add_header('Content-Type','application/json')
auth_response = urlopen(auth_request).read().decode()
json_response = json.loads(auth_response)
access_token = json_response['data']['access_token']
print('Access Token : ' + access_token)

for subdir, dirs, files in os.walk(root_path):
	for file in files:
		if '.md' in file and 'README.md' not in file:

			print("Processing " + file)
			
			# Read the file contents
			markdown_file_full_path = os.path.join(subdir, file)
			markdown_file = open(markdown_file_full_path,'r')
			markdown_text = markdown_file.read()
			
			# split the line into files, and chop the top 4 off
			# (to get rid of the title and date, as output by wp2md)
			markdown_text_lines = markdown_text.splitlines()
			hybrid_text_lines = []
			hybrid_text_lines += markdown_text_lines[4:]
			
			# build the post title and body
			post_title = markdown_text_lines[0].replace('# ','')
			post_body = '\r\n'.join(hybrid_text_lines)
			
			# Extract the date from the filename
			# (so we may use it to back-date the post into write.as)
			year = file[0:4]
			month = file[5:7]
			day = file[8:10]
			post_date = year + '-' + month + '-' + day + 'T00:00:00Z';
			
			# configure write.as collection API endpoint
			url = 'https://write.as/api/collections/' + collection_name + '/posts'
			
			# prepare the data to post to the API
			data = ({'body':post_body,'title':post_title,'created':post_date})
			data = json.dumps(data)
			data = str(data)
			data = data.encode('utf-8')
			
			# post the request to the API
			post_request = Request(url, data)
			post_request.add_header('Content-Type','application/json')
			post_request.add_header('Authorization','Token ' + access_token)
			post_response = urlopen(post_request).read().decode()
			
			# todo - validate the post (check post_response for 201
			
			# close the open markdown file
			markdown_file.close()
			
			# wait 1 second (to avoid stressing the API too much)
			time.sleep(1)
			
