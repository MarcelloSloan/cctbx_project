from __future__ import division
from libtbx.str_utils import make_sub_header
from libtbx.utils import Sorry, Usage
from math import sqrt
import random
import sys

merging_params_str = """
high_resolution = None
  .type = float
low_resolution = None
  .type = float
n_bins = 10
  .type = int
anomalous = False
  .type = bool
"""

master_phil = """
file_name = None
  .type = path
labels = None
  .type = str
space_group = None
  .type = space_group
unit_cell = None
  .type = unit_cell
symmetry_file = None
  .type = path
%s
debug = False
  .type = bool
""" % merging_params_str

def compute_cc_one_half (merged, unmerged, n_trials=1) :
  from cctbx.array_family import flex
  indices = merged.indices()
  cc_all = []
  for x in range(n_trials) :
    data_1 = flex.double()
    data_2 = flex.double()
    for hkl in indices :
      sele = (unmerged.indices() == hkl)
      hkl_array = unmerged.select(sele)
      n_obs = [0, 0]
      i_sum = [0, 0]
      for i_obs in range(len(hkl_array.indices())) :
        i_rand = random.randint(0,1)
        n_obs[i_rand] += 1
        i_sum[i_rand] += hkl_array.data()[i_obs]
      if (n_obs[0] > 0) and (n_obs[1] > 0) :
        data_1.append(i_sum[0] / n_obs[0])
        data_2.append(i_sum[1] / n_obs[1])
    cc = flex.linear_correlation(data_1, data_2).coefficient()
    cc_all.append(cc)
  return sum(cc_all) / n_trials

class merging_stats (object) :
  def __init__ (self, array, anomalous=False, debug=None) :
    from scitbx.array_family import flex
    array = array.customized_copy(anomalous_flag=anomalous).map_to_asu()
    self.merge = array.merge_equivalents()
    self.array_merged = self.merge.array()
    self.d_max, self.d_min = array.d_max_min()
    self.n_obs = array.indices().size()
    self.n_uniq = self.array_merged.indices().size()
    self.redundancies = self.merge.redundancies().data()
    self.mean_redundancy = flex.mean(self.redundancies.as_double())
    self.i_mean = flex.mean(self.array_merged.data())
    self.sigi_mean = flex.mean(self.array_merged.sigmas())
    nonzero_array = self.array_merged.select(self.array_merged.sigmas() != 0)
    i_over_sigma = nonzero_array.data() / nonzero_array.sigmas()
    self.i_over_sigma_mean = flex.mean(i_over_sigma)
    self.r_merge = self.merge.r_merge()
    self.r_meas = self.merge.r_meas()
    self.r_pim = self.merge.r_pim()
    # XXX Pure-Python reference implementation
    if (debug) :
      from libtbx.test_utils import approx_equal
      r_merge_num = r_meas_num = r_pim_num = r_merge_den = 0
      indices = self.array_merged.indices()
      data = self.array_merged.data()
      for hkl, i_mean in zip(indices, data) :
        sele = (array.indices() == hkl)
        hkl_array = array.select(sele)
        n_hkl = hkl_array.indices().size()
        if (n_hkl > 1) :
          sum_num = sum_den = 0
          for i_obs in hkl_array.data() :
            sum_num += abs(i_obs - i_mean)
            sum_den += i_obs
          r_merge_num += sum_num
          r_meas_num += sqrt(n_hkl/(n_hkl-1.)) * sum_num
          r_pim_num += sqrt(1./(n_hkl-1)) * sum_num
          r_merge_den += sum_den
      assert (approx_equal(self.r_merge, r_merge_num / r_merge_den))
      assert (approx_equal(self.r_meas, r_meas_num / r_merge_den))
      assert (approx_equal(self.r_pim, r_pim_num / r_merge_den))
    #self.cc_one_half = compute_cc_one_half(
    #  merged=self.array_merged,
    #  unmerged=array)
    #self.cc_star = sqrt((2*self.cc_one_half) / (1 + self.cc_one_half))

  def format (self) :
    #return "%6.2f  %6.2f %6d %6d   %5.2f  %8.1f  %6.1f  %5.3f  %5.3f  %5.3f  %5.3f  %5.3f" % (
    return "%6.2f  %6.2f %6d %6d   %5.2f  %8.1f  %6.1f  %5.3f  %5.3f  %5.3f" % (
      self.d_max, self.d_min,
      self.n_obs, self.n_uniq,
      self.mean_redundancy,
      self.i_mean, self.i_over_sigma_mean,
      self.r_merge, self.r_meas, self.r_pim)#,
#      self.cc_one_half, self.cc_star)

  def show_summary (self, out=sys.stdout) :
    print >> out, "Resolution: %.2f - %.2f" % (self.d_max, self.d_min)
    print >> out, "Observations: %d" % self.n_obs
    print >> out, "Unique reflections: %d" % self.n_uniq
    print >> out, "Redundancy: %.1f" % self.mean_redundancy
    print >> out, "Mean intensity: %.1f" % self.i_mean
    print >> out, "Mean I/sigma(I): %.1f" % self.i_over_sigma_mean
    print >> out, "R-merge: %5.3f" % self.r_merge
    print >> out, "R-meas:  %5.3f" % self.r_meas
    print >> out, "R-pim:   %5.3f" % self.r_pim

def show_merging_statistics (
    i_obs,
    crystal_symmetry=None,
    params=None,
    debug=False,
    out=None) :
  if (out is None) : out = sys.stdout
  if (params is None) :
    params = iotbx.phil.parase(merging_params_str).extract()
  info = i_obs.info()
  i_obs = i_obs.customized_copy(
    crystal_symmetry=crystal_symmetry).set_info(info)
  i_obs = i_obs.resolution_filter(
    d_min=params.high_resolution,
    d_max=params.low_resolution).set_info(info)
  i_obs.show_summary()
  anom_extra = ""
  if (not params.anomalous) :
    i_obs = i_obs.customized_copy(anomalous_flag=False)
    anom_extra = " (non-anomalous)"
  i_obs.setup_binner(n_bins=params.n_bins)
  merge = i_obs.merge_equivalents()
  stats = merging_stats(i_obs, anomalous=params.anomalous, debug=debug)
  make_sub_header("Merging statistics")
  stats.show_summary(out)
  print >> out, ""
  print >> out, "Redundancies%s:" % anom_extra
  for x in sorted(set(stats.redundancies)) :
    print "  %d : %d" % (x, stats.redundancies.count(x))
  print >> out, ""
  print >> out, """\
Statistics by resolution bin:
 d_min   d_max   #obs  #uniq   mult.       <I>  <I/sI>  r_mrg r_meas  r_pim"""
#  print >> out, """\
#Statistics by resolution bin:
# d_min   d_max   #obs  #uniq   mult.       <I>  <I/sI>  r_mrg r_meas  r_pim  cc1/2    cc*"""
  # statistics by bin
  for bin in i_obs.binner().range_used() :
    sele_unmerged = i_obs.binner().selection(bin)
    bin_stats = merging_stats(i_obs.select(sele_unmerged),
      anomalous=params.anomalous,
      debug=debug)
    print >> out, bin_stats.format()
  # overall statistics
  print >> out, stats.format()

def run (args, out=None) :
  if (out is None) : out = sys.stdout
  import iotbx.phil
  master_params = iotbx.phil.parse(master_phil)
  if (len(args) == 0) :
    raise Usage("""\
iotbx.merging_statistics [data_file] [options...]

Calculate merging statistics for non-unique data, including R-merge, R-meas,
R-pim, and redundancy.

Full parameters:
%s
""" % master_params.as_str(prefix="  "))
  import iotbx.phil
  cmdline = iotbx.phil.process_command_line_with_files(
    args=args,
    master_phil=master_params,
    reflection_file_def="file_name",
    pdb_file_def="symmetry_file")
  params = cmdline.work.extract()
  from iotbx import reflection_file_reader
  hkl_in = reflection_file_reader.any_reflection_file(params.file_name)
  print >> out, "Format:", hkl_in.file_type()
  miller_arrays = hkl_in.as_miller_arrays(merge_equivalents=False)
  i_obs = None
  all_i_obs = []
  for array in miller_arrays :
    labels = array.info().label_string()
    if (labels == params.labels) :
      i_obs = array
      break
    elif (array.is_xray_intensity_array()) :
      all_i_obs.append(array)
  if (i_obs is None) :
    if (len(all_i_obs) == 0) :
      raise Sorry("No intensities found in %s." % params.file_name)
    elif (len(all_i_obs) > 1) :
      raise Sorry("Multiple intensity arrays - please specify one:\n%s" %
        "\n".join(["  labels=%s"%a.info().label_string() for a in all_i_obs]))
    else :
      i_obs = all_i_obs[0]
  if (not i_obs.is_xray_intensity_array()) :
    raise Sorry("%s is not an intensity array." % i_obs.info().label_string())
  symm = None
  if (params.symmetry_file is not None) :
    from iotbx import crystal_symmetry_from_any
    symm = crystal_symmetry_from_any.extract_from(
      file_name=params.symmetry_file)
    if (symm is None) :
      raise Sorry("No symmetry records found in %s." % params.symmetry_file)
  if (symm is None) :
    sg = i_obs.space_group()
    if (sg is None) :
      if (params.space_group is not None) :
        sg = params.space_group.group()
      else :
        raise Sorry("Missing space group information.")
    uc = i_obs.unit_cell()
    if (uc is None) :
      if (params.unit_cell is not None) :
        uc = params.unit_cell
      else :
        raise Sorry("Missing unit cell information.")
    from cctbx import crystal
    symm = crystal.symmetry(
      space_group=sg,
      unit_cell=uc)
  if (i_obs.is_unique_set_under_symmetry()) :
    raise Sorry(("The data in %s are already merged.  Only unmerged (but "+
      "scaled) data may be used in this program.")%i_obs.info().label_string())
  show_merging_statistics(
    i_obs=i_obs,
    crystal_symmetry=symm,
    params=params,
    debug=params.debug,
    out=out)
  show_citations(out=out)

def show_citations (out=sys.stdout) :
  print >> out, """
References:
  Diederichs K & Karplus PA (1997) Nature Structural Biology 4:269-275
    (also erratum in: Nat Struct Biol 1997 Jul;4(7):592)
  Weiss MS (2001) J Appl Cryst 34:130-135.
"""
  # Karplus PA & Diederichs K (2012) Science 336:1030-3.

if (__name__ == "__main__") :
  run(sys.argv[1:])
