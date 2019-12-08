require 'spec_helper'

describe command('which podman') do
  its(:stdout) { should match /podman$/ }
  its(:exit_status) { should eq 0 }
end

describe command('podman pull docker.io/hello-world') do
    its(:exit_status) { should eq 0 }
end

describe command('podman run hello-world') do
    its(:stdout) { should contain('Hello from Docker!')}
end