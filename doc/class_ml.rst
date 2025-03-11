Machine learning classes
========================

.. This documentation should go here in the future?
   transformations:
   quantile transforms to [0,1]
   MinMaxScaler transforms to [a,b]

These classes are simple wrappers around machine learning classes to
perform basic tasks. While they are also designed to be accessed in
C++ by O₂scl, they do not require the installation of O₂scl to be
functional.
   
Interpolators
-------------

* :class:`o2sclpy.interpm_sklearn_gp`: Gaussian process interpolation
  from scikit-learn
* :class:`o2sclpy.interpm_sklearn_mlpr`: Multilayer perceptron
  regression from scikit-learn
* :class:`o2sclpy.interpm_sklearn_dtr`: Decision-tree regression
  from scikit-learn
* :class:`o2sclpy.interpm_tf_dnn`: Regression using a simple
  Tensorflow neural network
* :class:`o2sclpy.interpm_torch_dnn` Regression using a simple
  Torch neural network

Classifiers
-----------

* :class:`o2sclpy.classify_sklearn_gnb` Gaussian naive Bayes
  classifier from scikit-learn
* :class:`o2sclpy.classify_sklearn_mlpc` Multilayer perceptron
  classifier from scikit-learn
* :class:`o2sclpy.classify_sklearn_dtc` Decision-tree classification
  from scikit-learn

Probability density functions
-----------------------------

* Gaussian mixture model in :class:`o2sclpy.gmm_sklearn` and
  Bayesian Gaussian mixture model in :class:`o2sclpy.bgmm_sklearn`.
* Kernel density estimators: :class:`o2sclpy.kde_sklearn` and
  :class:`o2sclpy.kde_scipy`.
* Normalizing flows using Torch and the ``nflows`` package:
  :class:`o2sclpy.nflows_nsf`.

Class documentation
-------------------
   
.. autoclass:: o2sclpy.bgmm_sklearn
	:members:
	:undoc-members:

.. autoclass:: o2sclpy.classify_sklearn_dtc
	:members:
	:undoc-members:

.. autoclass:: o2sclpy.classify_sklearn_gnb
	:members:
	:undoc-members:

.. autoclass:: o2sclpy.classify_sklearn_mlpc
	:members:
	:undoc-members:

.. autoclass:: o2sclpy.gmm_sklearn
	:members:
	:undoc-members:

.. autoclass:: o2sclpy.nflows_nsf
	:members:
	:undoc-members:

.. autoclass:: o2sclpy.kde_sklearn
	:members:
	:undoc-members:

.. autoclass:: o2sclpy.kde_scipy
	:members:
	:undoc-members:

.. autoclass:: o2sclpy.interpm_sklearn_dtr
	:members:
	:undoc-members:

.. autoclass:: o2sclpy.interpm_sklearn_gp
	:members:
	:undoc-members:

.. autoclass:: o2sclpy.interpm_sklearn_mlpr
	:members:
	:undoc-members:

.. autoclass:: o2sclpy.interpm_tf_dnn
	:members:
	:undoc-members:

.. autoclass:: o2sclpy.interpm_torch_dnn
	:members:
	:undoc-members:

