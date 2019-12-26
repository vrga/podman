import os

import testinfra.utils.ansible_runner
from testinfra.host import Host
from requests import get
from pprint import pprint

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']
).get_hosts('all')


def test_package_installed(host: Host):
    podman = host.package('podman')
    assert podman.is_installed
    assert podman.version.startswith('1.6')


def test_container_basics(host: Host):
    with host.sudo():
        host.run_expect([0], 'podman container exists hello-world')
        host.run_expect([0], 'podman container exists hello-world-2')
        host.run_expect([0], 'podman container exists httpd-test')

        run_hello_world = host.run_expect([0], 'podman run --rm hello-world')
        assert 'Hello from Docker!' in run_hello_world.stdout


def test_httpd_container(host: Host):
    with host.sudo():
        host.run_expect([0], 'podman container start httpd-test')

    curl_works = host.run_expect([0], "curl 'http://localhost:8080/'")
    assert 'It works!' in curl_works.stdout

    with host.sudo():
        host.run_expect([0], 'podman container stop httpd-test')
        host.run_expect([0], 'podman container start httpd-test')
        host.run_expect([0], 'podman container stop httpd-test')
