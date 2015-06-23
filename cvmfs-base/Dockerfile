##
## dahuo2013/cvmfs-base
## A container where CernVM-FS is up and running
##
FROM binet/slc-base
MAINTAINER Da Huo "dhuo@nd.edu"

USER root
ENV USER root
ENV HOME /root

## make sure FUSE can be enabled
RUN if [[ ! -e /dev/fuse ]]; then mknod -m 666 /dev/fuse c 10 229; fi

# install cvmfs repos
ADD etc-yum-cernvm.repo /etc/yum.repos.d/cernvm.repo

# Install rpms
RUN yum update -y && yum -y install \
    cvmfs cvmfs-init-scripts cvmfs-auto-setup \
    freetype fuse \
    man nano openssh-server openssl098e libXext libXpm

WORKDIR /root

## add files last (as this invalids caches)
ADD dot-pythonrc.py  $HOME/.pythonrc.py

ADD etc-cvmfs-default-local /etc/cvmfs/default.local
ADD etc-cvmfs-domain-local  /etc/cvmfs/domain.d/cern.ch.local

ADD run-cvmfs.sh /root/run-cvmfs.sh

RUN mkdir -p \
    /cvmfs/cernvm-prod.cern.ch \
    /cvmfs/sft.cern.ch \
    /cvmfs/grid.cern.ch \
    /cvmfs/cms.cern.ch

RUN echo "cernvm-prod.cern.ch /cvmfs/cernvm-prod.cern.ch cvmfs defaults 0 0" >> /etc/fstab && \
    echo "sft.cern.ch         /cvmfs/sft.cern.ch cvmfs defaults 0 0" >> /etc/fstab && \
    echo "grid.cern.ch       /cvmfs/grid.cern.ch cvmfs defaults 0 0" >> /etc/fstab && \
    echo "cms.cern.ch         /cvmfs/cms.cern.ch cvmfs defaults 0 0" >> /etc/fstab
    
RUN mv -v /etc/cvmfs/keys/*/* /etc/cvmfs/keys

ADD dot-bashrc              $HOME/.bashrc
## EOF
