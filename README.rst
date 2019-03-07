|pypi| |travis| |codecov| |downloads|

Allocation
==========

Functions to allocate new subjects to a trial either by randomization or adaptive methods.

Note: This is a work in progress.


Minimization
~~~~~~~~~~~

Minimization attempts to minimize imbalance within a set of factors between a group of treatments.

Suppose you are interested in sex and race a prognostic factors in a clinical trial.

So far, you have the following counts:

+------------------+----------+-------------+------------+
| Prognostic Factor| Level    | Treatment 1 | Treatment 2|
+------------------+----------+-------------+------------+
|Sex               | Male     | 8           | 9          |
|                  | Female   | 10          | 9          |
+------------------+----------+-------------+------------+
|Race              | AA       | 3           | 4          |
|                  | Asian    | 2           | 0          |
|                  | Hispanic | 2           | 2          |
|                  | White    | 11          | 12         |
+------------------+----------+-------------+------------+

The next person to be assigned to a treatment is an Hispanic Female.

To perform the minimization, we add up the number of Hispanic and Females assigned to each treatment.  Treatment 1 has ``10 + 2 = 12``.  Treatment 2 has ``9 + 2 = 11``.  Since ``11 < 12``, we assign the new subject to Treatment 2.

Double Biased Coin Minimization
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Returns a group assignment for adaptive trials using the Double Biased Coin Minimization method.

Suppose that :math:`N_{c}` is the number of controls, of which :math:`S_{c}` were successes and :math:`N_{t}` is the number of treatments, of which :math:`S_{t}` were successes.  We can define the probability of success as:

.. math::
    p_{c} = \\frac{S_{c}}{N_{c}}
    p_{t} = \\frac{S_{t}}{N_{t}}

The next subject will be randomized to the control group with probability:

.. math::
    \\frac{\sqrt{p_{c}}}{\\sqrt{p_{c}} + \\sqrt{p_{t}}}

.. |pypi| image:: https://img.shields.io/pypi/v/allocation.svg
    :target: https://pypi.python.org/pypi/allocation
    
.. |travis| image:: https://travis-ci.com/erikvw/allocation.svg?branch=setup_tox
    :target: https://travis-ci.com/erikvw/allocation
    
.. |codecov| image:: https://codecov.io/gh/erikvw/allocation/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/erikvw/allocation

.. |downloads| image:: https://pepy.tech/badge/allocation
   :target: https://pepy.tech/project/allocation
