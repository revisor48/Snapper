# Snapper
A security tool for grabbing screenshots of many web hosts. This tool is useful after [DNS enumeration](https://github.com/mschwager/fierce) or after enumerating web hosts via nmap or nessus.

A sample output can be seen here: [https://security.love/Snapper/output](https://security.love/Snapper/output)

## How to install 


- Pypl package
```bash
pip install -i  https://test.pypi.org/simple/ snapper
```

- Install phantomJS (you need to have [npm installed](https://nodejs.org/en/download/package-manager/))
```bash
npm -g install phantomjs
```

## How to use

For a simple demo try:
```
snap -l "google.com, gmail.google.com,ads.google.com" -c 3 -p 8000
```
This kicks off 3 processes, each of which fetch screenshots of the http and https versions of the hosts in question. The output is served up via the given port, http://127.0.0.1:8000 by default
![output results](http://i.imgur.com/OlvyIBp.png)

You can also read from a file, these results where generated from a [fierce](https://github.com/mschwager/fierce) enumeration:
```
python snapper.py -f googleExample.txt -c 10 -v
```
You can view the results [here](https://security.love/Snapper/output). Note in addition to the server, the static files are available in your current working directory as "output"


## More options

```bash
python snapper.py --help
```

```
Options:
  -h, --help            show this help message and exit
  -f FILE, --file=FILE  Souce from input file
  -l LIST, --list=LIST  Source from commandline list
  -u USER_AGENT, --user-agent=USER_AGENT
                        The user agent used for requests
  -c NUMWORKERS, --concurrency=NUMWORKERS
                        Number of cuncurrent processes
  -t TIMEOUT, --timeout=TIMEOUT
                        Number of seconds to try to resolve
  -p PORT, --port=PORT  Port to run server on
  -v                    Display console output for fetching each host
```
