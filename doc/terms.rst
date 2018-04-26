Terms
-----

CLIO
    the system described in these notes

Component
    a piece of software, usually a complete package.
    It can be Simple or Complex.

Simple Component
    a software component which does not include
    other components.
    For example, small libraries are usually Simple Components.

Complex Component
    a software component which includes
    (or has other Relationship) other components.
    Typical software is usually a Complex Component
    since it includes many Simple Components (e.g., libraries).
    Note that it is perfectly possible for a Complex Component
    to include other Complex Components.

Component Details
    the set of data pertaining to a Component.
    At minimum, these include name of the component and License (OBL).
    Other info usually present includes version, origin URL, etc.

Catalog
    the set of Simple Components (with their Component Details)
    that are used in the various Complex Components.

Software License
    the set of rights and obligations one must follow
    when using a software. In most of the cases, the license in CLIO
    will be denoted by a SPDX license expression.

Outbound License (OBL)
    the set of licenses a Component is licensed under

Inbound License (IBL)
    the license that a Component is licensed under
    when used in a Complex Component

Relationship
    a connection between two Software Components.
    The most basic relationship is INCLUDES, when a Component includes
    the code of another Component (possibly modified).
    There are many relationships defined in the SPDX Specification,
    although many of them apply to files and not Components
    and as such are not relevant.

