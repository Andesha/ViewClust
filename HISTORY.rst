=======
History
=======

0.4.5 (2020-09-15)
------------------

* Bug fix on sacct poller


0.4.4 (2020-09-14)
------------------

* Added ability to sacct poll all accounts in slurm submodule


0.4.3 (2020-07-22)
------------------

* Refactor calculations for eqv use_unit measures
* Completed support for gpu eqv usage calculations


0.4.2 (2020-07-15)
------------------

* Minor formatting to mem info parsing


0.4.1 (2020-07-13)
------------------

* Can now serialize user run
* Crediting Sergio!


0.4.0 (2020-07-07)
------------------

* Add new support for plotting to the terminal
* Bug fix stderr output


0.3.2 (2020-06-25)
------------------

* Docs update for new changes


0.3.1 (2020-06-24)
------------------

* Bug fix for the init py file


0.3.0 (2020-06-24)
------------------

* Major versioning bump
* User area colouring in usage figures
* Mem info plotting support
* Serialization of user
* Removed violin plot. Moved to ViewClust-Vis
* Removed use_suite. Moved to ViewClust-Vis
* Removed job_stack. Moved to ViewClust-Vis
* Deprecated cumu/insta plotting function. Supported versions moved to ViewClust-Vis


0.2.2 (2020-05-07)
------------------

* Added support for user breakdown of activity on plots


0.2.1 (2020-04-14)
------------------

* Fixed other half of instaplot bug


0.2.0 (2020-04-14)
------------------

* Fix use suite string passing bug


0.1.9 (2020-04-14)
------------------

* Fix insta plot pre reference bug


0.1.8 (2020-04-09)
------------------

* Fix syntax based errors


0.1.7 (2020-04-09)
------------------

* Fix failing doc build


0.1.6 (2020-04-09)
------------------

* GPU usage added back
* README fixes to include credits and features
* Figures now return their handles for extra processing if needed
* Figures can now have their polling rates downsampled for ease of sharing
* Prepared responses for figures section added in to documentation


0.1.5 (2020-03-12)
------------------

* Inclusion of API documentation


0.1.4 (2020-03-11)
------------------

* Overhauled the documentation usage section


0.1.3 (2020-03-03)
------------------

* Reduced versioning complexity


0.1.2 (2020-03-03)
------------------

* Testing distributions changed


0.1.1 (2020-03-03)
------------------

* File inclusion


0.1.0 (2020-03-03)
------------------

* First release on PyPI.
