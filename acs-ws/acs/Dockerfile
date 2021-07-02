FROM centos:centos8.2.2004

ARG USER_NAME
ARG GROUP_NAME
ARG USER_ID
ARG GROUP_ID

#General packages
RUN dnf -y install vim redhat-lsb-core sudo dbus-x11 rsync dnf-plugins-core glibc-locale-source glibc-langpack-en
RUN dnf config-manager --set-enabled PowerTools

#Install Git and Git LFS
RUN dnf -y install epel-release
RUN dnf -y install https://download1.rpmfusion.org/free/el/rpmfusion-free-release-8.noarch.rpm
RUN dnf -y install git
RUN curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.rpm.sh | bash
RUN dnf -y install git-lfs

#Install Java 11
RUN dnf -y install java-11-openjdk-devel

#Prepare for Java
RUN mkdir -p /usr/java
RUN ln -s /usr/lib/jvm/java-openjdk /usr/java/default

#Install ACS required packages
RUN dnf -y install ksh gcc gcc-c++ gcc-gfortran libX11-devel libffi-devel perl readline-devel bzip2 bzip2-devel openssl-devel openldap-devel libxml2-devel freetype-devel libxslt-devel sqlite-devel expat-devel tcl-devel tk-devel bison flex autoconf unzip dos2unix procmail cppunit-devel doxygen graphviz

#Debugging Tools
RUN dnf -y install gdb net-tools valgrind
RUN yum -y install tree meld

RUN mkdir /scripts
#COPY cloneRepo.sh /scripts
COPY acs.env /scripts
COPY buildExtProds.sh /scripts
COPY buildACS.sh /scripts

#User configuration
RUN groupadd -r -g ${GROUP_ID} ${GROUP_NAME}
RUN useradd -r -m -u ${USER_ID} -g ${GROUP_NAME} ${USER_NAME}
RUN groupadd sudo
RUN usermod -aG sudo ${USER_NAME}
RUN echo new2me |passwd ${USER_NAME} --stdin
RUN echo "%sudo	ALL=(ALL)	ALL" >> /etc/sudoers
RUN echo "%sudo	ALL=(ALL)	NOPASSWD: ALL" >> /etc/sudoers
USER ${USER_NAME}
WORKDIR /home/${USER_NAME}
