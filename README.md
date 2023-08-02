# Weavegrid Backend Coding Assessment

## Custom additions from @colinyoung follow :point-down:

### Running this project:

As a Dockerized application, it makes sense to build and run this application quickly, especially so you
don't have to deal with Python version issues. I found one way to do this:

```
docker run --rm -p 8080:80 -it $(docker build -q .) # Credit: https://stackoverflow.com/a/51314059

# Then, you can access the API at http://localhost:8080.
curl -i http://localhost:8080

# You can also change the base directory of the application (which must be a subdir of `filesystem_crawler`) using:
docker run -e UVICORN_BASEDIR=other_files --rm -p 8080:80 -it $(docker build -q .)

# You can, of course, run your Docker image however you like.
```

### Env vars

- UVICORN_BASEDIR: string

-----

## Introduction

The purpose of this exercise is for you to show us what you're made of! We know you can code, 
but we want to see where you fit and really shine! 
We want to understand both your coding style and your documentation patterns
while you attempt to make a simple program. We want to ensure that it is easy for others to contribute, read, and run.

The full evaluation criteria are provided below. We welcome your feedback on the exercise, as well as creative solutions.
We are happy to accommodate changes in the test format based on your specific context.

## The Exercise

### The Application
The application is a small REST API to display file information from a portion of the user’s file system. 
The user will specify a root directory when launching the application. All directories from the 
root on downward are then browsable using the REST API. Additionally, the application should have the 
ability to create new files and directories within the specified portion of the user's file system.
						
For example, suppose there is a directory ​`stuff/foo/`​ which contains the following:

```
foo1 # file
foo2 # file
bar/ # directory
  \  
  bar1 # file
  baz/ # subdirectory
```

If the REST API application is started with root directory of  `stuff/foo`​ it will return something like:
						
    GET / -> list contents of ​foo/​ (e.g. foo1, foo2, bar/) 
    GET /bar -> list contents of ​foo/bar/​ (e.g bar1, baz/) 
    GET /foo1 -> contents of file ​foo/foo1
    GET /bar/bar1 -> contents of file ​foo/bar/bar1

Now if we wanted to create a new file, foo3, or a new directory, bar2/, in the base directory, your
REST API will look something like: 
  
    POST /foo3 
    POST /bar2/

### Basic Rules
- You can use any programming language you like, but Python is preferred.  Infrastructure to help you 
get started on this assignment has been provided assuming Python would be used, but feel free to change things to work for your preferred language.  
  - Please inform your WeaveGrid recruiter if you intend to 
  use a language other than Python on this assignment to ensure we have an appropriate grader for you. 
- The application must be Dockerized.  You may use the dockerfile provided to you as a starting point and edit 
it as you see fit, including changing the library being used to create your API.  
- Provide an easy & user-friendly way for someone to run your application and enter the required configuration for the application.
- Your REST API should return responses in JSON in an appropriate fashion.  Any request bodies should also be JSON.
Please use REST API best practices when applicable. 
- Report all files in directory responses, including hidden files.  You should report file name, owner, size, 
and permissions (read/write/execute - standard octal representation is acceptable).
  - You can assume that all files are text files of modest size (i.e., that can fit comfortably within a JSON blob).
- Clearly state all assumptions you make in your application. 
- Write as many unit tests as you can. We don’t expect 100% code coverage, but at least include a test script 
that gives a good example of your testing strategy.	
- Document your API. 
- Comment your code.
- Edit the README.md file for your repository fork to talk about the application you built. Feel free to remove instructions for building the app. 
If you do not have time to build a particular step in your application, we recommend writing about it in your README.md. 
- Enjoy yourself.
	
### Extra Credit
- Create PUT and DELETE endpoints to replace and delete directories and files as appropriate. Any request bodies should be JSON.

## Time Expectations
Please don’t spend more than 4 hours maximum on the entire exercise and let us know how long you spend on this exercise in the README.md file. If you have concerns about the time needed, please don’t hesitate to reach out with questions. Our goal is to understand enough about your coding strategy so you will be able to demonstrate some of your best practices when we next meet in person!

## How to submit your work

1. Visit https://github.com/weavegrid/wg-takehome-filesystem-crawler 
2. Create a copy of the repository in your own github account. Call it whatever you want but make sure it's private. We will not accept PR's against this repo as application submission.
3. When you're done with your work, your recruiter will give you the Github usernames of the engineers who will be reviewing your work so you can give them access to the repository.
 							
