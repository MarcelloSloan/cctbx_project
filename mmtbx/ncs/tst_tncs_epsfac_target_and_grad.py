from __future__ import division
import cctbx.array_family.flex # import dependency
import boost.python
ext = boost.python.import_ext("mmtbx_ncs_ext")
import iotbx.pdb
from mmtbx.ncs import tncs

pdb_str="""
CRYST1   55.000   55.000   55.000  90.00  90.00  90.00 P 1
SCALE1      0.018182  0.000000  0.000000        0.00000
SCALE2      0.000000  0.018182  0.000000        0.00000
SCALE3      0.000000  0.000000  0.018182        0.00000
ATOM      1 C7   ALA A   1      13.701  17.636  20.433  1.00 10.00           C
ATOM      2 C116 ALA A   2      12.366   6.187  17.949  1.00 10.00           C
ATOM      3 C135 ALA A   3      12.358  18.443  20.392  1.00 10.00           C
ATOM      4 C318 ALA A   4      16.723   9.456  15.994  1.00 10.00           C
ATOM      5 C325 ALA A   5      13.023  10.841  10.069  1.00 10.00           C
ATOM      6 C375 ALA A   6      12.752  15.083   6.413  1.00 10.00           C
ATOM      7 C393 ALA A   7      10.852  10.986   7.235  1.00 10.00           C
ATOM      8 C423 ALA A   8       6.856  17.368  17.973  1.00 10.00           C
ATOM      9 C529 ALA A   9       8.289  18.565  18.488  1.00 10.00           C
ATOM     10 C582 ALA A  10      18.055  19.070   8.401  1.00 10.00           C
ATOM     11 C668 ALA A  11       9.912  22.046  11.754  1.00 10.00           C
ATOM     12 C723 ALA A  12      12.430  16.010  19.850  1.00 10.00           C
ATOM     13 C768 ALA A  13      11.102  15.960  19.526  1.00 10.00           C
ATOM     14 C769 ALA A  14       8.437  12.573  12.854  1.00 10.00           C
ATOM     15 C801 ALA A  15      17.327  17.934  17.256  1.00 10.00           C
ATOM     16 C829 ALA A  16       8.276  18.775  10.775  1.00 10.00           C
ATOM     17 C845 ALA A  17      12.801  22.237   9.595  1.00 10.00           C
ATOM     18 C900 ALA A  18      14.712  14.808  14.485  1.00 10.00           C
ATOM     19 C959 ALA A  19       7.926  15.643   9.501  1.00 10.00           C
ATOM     20 C978 ALA A  20      13.077  16.727  22.622  1.00 10.00           C
ATOM     21 C104 ALA A  21      11.201   9.953  17.040  1.00 10.00           C
ATOM     22 C107 ALA A  22       9.132   7.449  13.843  1.00 10.00           C
ATOM     23 C109 ALA A  23      17.073  16.541  15.076  1.00 10.00           C
ATOM     24 C113 ALA A  24      18.273  10.890  19.158  1.00 10.00           C
ATOM     25 C114 ALA A  25       9.020  12.518  15.904  1.00 10.00           C
ATOM     26 C129 ALA A  26      19.727   9.098  21.104  1.00 10.00           C
ATOM     27 C129 ALA A  27      23.544  17.469  18.536  1.00 10.00           C
ATOM     28 C130 ALA A  28      17.361  17.842  13.001  1.00 10.00           C
ATOM     29 C134 ALA A  29      17.419  12.979  14.542  1.00 10.00           C
ATOM     30 C152 ALA A  30      19.464  11.727  19.346  1.00 10.00           C
ATOM     31 C153 ALA A  31      22.842  12.077  10.237  1.00 10.00           C
ATOM     32 C154 ALA A  32      16.451  13.085  16.752  1.00 10.00           C
ATOM     33 C164 ALA A  33      10.038  20.697  14.559  1.00 10.00           C
ATOM     34 C167 ALA A  34      14.185  20.324   7.437  1.00 10.00           C
ATOM     35 C168 ALA A  35       6.300  17.761  11.873  1.00 10.00           C
ATOM     36 C169 ALA A  36      22.681  12.748  10.334  1.00 10.00           C
ATOM     37 C174 ALA A  37      14.879  15.242  21.473  1.00 10.00           C
ATOM     38 C177 ALA A  38      12.619  10.245  17.743  1.00 10.00           C
ATOM     39 C178 ALA A  39      20.810  12.695  12.135  1.00 10.00           C
ATOM     40 C183 ALA A  40      19.126  18.354  21.302  1.00 10.00           C
ATOM     41 C186 ALA A  41      22.171   9.795  15.535  1.00 10.00           C
ATOM     42 C187 ALA A  42      10.123  20.228  15.505  1.00 10.00           C
ATOM     43 C189 ALA A  43      14.218  20.351  20.400  1.00 10.00           C
ATOM     44 C190 ALA A  44      17.990  14.381   8.065  1.00 10.00           C
ATOM     45 C192 ALA A  45      22.487  11.050   9.852  1.00 10.00           C
ATOM     46 C195 ALA A  46      13.513   9.358  17.902  1.00 10.00           C
ATOM     47 C216 ALA A  47      19.547  19.669  18.906  1.00 10.00           C
ATOM     48 C221 ALA A  48      16.348  19.661  14.511  1.00 10.00           C
ATOM     49 C226 ALA A  49      14.910  11.972  18.502  1.00 10.00           C
ATOM     50 C229 ALA A  50      18.475  23.509  15.945  1.00 10.00           C
ATOM     51 C234 ALA A  51      11.102  10.570  17.360  1.00 10.00           C
ATOM     52 C237 ALA A  52      14.353  22.477  18.648  1.00 10.00           C
ATOM     53 C247 ALA A  53       9.150  19.933  10.445  1.00 10.00           C
ATOM     54 C250 ALA A  54      18.684   6.783  11.555  1.00 10.00           C
ATOM     55 C253 ALA A  55      22.260  15.618  18.081  1.00 10.00           C
ATOM     56 C254 ALA A  56       8.434  20.022  15.818  1.00 10.00           C
ATOM     57 C259 ALA A  57      16.042  14.366   5.312  1.00 10.00           C
ATOM     58 C262 ALA A  58      21.392  21.650  14.481  1.00 10.00           C
ATOM     59 C264 ALA A  59       6.678  17.698  12.625  1.00 10.00           C
ATOM     60 C269 ALA A  60       8.327  12.879  17.470  1.00 10.00           C
ATOM     61 C271 ALA A  61       7.510   9.079  17.557  1.00 10.00           C
ATOM     62 C273 ALA A  62      11.103  16.026  20.771  1.00 10.00           C
ATOM     63 C279 ALA A  63      19.453   8.063  20.118  1.00 10.00           C
ATOM     64 C285 ALA A  64      18.893   7.710  10.625  1.00 10.00           C
ATOM     65 C295 ALA A  65      20.485  20.440  11.734  1.00 10.00           C
ATOM     66 C304 ALA A  66      13.310  10.067  10.497  1.00 10.00           C
ATOM     67 C304 ALA A  67      13.522  10.034  22.514  1.00 10.00           C
ATOM     68 C307 ALA A  68      13.752   5.717  11.896  1.00 10.00           C
ATOM     69 C309 ALA A  69       9.873  10.448  12.931  1.00 10.00           C
ATOM     70 C316 ALA A  70      17.329  16.937  17.428  1.00 10.00           C
ATOM     71 C316 ALA A  71      12.746  11.817  20.837  1.00 10.00           C
ATOM     72 C336 ALA A  72      17.247  10.742  17.405  1.00 10.00           C
ATOM     73 C337 ALA A  73      21.636  11.562  20.613  1.00 10.00           C
ATOM     74 C344 ALA A  74      20.145  20.995  20.309  1.00 10.00           C
ATOM     75 C345 ALA A  75       9.873  12.910  10.483  1.00 10.00           C
ATOM     76 C348 ALA A  76      14.952  20.215  12.301  1.00 10.00           C
ATOM     77 C357 ALA A  77       9.415  11.208   8.319  1.00 10.00           C
ATOM     78 C358 ALA A  78      14.853  16.782  11.204  1.00 10.00           C
ATOM     79 C364 ALA A  79      13.852  15.132  24.685  1.00 10.00           C
ATOM     80 C366 ALA A  80      18.626  10.327  17.281  1.00 10.00           C
ATOM     81 C376 ALA A  81      13.940  16.792  11.870  1.00 10.00           C
ATOM     82 C392 ALA A  82      10.279  17.606  21.633  1.00 10.00           C
ATOM     83 C395 ALA A  83       5.395  16.876  15.353  1.00 10.00           C
ATOM     84 C399 ALA A  84      12.370  14.354  19.736  1.00 10.00           C
TER
ATOM      1 C7   ALA B   1      33.629  37.483  40.057  1.00 10.00           C
ATOM      2 C116 ALA B   2      32.207  25.758  38.091  1.00 10.00           C
ATOM      3 C135 ALA B   3      32.730  38.636  40.789  1.00 10.00           C
ATOM      4 C318 ALA B   4      36.791  29.905  35.951  1.00 10.00           C
ATOM      5 C325 ALA B   5      32.470  31.007  29.953  1.00 10.00           C
ATOM      6 C375 ALA B   6      32.035  34.885  26.241  1.00 10.00           C
ATOM      7 C393 ALA B   7      31.115  30.943  27.010  1.00 10.00           C
ATOM      8 C423 ALA B   8      27.006  36.919  38.423  1.00 10.00           C
ATOM      9 C529 ALA B   9      27.989  38.384  39.082  1.00 10.00           C
ATOM     10 C582 ALA B  10      37.996  39.441  28.616  1.00 10.00           C
ATOM     11 C668 ALA B  11      30.058  41.645  32.487  1.00 10.00           C
ATOM     12 C723 ALA B  12      32.709  35.478  40.348  1.00 10.00           C
ATOM     13 C768 ALA B  13      31.595  35.968  39.451  1.00 10.00           C
ATOM     14 C769 ALA B  14      28.607  32.772  33.124  1.00 10.00           C
ATOM     15 C801 ALA B  15      37.367  37.939  37.494  1.00 10.00           C
ATOM     16 C829 ALA B  16      28.448  38.667  31.552  1.00 10.00           C
ATOM     17 C845 ALA B  17      32.389  42.098  30.000  1.00 10.00           C
ATOM     18 C900 ALA B  18      34.712  34.747  34.213  1.00 10.00           C
ATOM     19 C959 ALA B  19      27.940  35.599  29.639  1.00 10.00           C
ATOM     20 C978 ALA B  20      33.179  36.087  42.776  1.00 10.00           C
ATOM     21 C104 ALA B  21      31.825  30.277  36.740  1.00 10.00           C
ATOM     22 C107 ALA B  22      29.386  27.282  33.262  1.00 10.00           C
ATOM     23 C109 ALA B  23      36.838  36.604  35.303  1.00 10.00           C
ATOM     24 C113 ALA B  24      38.765  30.918  38.898  1.00 10.00           C
ATOM     25 C114 ALA B  25      28.613  32.074  35.871  1.00 10.00           C
ATOM     26 C129 ALA B  26      39.751  29.397  40.286  1.00 10.00           C
ATOM     27 C129 ALA B  27      44.016  37.648  38.635  1.00 10.00           C
ATOM     28 C130 ALA B  28      36.840  37.477  32.864  1.00 10.00           C
ATOM     29 C134 ALA B  29      37.766  33.004  34.710  1.00 10.00           C
ATOM     30 C152 ALA B  30      39.335  31.789  39.345  1.00 10.00           C
ATOM     31 C153 ALA B  31      43.142  32.072  29.467  1.00 10.00           C
ATOM     32 C154 ALA B  32      36.139  33.176  36.560  1.00 10.00           C
ATOM     33 C164 ALA B  33      29.927  40.295  34.577  1.00 10.00           C
ATOM     34 C167 ALA B  34      33.392  40.684  27.475  1.00 10.00           C
ATOM     35 C168 ALA B  35      25.888  37.606  32.221  1.00 10.00           C
ATOM     36 C169 ALA B  36      42.237  32.657  29.963  1.00 10.00           C
ATOM     37 C174 ALA B  37      34.646  34.971  41.301  1.00 10.00           C
ATOM     38 C177 ALA B  38      33.141  30.239  37.921  1.00 10.00           C
ATOM     39 C178 ALA B  39      40.262  32.855  31.999  1.00 10.00           C
ATOM     40 C183 ALA B  40      39.299  37.808  41.185  1.00 10.00           C
ATOM     41 C186 ALA B  41      42.581  29.835  35.151  1.00 10.00           C
ATOM     42 C187 ALA B  42      30.112  40.340  36.163  1.00 10.00           C
ATOM     43 C189 ALA B  43      33.969  39.902  40.547  1.00 10.00           C
ATOM     44 C190 ALA B  44      37.594  34.269  27.934  1.00 10.00           C
ATOM     45 C192 ALA B  45      42.217  31.750  29.257  1.00 10.00           C
ATOM     46 C195 ALA B  46      33.674  29.140  38.091  1.00 10.00           C
ATOM     47 C216 ALA B  47      39.924  39.197  38.768  1.00 10.00           C
ATOM     48 C221 ALA B  48      35.838  39.936  34.881  1.00 10.00           C
ATOM     49 C226 ALA B  49      35.207  31.824  38.237  1.00 10.00           C
ATOM     50 C229 ALA B  50      38.208  43.472  35.766  1.00 10.00           C
ATOM     51 C234 ALA B  51      30.837  30.576  37.681  1.00 10.00           C
ATOM     52 C237 ALA B  52      34.418  41.980  39.194  1.00 10.00           C
ATOM     53 C247 ALA B  53      29.220  39.587  30.382  1.00 10.00           C
ATOM     54 C250 ALA B  54      38.385  27.092  31.196  1.00 10.00           C
ATOM     55 C253 ALA B  55      42.314  35.372  37.635  1.00 10.00           C
ATOM     56 C254 ALA B  56      27.859  39.968  36.542  1.00 10.00           C
ATOM     57 C259 ALA B  57      35.947  34.685  25.402  1.00 10.00           C
ATOM     58 C262 ALA B  58      41.193  41.883  34.315  1.00 10.00           C
ATOM     59 C264 ALA B  59      26.451  37.533  32.522  1.00 10.00           C
ATOM     60 C269 ALA B  60      28.509  32.194  37.171  1.00 10.00           C
ATOM     61 C271 ALA B  61      27.176  28.683  37.113  1.00 10.00           C
ATOM     62 C273 ALA B  62      31.639  35.892  40.452  1.00 10.00           C
ATOM     63 C279 ALA B  63      39.991  28.066  39.457  1.00 10.00           C
ATOM     64 C285 ALA B  64      39.056  27.565  30.762  1.00 10.00           C
ATOM     65 C295 ALA B  65      40.609  41.159  31.321  1.00 10.00           C
ATOM     66 C304 ALA B  66      32.975  30.640  30.089  1.00 10.00           C
ATOM     67 C304 ALA B  67      33.621  30.108  42.275  1.00 10.00           C
ATOM     68 C307 ALA B  68      33.732  25.725  31.381  1.00 10.00           C
ATOM     69 C309 ALA B  69      29.691  30.483  33.155  1.00 10.00           C
ATOM     70 C316 ALA B  70      37.833  37.393  37.774  1.00 10.00           C
ATOM     71 C316 ALA B  71      32.500  31.149  40.733  1.00 10.00           C
ATOM     72 C336 ALA B  72      37.083  30.383  37.398  1.00 10.00           C
ATOM     73 C337 ALA B  73      41.381  31.928  40.569  1.00 10.00           C
ATOM     74 C344 ALA B  74      40.625  40.814  40.559  1.00 10.00           C
ATOM     75 C345 ALA B  75      29.526  33.019  30.368  1.00 10.00           C
ATOM     76 C348 ALA B  76      34.727  39.887  31.980  1.00 10.00           C
ATOM     77 C357 ALA B  77      29.063  31.178  28.460  1.00 10.00           C
ATOM     78 C358 ALA B  78      34.723  36.845  31.753  1.00 10.00           C
ATOM     79 C364 ALA B  79      34.249  35.182  45.102  1.00 10.00           C
ATOM     80 C366 ALA B  80      38.406  30.502  37.220  1.00 10.00           C
ATOM     81 C376 ALA B  81      34.167  36.966  32.126  1.00 10.00           C
ATOM     82 C392 ALA B  82      30.371  36.813  41.511  1.00 10.00           C
ATOM     83 C395 ALA B  83      25.033  37.160  35.732  1.00 10.00           C
ATOM     84 C399 ALA B  84      32.167  34.524  39.794  1.00 10.00           C
TER
END
"""

def run(reflections_per_bin=250):
  #
  # Read PDB file from string above, create xray_structure object
  #
  pdb_inp = iotbx.pdb.input(source_info=None, lines=pdb_str)
  pdb_inp.write_pdb_file(file_name="model.pdb")
  xray_structure = pdb_inp.xray_structure_simple()
  #
  # Calculate "Fobs" from this model
  #
  f_obs = abs(xray_structure.structure_factors(d_min=2.0).f_calc())
  #
  o = tncs.compute_eps_factor(
    f_obs               = f_obs,
    pdb_hierarchy       = pdb_inp.construct_hierarchy(),
    reflections_per_bin = reflections_per_bin)
  o.show_summary()

if (__name__ == "__main__"):
  run()
