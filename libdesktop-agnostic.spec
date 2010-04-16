%define major 0
%define libname %mklibname desktop-agnostic %major
%define develname %mklibname -d desktop-agnostic

Summary:	A desktop-agnostic library for GLib-based projects
Name:		libdesktop-agnostic
Version:	0.3.90
Release:	%mkrel 5
Url:		https://launchpad.net/libdesktop-agnostic
Source0:	%{name}-%{version}.tar.gz
License:	GPLv2+
Group:		Development/Other
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:	libvala-devel >= 0.7.7
BuildRequires:	libgladeui-devel
BuildRequires:	python-devel
BuildRequires:	libGConf2-devel
BuildRequires:	gobject-introspection-devel >= 0.6.3
BuildRequires:	python-gobject-devel
BuildRequires:  pygtk2.0-devel
#BuildRequires:	glib2-devel
#BuildRequires:	libgtk+2-devel
#BuildRequires:	python-gobject-devel
#BuildRequires:	gnome-desktop-devel
#BuildRequires:	gnome-vfs2-devel
#BuildRequires:	thunar-devel
Requires:	libdesktop-agnostic-vfs-gio
Requires:	libdesktop-agnostic-cfg-gconf
Requires:	libdesktop-agnostic-fdo-glib
Requires:	pygtk2

%description
This library provides an extensible configuration API, a unified virtual file
system API, and a desktop item editor (all with pluggable backends) for
GLib-based projects. It is not tied to any one desktop environment, although
there are desktop-specific modules.

%package -n	%libname
Group:		Development/Other
Summary:	%{name} library package
Requires:	%{name} >= %{version}

%description -n	%libname
%summary.

%package -n %develname
Summary:	%{name} development files
Group:		Development/Other
Provides:	%{name}-devel = %{version}-%{release}
Requires:	%{name} = %{version}-%{release}

%description -n %develname
This package contains header files needed when building applications based on
%{name}.

%package	cfg-gconf
Summary:	GConf module for %{name}
Group:		Development/Other
Requires:	%{name} = %{version}-%{release}
Provides:	libdesktop-agnostic-cfg

%description	cfg-gconf
This package contains the GConf mdoule for %{name}.

#%package	cfg-keyfile
#Summary:	GLib GKeyFile module for %{name}
#Group:		Development/Other
#Requires:	%{name} = %{version}-%{release}
#Provides:	libdesktop-agnostic-cfg

#%description	cfg-keyfile
#This package contains the GLib GKeyFile module for %{name}.

%package	fdo-glib
Summary:	GLib desktop entry module for %{name}
Group:		Development/Other
Requires:	%{name} = %{version}-%{release}
Provides:	libdesktop-agnostic-fdo

%description	fdo-glib
This package contains the GLib desktop entry module for %{name}.

#%package	fdo-gnome
#Summary:	GNOME-based desktop entry module for %{name}
#Group:		Development/Other
#Requires:	%{name} = %{version}-%{release}
#Provides:	libdesktop-agnostic-fdo
#
#%description	fdo-gnome
#This package contains the GNOME-based desktop entry module for %{name}.
#
%package	vfs-gio
Summary:	GIO VFS module for %{name}
Group:		Development/Other
Requires:	%{name} = %{version}-%{release}

%description	vfs-gio
This package contains the GIO VFS module for %{name}.

#%package	vfs-gnome
#Summary:	GNOME VFS module for %{name}
#Group:		Development/Other
#Requires:	%{name} = %{version}-%{release}
#Provides:	libdesktop-agnostic-vfs
#
#%description	vfs-gnome
#This package contains the GNOME VFS module for %{name}.
#
#%package	vfs-thunar
#Summary:	Thunar VFS module for %{name}
#Group:		Development/Other
#Requires:	%{name} = %{version}-%{release}
#Provides:	libdesktop-agnostic-vfs
#
#%description	vfs-thunar
#This package contains the Thunar VFS module for %{name}.
#

%prep
%setup -q

%build
%define Werror_cflags %nil 
%setup_compile_flags
export PYTHONDIR=%{python_sitearch}
./waf configure \
	--prefix=%{_prefix} \
	--sysconfdir=%{_sysconfdir} \
	--localstatedir=%{_localstatedir} \
	--libdir=%{_libdir} \
	--mandir=%{_mandir} \
	--enable-debug \
	--config-backends=gconf \
	--vfs-backends=gio \
	--desktop-entry-backends=glib \
	--with-glade

./waf build --nocache

%install
rm -rf %{buildroot}
./waf  --nocache install --destdir=%{buildroot}

# fix .so permissions so that debuginfo can be extracted for the debug package
find %{buildroot}%{_libdir} -name *.so -exec chmod 755 {} \;

# install man pages
mkdir -p %{buildroot}%{_mandir}/man1
install -m 644 debian/lda*1 %{buildroot}%{_mandir}/man1

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc COPYING COPYING.GPL-2
%{_sysconfdir}/xdg/%{name}/desktop-agnostic.ini
%{_bindir}/lda-desktop-entry-editor
%{_bindir}/lda-schema-to-gconf
%dir %{_libdir}/desktop-agnostic
%{_libdir}/desktop-agnostic/modules/libda-cfg-type-color.so
%{_libdir}/desktop-agnostic/modules/libda-module-guesser.so
%{_datadir}/glade3/catalogs/desktop-agnostic.xml
%{_mandir}/man1/lda-*1.*
%{python_sitearch}/desktopagnostic/*.py

%files cfg-gconf
%defattr(-,root,root)
%{_libdir}/desktop-agnostic/modules/libda-cfg-gconf.so

#%files cfg-keyfile
#%defattr(-,root,root)
#%{_libdir}/desktop-agnostic/modules/libda-cfg-keyfile.so

%files fdo-glib
%defattr(-,root,root)
%{_libdir}/desktop-agnostic/modules/libda-fdo-glib.so

#%files fdo-gnome
#%defattr(-,root,root)
#%{_libdir}/desktop-agnostic/modules/libda-fdo-gnome.so

%files vfs-gio
%defattr(-,root,root)
%{_libdir}/desktop-agnostic/modules/libda-vfs-gio.so

#%files vfs-gnome
#%defattr(-,root,root)
#%{_libdir}/desktop-agnostic/modules/libda-vfs-gnome-vfs.so
#
#%files vfs-thunar
#%defattr(-,root,root)
#%{_libdir}/desktop-agnostic/modules/libda-vfs-thunar-vfs.so

%files -n %libname
%defattr(-,root,root)
%{_libdir}/%{name}*.so.%{major}*
%{_libdir}/girepository-1.0/*.typelib
%{python_sitearch}/desktopagnostic/*.so

%files -n %develname
%defattr(-,root,root)
%dir %{_includedir}/%{name}-1.0
%dir %{_includedir}/%{name}-1.0/%{name}
%{_includedir}/%{name}-1.0/%{name}/*.h
%{_libdir}/%{name}*.so
%{_libdir}/pkgconfig/desktop-agnostic.pc
%{_datadir}/gir-1.0/*.gir
%{_datadir}/pygtk/2.0/defs/*.defs
%{_datadir}/vala/vapi/*.vapi
%{_datadir}/vala/vapi/desktop-agnostic*.deps
