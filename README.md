
## Installation

Install openshift cli [here](https://docs.openshift.com/container-platform/4.8/cli_reference/openshift_cli/getting-started-cli.html)

Install stern [here](https://github.com/stern/stern)

Install oc.console

```bash
sudo chmod +x install.sh
sudo ./install.sh
```

## Documentation
  - #### help: Interactive console interface for easier use of the OpenShift Client.
    For more details use: help {COMMAND}
- #### login: Log in to the OpenShift Client using your credentials. 
    A host file with the host address is required.
    Use set-host 
- #### set-credentials: Save your login credentials.
    This command requires the path to the file containing the login credentials.
    The file should contain only the username and password, each on a separate line.
    ###### Usage:
      set-credentials {PATH}
- #### set-host: Save the host to login to.
    ###### Usage:
      set-host http://host.example
- #### currhost: Show the host that's currently in use.
- #### host?: Alias of currhost
- #### host: Alias of currhost
- #### set-credentials-path: Alias of set-credentials
- #### find: Locate a POD.
- #### ls: Alias of find
- #### logs: Shows the POD logs in real time.
    ###### Usage:
      logs {POD} --since {TIME}
- #### enter: Access a POD.
    You can specify the POD you want to enter, or if no name is provided, the last accessed POD will be used.
    ###### Usage:
      enter {POD}
- #### use-env: Switch between work environments.
    ###### Usage:
      use-env {ENVIRONMENT}
- #### currenv: Show the current working environment
- #### env?: Alias of currenv
- #### env: Alias of currenv
- #### upload: Upload a file to a specified POD.
    ###### Usage:
      --pod {POD} or default (uses the last accessed POD)
      --from {path/to/file}, the path to the file you want to upload
      --to {path/to/destination}, the destination path in the POD
    ###### Example:
      upload --pod default --from /path/to/somefile.pdf --to /path/to/destination
- #### download: Download a file from a specified POD.
    ###### Usage:
      --pod {POD} or default (uses the last accessed POD)
      --from {path/to/file}, the path to the file in the POD
      --to {path/to/destination}, the local destination path for the downloaded file
    ###### Example:
      download --pod default --from /path/to/somefile.pdf --to ~/Downloads

## Features

- #### upload-pod2pod: allows you to transfer files from a pod to another
