.. _repository:

Repository Manager
==================

This is a repository structure:

::

    my_repo
    ├── .repo_root
    └── stable
        ├── Packages.json
        ├── noarch
        │   └── nodist
        │       └── novers
        │           ├── hello_hell.tar
        │           ├── hello_world.tar
        │           └── test_deps.tar
        └── x86_64
            └── debian
                └── 6
                    ├── hello_hell2.tar
                    ├── hello_world2.tar
                    └── test_deps2.tar

And this how to create your own repository:

::

    ubik-repo create my_repo
     :: Create repository structure
     :: Create default "stable" branch and two examples

And you have just to put your packages into the good Branch/Arch/Dist/Vers and run ``ubik-repo generate`` in your repository root.