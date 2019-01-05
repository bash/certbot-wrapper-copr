%define debug_package %{nil}

Name: certbot-wrapper
Version: 0.1.0
Release: 1%{?dist}
Summary: A wrapper around certbot with some extras ✨
License: MIT
URL: https://github.com/bash/certbot-wrapper
%if 0%{?fedora} >= 24
ExclusiveArch: x86_64 i686 armv7hl
%else
ExclusiveArch: x86_64 aarch64
%endif
BuildRequires: cargo
%{?systemd_requires}
BuildRequires: systemd
Source0: https://github.com/bash/certbot-wrapper/archive/%{version}/certbot-wrapper-%{version}.tar.gz


%description
%{summary}.


%prep
{{{ git_dir_setup_macro }}}
%autosetup


%build
cargo build --release


%install
install -D -p -m 755 target/release/certbot-wrapper %{buildroot}%{_bindir}/certbot-wrapper
mkdir -p %{buildroot}%{_unitdir}
install -pm644 systemd-units/renew-certificates.service %{buildroot}%{_unitdir}
install -pm644 systemd-units/renew-certificates.timer %{buildroot}%{_unitdir}


%check
cargo test


%post
%systemd_post renew-certificates.service
%systemd_post renew-certificates.timer


%preun
%systemd_preun renew-certificates.service
%systemd_preun renew-certificates.timer


%postun
%systemd_postun_with_restart renew-certificates.service
%systemd_postun_with_restart renew-certificates.timer


%files
%license license.txt
%doc readme.md
%{_bindir}/certbot-wrapper
%{_unitdir}/renew-certificates.service
%{_unitdir}/renew-certificates.timer

# %changelog
# {{{ git_dir_changelog }}}
