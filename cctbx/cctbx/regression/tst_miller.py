from cctbx import crystal
from cctbx import miller
from cctbx.array_family import flex
from scitbx.test_utils import approx_equal
import math

def exercise_set():
  xs = crystal.symmetry((3,4,5), "P 2 2 2")
  mi = flex.miller_index(((1,2,3), (0,0,4)))
  ms = miller.set(xs, mi)
  ms = miller.set(xs, mi, 00000)
  ms = miller.set(xs, mi, 0001)
  assert ms.indices() == mi
  assert ms.anomalous_flag() == 0001
  assert tuple(ms.multiplicities().data()) == (4, 2)
  assert tuple(ms.epsilons().data()) == (1, 2)
  assert approx_equal(tuple(ms.d_spacings().data()), (1.177603, 1.25))
  assert approx_equal(tuple(ms.sin_theta_over_lambda_sq().data()),
                      (0.1802778, 0.16))
  assert approx_equal(ms.d_min(), 1.177603)
  assert approx_equal(ms.resolution_range(), (1.25, 1.177603))
  p1 = ms.expand_to_p1()
  assert p1.indices().size() == 6
  b = p1.setup_binner(auto_binning=0001)
  b = p1.setup_binner(reflections_per_bin=1)
  b = p1.setup_binner(n_bins=8)
  assert id(p1.binner()) == id(b)
  assert b.limits().size() == 9

def exercise_array():
  xs = crystal.symmetry((3,4,5), "P 2 2 2")
  mi = flex.miller_index(((1,-2,3), (0,0,-4)))
  data = flex.double((1,2))
  sigmas = flex.double((0.1,0.2))
  ms = miller.set(xs, mi)
  ma = miller.array(ms)
  ma = miller.array(ms, data)
  ma = miller.array(ms, data, sigmas)
  ma = miller.array(ms, data, sigmas, "test")
  assert ma.indices() == mi
  assert ma.data() == data
  assert ma.sigmas() == sigmas
  assert ma.info() == "test"
  ma.set_info("Test")
  assert ma.info() == "Test"
  asu = ma.map_to_asu()
  assert tuple(asu.indices()) == ((1,2,3), (0,0,4))
  mi = flex.miller_index(((1,2,3), (-1,-2,-3), (2,3,4), (-2,-3,-4), (3,4,5)))
  data = flex.double((1,2,5,3,6))
  sigmas = flex.double((0.1,0.2,0.3,0.4,0.5))
  ms = miller.set(xs, mi, anomalous_flag=0001)
  ma = miller.array(ms, data, sigmas)
  ad = ma.anomalous_differences()
  assert tuple(ad.indices()) == ((1,2,3), (2,3,4))
  assert approx_equal(tuple(ad.data()), (-1.0, 2.0))
  assert approx_equal(tuple(ad.sigmas()), (math.sqrt(0.05), 0.5))
  hs = ma.hemisphere("+")
  assert tuple(hs.indices()) == ((1,2,3), (2,3,4))
  assert approx_equal(tuple(hs.data()), (1,5))
  assert approx_equal(tuple(hs.sigmas()), (0.1,0.3))
  hs = ma.hemisphere("-")
  assert tuple(hs.indices()) == ((-1,-2,-3), (-2,-3,-4))
  assert approx_equal(tuple(hs.data()), (2,3))
  assert approx_equal(tuple(hs.sigmas()), (0.2,0.4))
  ms = miller.set(crystal.symmetry(), mi, anomalous_flag=0001)
  ma = miller.array(ms, data, sigmas)
  ad = ma.anomalous_differences()
  assert tuple(ad.indices()) == ((1,2,3), (2,3,4))
  hs = ma.hemisphere("+")
  assert tuple(hs.indices()) == ((1,2,3), (2,3,4))
  assert approx_equal(tuple(hs.data()), (1,5))
  assert approx_equal(tuple(hs.sigmas()), (0.1,0.3))
  hs = ma.hemisphere("-")
  assert tuple(hs.indices()) == ((-1,-2,-3), (-2,-3,-4))
  assert approx_equal(tuple(hs.data()), (2,3))
  assert approx_equal(tuple(hs.sigmas()), (0.2,0.4))
  assert tuple(ma.all_selection()) == (1,1,1,1,1)
  sa = ma.apply_selection(flex.bool((1,0,0,1,0)))
  assert tuple(sa.indices()) == ((1,2,3), (-2,-3,-4))
  assert approx_equal(tuple(sa.data()), (1,3))
  assert approx_equal(tuple(sa.sigmas()), (0.1,0.4))
  ms = miller.build_set(xs, anomalous_flag=00000, d_min=1)
  ma = miller.array(ms)
  sa = ma.resolution_filter()
  assert ma.indices().size() == sa.indices().size()
  sa = ma.resolution_filter(0.5)
  assert sa.indices().size() == 0
  sa = ma.resolution_filter(d_min=2)
  assert sa.indices().size() == 10
  sa = ma.resolution_filter(d_min=2, negate=0001)
  assert sa.indices().size() == 38
  ma = ma.d_spacings()
  ma = miller.array(ma, ma.data(), ma.data().deep_copy())
  assert ma.indices().size() == 48
  sa = ma.sigma_filter(0.5)
  assert sa.indices().size() == 48
  sa = ma.sigma_filter(2)
  assert sa.indices().size() == 0
  for i in (1,13,25,27,39):
    ma.sigmas()[i] /= 3
  sa = ma.sigma_filter(2)
  assert sa.indices().size() == 5
  assert approx_equal(ma.mean(0,0), 1.6460739)
  assert approx_equal(ma.mean(0,1), 1.5146784)
  ma.setup_binner(n_bins=3)
  assert approx_equal(tuple(ma.mean(1,0)), (2.228192, 1.2579831, 1.0639812))
  assert approx_equal(tuple(ma.mean(1,1)), (2.069884, 1.2587977, 1.0779636))
  assert approx_equal(ma.mean_sq(0,0), 3.3287521)
  assert approx_equal(ma.mean_sq(0,1), 2.6666536)
  assert approx_equal(tuple(ma.mean_sq(1,0)), (5.760794, 1.5889009, 1.1336907))
  assert approx_equal(tuple(ma.mean_sq(1,1)), (4.805354, 1.5916849, 1.1629777))
  assert approx_equal(ma.rms(0,0)**2, 3.3287521)
  assert approx_equal(ma.rms(0,1)**2, 2.6666536)
  assert approx_equal([x**2 for x in ma.rms(1,0)], tuple(ma.mean_sq(1,0)))
  assert approx_equal([x**2 for x in ma.rms(1,1)], tuple(ma.mean_sq(1,1)))
  for use_binning in (0,1):
    for use_multiplicities in (0,1):
      sa = ma.rms_filter(-1, use_binning, use_multiplicities)
      assert sa.indices().size() == 0
      sa = ma.rms_filter(100, use_binning, use_multiplicities, 00000)
      assert sa.indices().size() == ma.indices().size()
      sa = ma.rms_filter(-1, use_binning, use_multiplicities, negate=0001)
      assert sa.indices().size() == ma.indices().size()
      sa = ma.rms_filter(100, use_binning, use_multiplicities, negate=0001)
      assert sa.indices().size() == 0
      sa = ma.rms_filter(1.0, use_binning, use_multiplicities)
      assert sa.indices().size() \
          == ((36, 33), (29, 29))[use_binning][use_multiplicities]
  assert approx_equal(ma.statistical_mean(), 1.380312)
  assert approx_equal(tuple(ma.statistical_mean(0001)),
                      (1.768026, 1.208446, 0.9950434))
  no = ma.remove_patterson_origin_peak()
  assert approx_equal(no.data()[0], 3.231974)
  assert approx_equal(no.data()[47], 0.004956642)
  no = ma.normalize_structure_factors()
  assert approx_equal(no.data()[0], 2.415594)
  assert approx_equal(no.data()[47], 0.9276751)
  su = ma + 3
  assert approx_equal(tuple(su.data()), tuple(ma.data() + 3))
  su = ma + ma
  assert approx_equal(tuple(su.data()), tuple(ma.data() * 2))
  assert approx_equal(tuple(su.sigmas()), tuple(ma.sigmas() * math.sqrt(2)))
  s = ma.f_as_f_sq()
  v = s.f_sq_as_f()
  assert approx_equal(tuple(ma.data()), tuple(v.data()))
  assert not approx_equal(tuple(ma.sigmas()), tuple(v.sigmas()))
  s = miller.array(ma, ma.data()).f_as_f_sq()
  v = s.f_sq_as_f()
  assert approx_equal(tuple(ma.data()), tuple(v.data()))
  assert s.sigmas() == None
  assert v.sigmas() == None
  ma = miller.array(ms)
  s = ma[:]
  assert s.data() == None
  assert s.sigmas() == None
  ma = miller.array(ms, flex.double((1,2)))
  s = ma[:]
  assert s.data().all_eq(ma.data())
  assert s.sigmas() == None
  ma = miller.array(ms, flex.double((1,2)), flex.double(3,4))
  s = ma[:]
  assert s.data().all_eq(ma.data())
  assert s.sigmas().all_eq(ma.sigmas())

def exercise_fft_map():
  xs = crystal.symmetry((3,4,5), "P 2 2 2")
  mi = flex.miller_index(((1,-2,3), (0,0,-4)))
  for anomalous_flag in (00000, 0001):
    for data in (flex.double((1,2)), flex.complex_double((1,2))):
      ms = miller.set(xs, mi, anomalous_flag=anomalous_flag)
      ma = miller.array(ms, data)
      fft_map = miller.fft_map(ma)
      assert approx_equal(fft_map.resolution_factor(), 1./3)
      assert fft_map.symmetry_flags() == None
      assert approx_equal(fft_map.max_prime(), 5)
      assert fft_map.anomalous_flag() == anomalous_flag
      assert fft_map.real_map().size() > 0
      if (anomalous_flag):
        assert fft_map.complex_map().size() > 0

def run():
  exercise_set()
  exercise_array()
  exercise_fft_map()
  print "OK"

if (__name__ == "__main__"):
  run()
