# Remove bundled libraries from requirements/provides
%global __requires_exclude ^(libbass.*|libtreble)\\.so.*$
%global __provides_exclude_from ^%{_libdir}/%{name}/.*$

%global debug_package %{nil}
%define _build_id_links none

%global appstream_id com.plexamp.Plexamp

Name:           plexamp
Version:        4.50.19
Release:        2%{?dist}
Summary:        A beautiful Plex music player for audiophiles, curators, and hipsters
License:        https://www.plex.tv/about/privacy-legal/plex-terms-of-service
URL:            https://plexamp.com/
ExclusiveArch:  x86_64 aarch64

Source0:        https://plexamp.plex.tv/desktop/Plexamp-%{version}-x86_64.AppImage
Source1:        https://plexamp.plex.tv/desktop/Plexamp-%{version}-aarch64.AppImage
Source2:        https://raw.githubusercontent.com/flathub/%{appstream_id}/master/%{appstream_id}.metainfo.xml
Source10:       %{name}-wrapper

BuildRequires:  desktop-file-utils
BuildRequires:  libappstream-glib

%description
Plexamp is a small, highly opinionated music player for Plex Media Server.
A Plex Pass and Plex Media Server is required to use Plexamp.

%prep
%setup -q -c -T
chmod +x %{_sourcedir}/*.AppImage
%{_sourcedir}/Plexamp-%{version}-%{_arch}.AppImage --appimage-extract
mv squashfs-root/* .

%install
mkdir -p %{buildroot}%{_libdir}/%{name}/{bin,lib}
install -p -m 0755 usr/bin/Plexamp %{buildroot}%{_libdir}/%{name}/bin/
cp -a usr/lib/Plexamp usr/lib/plexamp %{buildroot}%{_libdir}/%{name}/lib/

# The copies in usr/lib have a clean RUNPATH, the ones in the plugin folder do not
for lib in libtreble.so libbass.so libbassmix.so libbass_fx.so libbassenc.so; do
    install -p -m 0755 usr/lib/$lib %{buildroot}%{_libdir}/%{name}/lib/
    ln -sf ../$lib %{buildroot}%{_libdir}/%{name}/lib/plexamp/$lib
done

mkdir -p %{buildroot}%{_bindir}
sed -e 's|INSTALL_DIR|%{_libdir}/%{name}|g' %{SOURCE10} > %{buildroot}%{_bindir}/%{name}
chmod 0755 %{buildroot}%{_bindir}/%{name}

# Desktop file
cp Plexamp.desktop %{appstream_id}.desktop
desktop-file-install \
    --dir %{buildroot}%{_datadir}/applications \
    --set-key=Exec --set-value="%{name} %%U" \
    --set-icon=%{appstream_id} \
    %{appstream_id}.desktop

# Icons
for size in 32x32 128x128 256x256@2; do
    install -D -p -m 0644 usr/share/icons/hicolor/$size/apps/Plexamp.png \
        %{buildroot}%{_datadir}/icons/hicolor/$size/apps/%{appstream_id}.png
done

# AppStream metadata
install -D -p -m 0644 %{SOURCE2} %{buildroot}%{_metainfodir}/%{appstream_id}.metainfo.xml

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/%{appstream_id}.desktop
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/%{appstream_id}.metainfo.xml

%files
%{_bindir}/%{name}
%{_datadir}/applications/%{appstream_id}.desktop
%{_datadir}/icons/hicolor/*/apps/%{appstream_id}.png
%{_libdir}/%{name}
%{_metainfodir}/%{appstream_id}.metainfo.xml

%changelog
* Fri Oct 09 2026 Simone Caronni <negativo17@gmail.com> - 4.50.19-2
- Fix Wayland protocol error with WebKitGTK on NVIDIA.

* Thu Oct 08 2026 Simone Caronni <negativo17@gmail.com> - 4.50.19-1
- Rebase on 4.50.19.
- New Tauri based application, use system WebKitGTK and add aarch64 support.

* Thu Oct 23 2025 Simone Caronni <negativo17@gmail.com> - 4.13.0-1
- First build.
