Ansible Role: Java with DCEVM
==================

Role to install the Java with DCEVM.

**Important:** since the 8.0.0 release of this role the Oracle JDK is no longer
supported, [AdoptOpenJDK](https://adoptopenjdk.net) is used for all Java
versions. Due to this, support for Java 7 has been discontinued.

Requirements
------------
 Tested with
* Ansible >= 2.9

* Linux Distribution
    * Ubuntu
        * Focal (20.04)
        * Note: other versions are likely to work but have not been tested.

Role Variables
--------------

The following variables will change the behavior of this role (default values
are shown below):

```yaml
# Java version number
# Specify '8', '11' to get the latest patch
# version of that release.
java_version: '11.0.7+1'

# Base installation directory for any Java distribution
java_install_dir: '/opt/java'

# Directory to store files downloaded for Java installation on the remote box
java_download_dir: "{{ x_ansible_download_dir | default(ansible_env.HOME + '/.ansible/tmp/downloads') }}"

# If this is the default installation, profile scripts will be written to set
# the JAVA_HOME environment variable and add the bin directory to the PATH
# environment variable.
java_is_default_installation: yes
```

Example Playbooks
-----------------

By default this role will install the latest LTS JDK version provided by
AdoptOpenJDK that has been tested and is known to work with this role:

```yaml
- hosts: servers
  roles:
    - role: ansible-role-java-dcevm
```

You can install a specific version of the JDK by specifying the `java_version`.

```yaml
- hosts: servers
  roles:
    - role: ansible-role-java-dcevm
      java_version: '8'
```

**Note:** with [curl](https://curl.haxx.se) and
[jq](https://stedolan.github.io/jq) you can view the available versions by
running the following command:

```bash
for i in 8 11; do (curl --silent http   "https://api.github.com/repos/TravaOpenJDK/trava-jdk-$i-dcevm/releases"\
   | jq --raw-output '.[].tag_name'); done
```

You can install the multiple versions of the JDK by using this role more than
once:

```yaml
- hosts: servers
  roles:
    - role: ansible-role-java
      java_version: '8'
      java_is_default_installation: no

    - role: ansible-role-java
      java_version: '11'
      java_is_default_installation: yes
```

Development & Testing
---------------------

This project uses [Molecule](http://molecule.readthedocs.io/) to aid in the
development and testing; the role is unit tested using
[Testinfra](http://testinfra.readthedocs.io/) and
[pytest](http://docs.pytest.org/).

To develop or test you'll need to have installed the following:

* Linux (e.g. [Ubuntu](http://www.ubuntu.com/))
* [Docker](https://www.docker.com/)
* [Python](https://www.python.org/) (including pip)
* [Ansible](https://www.ansible.com/)
* [Molecule](http://molecule.readthedocs.io/)

Because the above can be tricky to install, this project includes
[Molecule Wrapper](https://github.com/gantsign/molecule-wrapper). Molecule
Wrapper is a shell script that installs Molecule and it's dependencies (apart
from Linux) and then executes Molecule with the command you pass it.

To test this role using Molecule Wrapper run the following command from the
project root:

```bash
./moleculew test
```

Note: some of the dependencies need `sudo` permission to install.

License
-------

MIT

Author Information
------------------
Rabah Meradi

Thanks
-------------------
I would to thank John Freeman as this role is inspired by his role ansible-role-java

