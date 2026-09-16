## Installation
 
Download the OpenShift cli [here](https://docs.redhat.com/en/documentation/openshift_container_platform/4.8/html/installing/index)[cite: 1]

Download stern [here](https://github.com/stern/stern)[cite: 1]

## Commands list
<blockquote style="color: #c00;"> 
    <u>Parameters inside unordered lists don't have a specific order</u>
</blockquote>[cite: 1]
<blockquote style="color: #c00;"> 
    <u>Parameters inside ordered lists must follow the given order</u>
</blockquote>[cite: 1]
<table style="font-size: 1rem;">
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
                <code>help</code>, <code>manuel</code>, <code>manuel!</code>
            </td>
            <td>
                <small>
                    <ul>
                        <li>command (optional)</li>
                    </ul>
                </small>
            </td>
            <td>
                <code>help logs</code>
            </td>
            <td>
                <p>
                    <small>
                        Displays details about this program or usage of a specified command.
                    </small>
                </p>
            </td>
        </tr>
        <tr>
            <td>
                <code>clear</code>, <code>cls</code>
            </td>
            <td>
                <br/>
            </td>
            <td>
                <code>clear</code>
            </td>
            <td>
                <p>
                    <small>
                        Clears the terminal screen.
                    </small>
                </p>
            </td>
        </tr>
        <tr>
            <td>
                <code>purge</code>
            </td>
            <td>
                <small>
                    <ol>
                        <li>history | note</li>
                        <li>note-name (required for note)</li>
                    </ol>
                </small>
            </td>
            <td>
                <code>purge history</code><br/>
                <code>purge note my_note.txt</code>
            </td>
            <td>
                <p>
                    <small>
                        Deletes command history or removes a specific note file.
                    </small>
                </p>
            </td>
        </tr>
        <tr>
            <td>
                <code>reload</code>, <code>reload-config</code>, <code>reload-conf</code>, <code>reload-env</code>
            </td>
            <td>
                <br/>
            </td>
            <td>
                <code>reload</code>
            </td>
            <td>
                <p>
                    <small>
                        Reloads the configuration file and environment settings.
                    </small>
                </p>
            </td>
        </tr>
        <tr>
            <td>
                <code>show</code>
            </td>
            <td>
                <small>
                    <ol>
                        <li>config | notes</li>
                        <li>sub-parameters (optional)</li>
                    </ol>
                </small>
            </td>
            <td>
                <code>show config all</code><br/>
                <code>show notes</code>
            </td>
            <td>
                <p>
                    <small>
                        Displays connection configuration or lists saved notes.
                    </small>
                </p>
            </td>
        </tr>
        <tr>
            <td>
                <code>set</code>
            </td>
            <td>
                <small>
                    <ol>
                        <li>host | credentials | username | password | namespace | env</li>
                        <li>value(s)</li>
                    </ol>
                </small>
            </td>
            <td>
                <code>set host 0</code><br/>
                <code>set credentials user pass</code><br/>
                <code>set namespace my-project</code>
            </td>
            <td>
                <p>
                    <small>
                        Updates configuration values. Setting host by index triggers auto-relogin.
                    </small>
                </p>
            </td>
        </tr>
        <tr>
            <td>
                <code>add</code>
            </td>
            <td>
                <small>
                    <ol>
                        <li>new</li>
                        <li>host | note</li>
                        <li>value / file-name (optional for note)</li>
                    </ol>
                </small>
            </td>
            <td>
                <code>add new host domain.com</code><br/>
                <code>add new note my_note.txt</code>
            </td>
            <td>
                <p>
                    <small>
                        Adds a new host or creates/edits a note using <code>nano</code>.
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
                        <li>via web</li>
                        <li>with [host] [username] [password] [token]</li>
                    </ul>
                </small>
            </td>
            <td>
                <code>login via web</code><br/>
                <code>login with host domain.com username admin</code>
            </td>
            <td>
                <p>
                    <small>
                        Log into OpenShift using config credentials, key-value pairs, or web flow.
                    </small>
                </p>
            </td>
        </tr>
        <tr>
            <td>
                <code>logout</code>, <code>exit</code>
            </td>
            <td>
                <br/>
            </td>
            <td>
                <code>logout</code>
            </td>
            <td>
                <p>
                    <small>
                        Logs out from OpenShift. <code>exit</code> terminates the shell session.
                    </small>
                </p>
            </td>
        </tr>
        <tr>
            <td>
                <code>status</code>
            </td>
            <td>
                <br/>
            </td>
            <td>
                <code>status</code>
            </td>
            <td>
                <p>
                    <small>
                        Displays current OpenShift connection and cluster status.
                    </small>
                </p>
            </td>
        </tr>
        <tr>
            <td>
                <code>envs</code>, <code>envs?</code>, <code>namespaces</code>
            </td>
            <td>
                <br/>
            </td>
            <td>
                <code>namespaces</code>
            </td>
            <td>
                <p>
                    <small>
                        Lists all available namespaces/projects.
                    </small>
                </p>
            </td>
        </tr>
        <tr>
            <td>
                <code>ls</code>, <code>pods</code>
            </td>
            <td>
                <br/>
            </td>
            <td>
                <code>pods</code>
            </td>
            <td>
                <p>
                    <small>
                        Lists all pods in the current namespace.
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
                        <li>pod-name (partial)</li>
                    </ul>
                </small>
            </td>
            <td>
                <code>find web-app</code>
            </td>
            <td>
                <p>
                    <small>
                        Searches and displays matching pod names.
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
                        <li>pod-name (full or partial)</li>
                    </ul>
                </small>
            </td>
            <td>
                <code>enter my-pod</code>
            </td>
            <td>
                <p>
                    <small>
                        Starts an interactive shell session inside the requested pod.
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
                        <li>pod-name</li>
                        <li>--since | -T {time}</li>
                        <li>--debug | -D</li>
                        <li>--save-logs | > [file]</li>
                        <li>--search | -F {filter1} {filter2...}</li>
                    </ol>
                </small>
            </td>
            <td>
                <code>logs app --since 1h --search error fail</code>
            </td>
            <td>
                <p>
                    <small>
                        Streams pod logs via stern. Supports time filtering, log saving, and multi-keyword filtering.
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
                    <p>Method 1: {src} {dest}</p>
                    <p>Method 2: {pod} {src} {dest}</p>
                </small>
            </td>
            <td>
                <code>upload file.txt /tmp/</code><br/>
                <code>upload my-pod file.txt /tmp/</code>
            </td>
            <td>
                <p>
                    <small>
                        Uploads a file to a pod. Defaults to last accessed pod if omitted.
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
                    <p>Method 1: {src} {dest} [--except/--exclude {paths}]</p>
                    <p>Method 2: {pod} {src} {dest} [--except/--exclude {paths}]</p>
                </small>
            </td>
            <td>
                <code>download /var/logs . --except *.tmp</code><br/>
                <code>download my-pod /var/logs . --exclude cache/</code>
            </td>
            <td>
                <p>
                    <small>
                        Downloads files from a pod via <code>oc rsync</code> with exclusion patterns support.
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
                        <li>pod1:src</li>
                        <li>pod2:dest</li>
                    </ol>
                </small>
            </td>
            <td>
                <code>upload-pod2pod app1:/data.db app2:/tmp/</code>
            </td>
            <td>
                <p>
                    <small>
                        Transfers files directly from one pod to another using local temp staging.
                    </small>
                </p>
            </td>
        </tr>
    </tbody>
</table>