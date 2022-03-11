Name: olefy
Version: 1.2.3
Release: 1%{?dist}
Summary: oletools verify over TCP socket

License: Apache
URL: http://github.com/NethServer/olefy
Source0: %{name}-%{version}.tar.gz

#
# Run pip download --no-deps -r requirements.txt to retrieve additional source packages
#
Source12: https://github.com/HeinleinSupport/olefy/archive/9a3d5780394b7a0126981f0115a110d69aad60a0/olefy.tar.gz
Source1: cffi-1.13.0.tar.gz
Source2: colorclass-2.2.0.tar.gz
Source3: cryptography-2.8.tar.gz
Source4: easygui-0.98.1.tar.gz
Source5: msoffcrypto-tool-4.10.1.tar.gz
Source6: olefile-0.46.zip
Source7: oletools-master.zip
Source8: pycparser-2.19.tar.gz
Source9: pyparsing-2.4.2.tar.gz
Source10: python-magic-0.4.15.tar.gz
Source11: six-1.12.0.tar.gz
Source13: pcodedmp-1.2.6.tar.gz

BuildRequires: python3
BuildRequires: python3-devel
BuildRequires: python3-pip
BuildRequires: libffi-devel
BuildRequires: openssl-devel

Requires: python3
Requires(postun): systemd

%description
This package ships the olefy (https://github.com/HeinleinSupport/olefy) TCP
server wrapper that checks files with oletools.

This package is built for NethServer 7 but could work on CentOS 7 too.

%prep
%setup -q
%setup -q -D -T -b 12

%install
tdir=$(mktemp -d)
chmod 755 ${tdir}
python3 -m venv --copies ${tdir}
rm -f ${tdir}/bin/activate*
${tdir}/bin/pip install \
    --pre --no-deps \
    %{S:1} %{S:2} %{S:3} %{S:4} %{S:5} %{S:6} \
    %{S:7} %{S:8} %{S:9} %{S:10} %{S:11} %{S:13}
${tdir}/bin/pip uninstall -y pip
mkdir -p %{buildroot}/opt
mv ${tdir} %{buildroot}/opt/olefy
install -D -m 0755 %{_builddir}/olefy-*/olefy.py %{buildroot}/opt/olefy/bin/olefy
install -D -m 0644 olefy.conf %{buildroot}/etc/opt/olefy/olefy.conf
install -D -m 0644 olefy.service %{buildroot}%{_unitdir}/olefy.service
find %{buildroot}/opt/olefy/bin -type f -executable -exec sed -i '1 s|^#!.*$|#!/opt/olefy/bin/python|' '{}' \;

%files
%defattr (-,root,root)
%license LICENSE
%license LICENSE-cffi
%license LICENSE-cryptography
%license LICENSE-msoffcrypto-tool
%license LICENSE-olefile
%license LICENSE-oletools
%license LICENSE-oletools-3rdp-DridexUrlDecoder
%license LICENSE-oletools-3rdp-xglob
%license LICENSE-oletools-3rdp-xxxswf
%license LICENSE-pycparser
%license LICENSE-pyparsing
%license LICENSE-python-magic
%license LICENSE-six
%license LICENSE-pcodedmp
%doc README.rst
/opt/olefy
%dir /etc/opt/olefy
%config(noreplace) %attr(0644,root,root) /etc/opt/olefy/olefy.conf
%{_unitdir}/olefy.service


%pre
# ensure olefy user exists:
if ! getent passwd olefy >/dev/null ; then
   useradd -r -U olefy
fi

%preun
%systemd_preun olefy.service

%postun
%systemd_postun_with_restart olefy.service

%changelog
* Wed Nov 04 2020 Davide Principi <davide.principi@nethesis.it> - 1.2.3-1
- Official Olefy 0.56 does not block macro virus - Bug NethServer/dev#6321

* Thu Oct 01 2020 Davide Principi <davide.principi@nethesis.it> - 1.2.1-1
- Bump oletools 0.56 -- NethServer/olefy@11d252f

* Wed Sep 23 2020 Davide Principi <davide.principi@nethesis.it> - 1.2.0-1
- Upstream Olefy and Oletools fixes for multiple issues - NethServer/dev#6271
- Bump oletools 0.56dev10 and olefy from master branch

* Wed Jan 15 2020 Davide Principi <davide.principi@nethesis.it> - 1.1.0-1
- Upgrade to oletools-0.55 -- NethServer/dev#5964

* Mon Dec 02 2019 Davide Principi <davide.principi@nethesis.it> - 1.0.1-1
- Olefy TCP port 10050 conflict - Bug NethServer/dev#5963

* Wed Nov 20 2019 Davide Principi <davide.principi@nethesis.it> - 1.0.0-1
- Scan MS Office files for bad macros - NethServer/dev#5891

* Tue Oct 22 2019 Davide Principi <davide.principi@nethesis.it>
- Initial release
