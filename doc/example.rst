Example
-------

As an illustrative example, here are some data
that demonstrate the information handled by the system.

The Catalog contains two Simple Components::

        name: zlib
        license: Zlib
        version: 1.2.11
        origin: http://zlib.net
        URL: http://www.zlib.net/zlib-1.2.11.tar.gz

        name: xxHash
        license: BSD-2-Clause
        origin: http://www.xxhash.com/
        version: 0.6.2
        URL: https://github.com/Cyan4973/xxHash/archive/v0.6.2.tar.gz


There is also a Complex Component (example entry)::

        name: my_software
        license: BSD-3-Clause
        version: 0.1

which also has the following relationships::

        my_software INCLUDES zlib
        my_software STATICALLY_LINKS xxHash
        my_software DYNAMICALLY_LINKS libc


The system should be able to store, present, and manage this information
and provide a user-friendly way of entering and editing it.

[data about users and permissions are not shown in this example]
