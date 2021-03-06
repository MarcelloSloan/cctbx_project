from __future__ import division

from mmtbx.conformation_dependent_library.cdl_setup import \
  before_pro_groups, not_before_pro_groups

def distance2(a,b):
  d2 = 0
  for i in range(3):
    d2 += (a.xyz[i]-b.xyz[i])**2
  return d2

def get_c_ca_n(atom_group, return_subset=False):
  assert atom_group
  tmp = []
  outl = []
  for name in [" C  ", " CA ", " N  "]:
    atom = atom_group.find_atom_by(name=name)
    if atom:
      tmp.append(atom)
    else:
      outl.append('    missing atom "%s %s %s"' % (
        name,
        atom_group.resname,
        atom_group.resseq,
      ))
      if return_subset:
        tmp.append(None)
      else:
        tmp = None
        break
  return tmp, outl

def round_to_int(d, n=10, wrap=True):
  t = int(round((float(d))/int(n)))*int(n)
  if wrap:
    if t==180: return -180
  return t

def round_to_ten(d):
  return round_to_int(d, 10)

def get_res_type_group(resname1, resname2):
  resname1=resname1.strip()
  resname2=resname2.strip()
  if resname2=="PRO":
    lookup = before_pro_groups
  else:
    lookup = not_before_pro_groups
  for key in lookup:
    if resname1 in lookup[key]:
      return key
  return None
