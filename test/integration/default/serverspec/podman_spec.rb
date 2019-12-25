require 'spec_helper'

describe command('which podman') do
  its(:stdout) { should match /podman$/ }
  its(:exit_status) { should eq 0 }
end

describe command('podman container exists hello-world') do
    its(:exit_status) { should eq 0 }
end

describe command('podman container exists hello-world-2') do
    its(:exit_status) { should eq 0 }
end

describe command('podman container exists httpd-test') do
    its(:exit_status) { should eq 0 }
end

describe command('podman container start httpd-test') do
    its(:exit_status) { should eq 0 }
end

describe command("curl 'http://localhost:8080/'") do
  its(:exit_status) { should eq 0 }
  its(:stdout) { should match 'It works!' }
end

describe command('podman container stop httpd-test') do
    its(:exit_status) { should eq 0 }
end

describe command('podman run --rm hello-world') do
    its(:stdout) { should contain('Hello from Docker!')}
end