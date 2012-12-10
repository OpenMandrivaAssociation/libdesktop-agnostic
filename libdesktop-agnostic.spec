%define major 0
%define libname %mklibname desktop-agnostic %{major}
%define develname %mklibname -d desktop-agnostic

Summary:	A desktop-agnostic library for GLib-based projects
Name:		libdesktop-agnostic
Version:	0.3.92
Release:	3
License:	GPLv2+
Group:		Development/Other
Url:		https://launchpad.net/libdesktop-agnostic
Source0:	%{name}-%{version}.tar.gz
BuildRequires:	intltool
BuildRequires:	vala-devel
BuildRequires:	python-devel
BuildRequires:	pkgconfig(gconf-2.0)
BuildRequires:	pkgconfig(gladeui-2.0)
BuildRequires:	pkgconfig(gobject-introspection-1.0)
BuildRequires:	pkgconfig(pygobject-2.0)
BuildRequires:	pkgconfig(pygtk-2.0)
Requires:	libdesktop-agnostic-vfs-gio
Requires:	libdesktop-agnostic-cfg-gconf
Requires:	libdesktop-agnostic-fdo-glib
Requires:	pygtk2
Conflicts:	%{_lib}desktop-agnostic0 < 0.3.92-3

%description
This library provides an extensible configuration API, a unified virtual file
system API, and a desktop item editor (all with pluggable backends) for
GLib-based projects. It is not tied to any one desktop environment, although
there are desktop-specific modules.

%package -n	%{libname}
Group:		System/Libraries
Summary:	%{name} library package
Requires:	%{name} >= %{version}

%description -n	%{libname}
This library provides an extensible configuration API, a unified virtual file
system API, and a desktop item editor (all with pluggable backends) for
GLib-based projects. It is not tied to any one desktop environment, although
there are desktop-specific modules.

%package -n %{develname}
Summary:	%{name} development files
Group:		Development/Other
Provides:	%{name}-devel = %{version}-%{release}
Requires:	%{name} = %{version}-%{release}

%description -n %{develname}
This package contains header files needed when building applications based on
%{name}.

%package	cfg-gconf
Summary:	GConf module for %{name}
Group:		Development/Other
Requires:	%{name} = %{version}-%{release}
Provides:	libdesktop-agnostic-cfg = %{version}-%{release}

%description	cfg-gconf
This package contains the GConf mdoule for %{name}.

%package	fdo-glib
Summary:	GLib desktop entry module for %{name}
Group:		Development/Other
Requires:	%{name} = %{version}-%{release}
Provides:	libdesktop-agnostic-fdo = %{version}-%{release}

%description	fdo-glib
This package contains the GLib desktop entry module for %{name}.

%package	vfs-gio
Summary:	GIO VFS module for %{name}
Group:		Development/Other
Requires:	%{name} = %{version}-%{release}

%description	vfs-gio
This package contains the GIO VFS module for %{name}.

%prep
%setup -q
sed -i s,"gladeui-1.0","gladeui-2.0",g data/*

%build
%define Werror_cflags %{nil}
%setup_compile_flags
export LINKFLAGS="%{ldflags}"
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
./waf  --nocache install --destdir=%{buildroot}

# fix .so permissions so that debuginfo can be extracted for the debug package
find %{buildroot}%{_libdir} -name *.so -exec chmod 755 {} \;

%find_lang %{name}

%files -f %{name}.lang
%doc COPYING COPYING.GPL-2
%{_sysconfdir}/xdg/%{name}/desktop-agnostic.ini
%{_bindir}/lda-desktop-entry-editor
%{_bindir}/lda-schema-to-gconf
%dir %{_libdir}/desktop-agnostic
%dir %{_libdir}/desktop-agnostic/modules
%{_libdir}/desktop-agnostic/modules/libda-cfg-type-color.so
%{_libdir}/desktop-agnostic/modules/libda-module-guesser.so
%{_datadir}/glade/catalogs/desktop-agnostic.xml
%{python_sitearch}/desktopagnostic/*.py
%{python_sitearch}/desktopagnostic/*.so

%files cfg-gconf
%{_libdir}/desktop-agnostic/modules/libda-cfg-gconf.so

%files fdo-glib
%{_libdir}/desktop-agnostic/modules/libda-fdo-glib.so

%files vfs-gio
%{_libdir}/desktop-agnostic/modules/libda-vfs-gio.so

%files -n %{libname}
%{_libdir}/%{name}*.so.%{major}*

%files -n %{develname}
%dir %{_includedir}/%{name}-1.0
%dir %{_includedir}/%{name}-1.0/%{name}
%{_includedir}/%{name}-1.0/%{name}/*.h
%{_libdir}/%{name}*.so
%{_libdir}/pkgconfig/desktop-agnostic.pc
%{_datadir}/pygtk/2.0/defs/*.defs
%{_datadir}/vala/vapi/*.vapi
%{_datadir}/vala/vapi/desktop-agnostic*.deps

