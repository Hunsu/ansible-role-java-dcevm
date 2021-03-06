import os
import pytest

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


@pytest.mark.parametrize('command', [
    'java',
    'javac'
])
def test_java_tools(host, command):
    cmd = host.run('. /etc/profile && ' + command + ' -version')
    assert cmd.rc == 0
    assert '1.8.0_202b08' in cmd.stderr
    if command == 'java':
        assert "Dynamic Code Evolution" in cmd.stderr


@pytest.mark.parametrize('version_dir_pattern', [
    'dcevm8u202b08$'
])
def test_java_installed(host, version_dir_pattern):
    java_home = host.check_output('find %s | grep --color=never -E %s',
                                  '/opt/java/',
                                  version_dir_pattern)

    java_exe = host.file(java_home + '/bin/java')

    assert java_exe.exists
    assert java_exe.is_file
    assert java_exe.user == 'root'
    assert java_exe.group == 'root'
    assert oct(java_exe.mode) == '0o755'
