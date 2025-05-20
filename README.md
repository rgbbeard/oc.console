
## Installation

Install openshift cli [here](https://docs.openshift.com/container-platform/4.8/cli_reference/openshift_cli/getting-started-cli.html)

Install stern [here](https://github.com/stern/stern)

Install oc.console

```
sudo chmod +x install.sh
sudo ./install.sh
```

## Commands list
<blockquote style="color: #f00;"> 
    Parameters inside unordered lists don't have a specific order
</blockquote>
<blockquote style="color: #f00;"> 
    Parameters inside ordered lists must follow the given order
</blockquote>
<table style="font-size: 0.9em;">
    <thead>
        <tr>
            <th>Command</th>
            <th>Parameters</th>
            <th>Example</th>
            <th>Description</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>
                <code>help</code>
            </td>
            <td>
                <small>
                    <ul>
                        <li>
                            command (optional)
                        </li>
                    </ul>
                </small>
            </td>
            <td>
                <code>help {command}</code>
            </td>
            <td>
                <p>
                    <small>
                        Displays details about this program; Displays details and usage of a specified command
                    </small>
                </p>
            </td>
        </tr>
        <tr>
            <td>
                <code>manuel</code>
            </td>
            <td>
                <small>
                    <ul>
                        <li>
                            command (optional)
                        </li>
                    </ul>
                </small>
            </td>
            <td>
                <code>manuel {command}</code>
            </td>
            <td>
                <p>
                    <small>
                        Alias of help
                    </small>
                </p>
            </td>
        </tr>
        <tr>
            <td>
                <code>manuel!</code>
            </td>
            <td>
                <small>
                    <ul>
                        <li>
                            command (optional)
                        </li>
                    </ul>
                </small>
            </td>
            <td>
                <code>manuel! {command}</code>
            </td>
            <td>
                <p>
                    <small>
                        Alias of help
                    </small>
                </p>
            </td>
        </tr>
        <tr>
            <td>
                <code>login</code>
            </td>
            <td>
                <small>
                    <ul>
                        <li>
                            command (optional)
                        </li>
                    </ul>
                </small>
            </td>
            <td>
                <code>login</code>
            </td>
            <td>
                <p>
                    <small>
                        Log into OpenShift using your credentials.
                        <br/>
                        A <b>.host</b> file with the host address is required, use <code>set-host</code> to create it.
                    </small>
                </p>
            </td>
        </tr>
        <tr>
            <td>
                <code>set-credentials</code>
            </td>
            <td>
                <small>
                    <ul>
                        <li>
                            /path/to/credentials.txt
                        </li>
                    </ul>
                </small>
            </td>
            <td>
                <code>set-credentials credentials.txt</code>
            </td>
            <td>
                <p>
                    <small>
                        Save your login credentials.
                        <br/>
                        This command requires the path to the file containing the login credentials.
                        <br/>
                        The file should contain only the username and password, each on a separate line
                    </small>
                </p>
            </td>
        </tr>
        <tr>
            <td>
                <code>set-credentials-path</code>
            </td>
            <td>
                <small>
                    <ul>
                        <li>
                            /path/to/credentials.txt
                        </li>
                    </ul>
                </small>
            </td>
            <td>
                <code>set-credentials-path credentials.txt</code>
            </td>
            <td>
                <p>
                    <small>
                        Alias of set-credentials
                    </small>
                </p>
            </td>
        </tr>
        <tr>
            <td>
                <code>set-host</code>
            </td>
            <td>
                <small>
                    <ul>
                        <li>
                            host
                        </li>
                    </ul>
                </small>
            </td>
            <td>
                <code>set-host http(s)://domain.example</code>
            </td>
            <td>
                <p>
                    <small>
                        Save the host to login to
                    </small>
                </p>
            </td>
        </tr>
        <tr>
            <td>
                <code>currhost</code>
            </td>
            <td>
                <br/>
            </td>
            <td>
                <code>currhost</code>
            </td>
            <td>
                <p>
                    <small>
                        Displays the host that's currently in use
                    </small>
                </p>
            </td>
        </tr>
        <tr>
            <td>
                <code>host?</code>
            </td>
            <td>
                <br/>
            </td>
            <td>
                <code>host?</code>
            </td>
            <td>
                <p>
                    <small>
                        Alias of currhost
                    </small>
                </p>
            </td>
        </tr>
        <tr>
            <td>
                <code>host</code>
            </td>
            <td>
                <br/>
            </td>
            <td>
                <code>host</code>
            </td>
            <td>
                <p>
                    <small>
                        Alias of currhost
                    </small>
                </p>
            </td>
        </tr>
        <tr>
            <td>
                <code>find</code>
            </td>
            <td>
                <small>
                    <ul>
                        <li>
                            {pod name} or {partial pod name}
                        </li>
                    </ul>
                </small>
            </td>
            <td>
                <code>find pod-name</code>
                <br/>
                <br/>
                <code>find partial-pod-name</code>
            </td>
            <td>
                <p>
                    <small>
                        Find a pod
                    </small>
                </p>
            </td>
        </tr>
        <tr>
            <td>
                <code>ls</code>
            </td>
            <td>
                <small>
                    <ul>
                        <li>
                            {pod name} or {partial pod name}
                        </li>
                    </ul>
                </small>
            </td>
            <td>
                <code>find pod-name</code>
                <br/>
                <br/>
                <code>find partial-pod-name</code>
            </td>
            <td>
                <p>
                    <small>
                        Alias of find
                    </small>
                </p>
            </td>
        </tr>
        <tr>
            <td>
                <code>logs</code>
            </td>
            <td>
                <small>
                    <ol>
                        <li>
                            {pod name} or {partial pod name}
                        </li>
                        <li>
                            --debug (optional)
                        </li>
                        <li>
                            --save-logs (optional, <b>currently disabled</b>)
                        </li>
                        <li>
                            --since (optional) hoursminutesseconds
                            <br/>
                            (default 30m)
                        </li>
                        <li>
                            --search (optional) space separated filters
                            <br/>
                            (must be used at the end of all the options)
                        </li>
                    </ol>
                </small>
            </td>
            <td>
                <code>logs pod-name</code>
                <br/>
                <br/>
                <code>logs partial-pod-name</code>
                <br/>
                <br/>
                <code>logs pod-name --since 1h2m3s</code>
                <br/>
                <br/>
                <code>logs pod-name --since 1h2m3s --search filters....</code>
                <br/>
                <br/>
                <code>logs pod-name --search filters....</code>
            </td>
            <td>
                <p>
                    <small>
                        Displays the logs for the requested pod
                    </small>
                </p>
            </td>
        </tr>
        <tr>
            <td>
                <code>enter</code>
            </td>
            <td>
                <small>
                    <ul>
                        <li>
                            pod-name
                        </li>
                    </ul>
                </small>
            </td>
            <td>
                <code>enter pod-name</code>
            </td>
            <td>
                <p>
                    <small>
                        Enters the pod's console.
                        <br/>
                        The accessed pod is saved inside the <b>.currpod</b> file
                    </small>
                </p>
            </td>
        </tr>
        <tr>
            <td>
                <code>envs</code>
            </td>
            <td>
                <br/>
            </td>
            <td>
                <code>envs</code>
            </td>
            <td>
                <p>
                    <small>
                        List all the available projects (<b>oc projects</b> or <b>login</b>)
                    </small>
                </p>
            </td>
        </tr>
        <tr>
            <td>
                <code>use-env</code>
            </td>
            <td>
                <small>
                    <ul>
                        <li>
                            project-name
                        </li>
                    </ul>
                </small>
            </td>
            <td>
                <code>use-env project-name</code>
            </td>
            <td>
                <p>
                    <small>
                        Switches to the requested project.
                        <br/>
                        If it has <b>dev</b> or <b>prod</b> at the end of its name, automatically determines the work environment
                    </small>
                </p>
            </td>
        </tr>
        <tr>
            <td>
                <code>currenv</code>
            </td>
            <td>
                <br/>
            </td>
            <td>
                <code>currenv</code>
            </td>
            <td>
                <p>
                    <small>
                        Displays the current work environment
                    </small>
                </p>
            </td>
        </tr>
        <tr>
            <td>
                <code>env?</code>
            </td>
            <td>
                <br/>
            </td>
            <td>
                <code>env?</code>
            </td>
            <td>
                <p>
                    <small>
                        Alias of currenv
                    </small>
                </p>
            </td>
        </tr>
        <tr>
            <td>
                <code>env</code>
            </td>
            <td>
                <br/>
            </td>
            <td>
                <code>env</code>
            </td>
            <td>
                <p>
                    <small>
                        Alias of currenv
                    </small>
                </p>
            </td>
        </tr>
        <tr>
            <td>
                <code>upload</code>
            </td>
            <td>
                <small>
                    <h6>Method1</h6>
                    <ol>
                        <li>
                            /path/to/source/file
                        </li>
                        <li>
                            /path/to/destination/folder (<b>inside the pod</b>)
                        </li>
                    </ol>
                    <br/>
                    <h6>Method2</h6>
                    <ol>
                        <li>
                            pod-name
                        </li>
                        <li>
                            /path/to/source/file
                        </li>
                        <li>
                            /path/to/destination/folder (<b>inside the pod</b>)
                        </li>
                    </ol>
                </small>
            </td>
            <td>
                <code>upload /path/to/source/file /path/to/destination/folder</code>
            </td>
            <td>
                <p>
                    <small>
                        Uploads a file to the selected location inside a pod.
                        <br/>
                        If no pod is specified, it looks into the <b>.currpod</b> file for the last accessed pod (see <code>enter</code> command).
                    </small>
                </p>
            </td>
        </tr>
        <tr>
            <td>
                <code>download</code>
            </td>
            <td>
                <small>
                    <h6>Method1</h6>
                    <ol>
                        <li>
                            /path/to/source/file (<b>inside the pod</b>)
                        </li>
                        <li>
                            /path/to/destination/folder
                        </li>
                    </ol>
                    <br/>
                    <h6>Method2</h6>
                    <ol>
                        <li>
                            pod-name
                        </li>
                        <li>
                            /path/to/source/file (<b>inside the pod</b>)
                        </li>
                        <li>
                            /path/to/destination/folder
                        </li>
                    </ol>
                </small>
            </td>
            <td>
                <code>download /path/to/source/file /path/to/destination/folder</code>
            </td>
            <td>
                <p>
                    <small>
                        Downloads a file from the selected location inside a pod.
                        <br/>
                        If no pod is specified, it looks into the <b>.currpod</b> file for the last accessed pod (see <code>enter</code> command).
                    </small>
                </p>
            </td>
        </tr>
        <tr>
            <td>
                <code>upload-pod2pod</code>
            </td>
            <td>
                <small>
                    <ol>
                        <li>
                            pod-name1:/path/to/source/file
                        </li>
                        <li>
                            pod-name2:/path/to/destination/folder
                        </li>
                    </ol>
                </small>
            </td>
            <td>
                <code>upload-pod2pod pod-name1:/path/to/source/file pod-name2:/path/to/destination/folder</code>
            </td>
            <td>
                <p>
                    <small>
                        Copies a file from a pod to another
                    </small>
                </p>
            </td>
        </tr>
    </tbody>
</table>