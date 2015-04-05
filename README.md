## coding challenge famo.us

###problem statement
>Design two http end points get and put . put takes the input in json format 
>{fileName:"abc.txt",fileContent:"this is a test file"}
>get returns least recent file which was posted by get and not exposed yet


###files
* server.py              - contains src 
* curl-test-cases        - test cases written in CURL
* Dockerfile             - run this to create docker image
* config.cf              - contains cofiguration such as port number, db connection etc

###api calls
```sh
$ curl -H "content-Type: application/json" -d '{"fileName":"abc1.txt","fileContent":"this is a first file"}' http://127.0.0.1:5000/post
```
```sh
{
  "message": "data added successfully", 
  "success": true
}
```
```sh
$ curl http://127.0.0.1:5000/get
```
```sh
{
  "fileContent": "this is a first file", 
  "fileName": "abc1.txt", 
  "success": true
}
```
###validations
- fileName and fileContent cannot be empty 

