# .so is not a devel file here
%if %{_use_internal_dependency_generator}
%define __noautoprov 'devel\\(.*'
%define __noautoreq 'devel\\(.*'
%endif

%define major 1
%define libname %mklibname vdpau_va_gl %{major}

Summary:	VDPAU driver with OpenGL/VAAPI backend
Name:		libvdpau-va-gl
Version:	0.4.2
Release:	1
License:	GPLv3+
Group:		System/Libraries
Url:		https://github.com/i-rinat/libvdpau-va-gl
Source0:	https://github.com/i-rinat/libvdpau-va-gl/archive/v%{version}.tar.gz
Source1:	libvdpau-va-gl.rpmlintrc
BuildRequires:	cmake
BuildRequires:	pkgconfig(gl)
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(glu)
BuildRequires:	pkgconfig(libswscale)
BuildRequires:	pkgconfig(libva-glx)
BuildRequires:	pkgconfig(vdpau)
BuildRequires:	pkgconfig(x11)

%description
Many applications can use VDPAU to accelerate portions of the video decoding
process and video post-processing to the GPU video hardware. Unfortunately,
there is no such library for many graphic chipsets. Some applications also
support VA-API but many of them, including Adobe Flash Player, don't.

This library proposes a generic VDPAU library. It uses OpenGL under the hood
to accelerate drawing and scaling and VA-API (if available) to accelerate video
decoding.

#----------------------------------------------------------------------------

%package -n %{libname}
Summary:	VDPAU driver with OpenGL/VAAPI backend
Group:		System/Libraries
Provides:	%{name} = %{EVRD}

%description -n %{libname}
Many applications can use VDPAU to accelerate portions of the video decoding
process and video post-processing to the GPU video hardware. Unfortunately,
there is no such library for many graphic chipsets. Some applications also
support VA-API but many of them, including Adobe Flash Player, don't.

This library proposes a generic VDPAU library. It uses OpenGL under the hood
to accelerate drawing and scaling and VA-API (if available) to accelerate video
decoding.

%files -n %{libname}
%doc ChangeLog README.md
%{_libdir}/libvdpau_va_gl.so.%{major}*
%{_libdir}/libvdpau_va_gl.so
%{_libdir}/libvdpau_i965.so

#----------------------------------------------------------------------------

%prep
%setup -q
%autopatch -p1

%build
%cmake
%make

%install
%makeinstall_std -C build
# Add a symlink for libvdpau_i965.so: vdpau users look for it when
# using the Intel graphics drivers, but there is no Intel specific
# libvdpau implementation right now. So let's use one that works.
ln -s libvdpau_va_gl.so %{buildroot}%{_libdir}/libvdpau_i965.so
