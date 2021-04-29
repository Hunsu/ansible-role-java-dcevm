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
    if command == 'java':
        assert '11.0.10' in cmd.stderr
        assert "Dynamic Code Evolution" in cmd.stderr
    else:
        assert '11.0.10' in cmd.stdout


@pytest.mark.parametrize('version_dir_pattern', [
    'dcevm-[0-9\\.\\+]+$'
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
