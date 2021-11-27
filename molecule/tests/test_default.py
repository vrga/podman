import os

import testinfra.utils.ansible_runner
from testinfra.host import Host

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
        os.environ['MOLECULE_INVENTORY_FILE']
).get_hosts('all')


def test_package_installed(host: Host):
    host.run_expect([0], 'whereis podman')


def test_assert_all_containers_are_stopped_and_removed(host: Host):
    with host.sudo():
        host.run_expect([0], 'podman container stop -a')
        host.run_expect([0], 'podman container prune -f')


def test_container_basics(host: Host):
    with host.sudo():
        host.run_expect([0], 'podman image pull docker.io/hello-world')
        run_hello_world = host.run_expect([0], 'podman run --rm hello-world')
        assert 'Hello from Docker!' in run_hello_world.stdout


def test_httpd_container(host: Host):
    with host.sudo():
        host.run_expect([0], 'podman image pull docker.io/httpd:latest')
        host.run_expect([0], 'podman container create --name httpd-test -p 127.0.0.1:8080:80 httpd:latest')  # noqa E501
        host.run_expect([0], 'podman container start httpd-test')
    host.run_expect([0], 'sleep 2')

    curl_works = host.run_expect([0], "curl 'http://127.0.0.1:8080/' 2>/dev/null")
    assert 'It works!' in curl_works.stdout

    with host.sudo():
        host.run_expect([0], 'podman container stop httpd-test')
        host.run_expect([0], 'podman container start httpd-test')
        host.run_expect([0], 'podman container stop httpd-test')
