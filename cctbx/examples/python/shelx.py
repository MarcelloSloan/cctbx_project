#! /usr/local/Python-2.1/bin/python

import sys
sys.stderr = sys.stdout

print "Content-type: text/plain"
print

import traceback
import exceptions
class FormatError(exceptions.Exception): pass

import string, cgi

sys.path.insert(0, "/net/boa/srv/html/sgtbx") # for sgtbx
import sgtbx

print "sgtbx version:", sgtbx.__version__
print

class Empty: pass

def GetFormData():
  form = cgi.FieldStorage()
  inp = Empty()
  for key in (("sgsymbol", "P1"),
              ("convention", "")):
    if (form.has_key(key[0])):
      inp.__dict__[key[0]] = string.strip(form[key[0]].value)
    else:
      inp.__dict__[key[0]] = key[1]
  return inp

def Symbol_to_SgOps(sgsymbol, convention):
  if (convention == "Hall"):
    HallSymbol = sgsymbol
  else:
    Symbols_Inp = sgtbx.SpaceGroupSymbols(sgsymbol, convention)
    HallSymbol = Symbols_Inp.Hall()
  try:
    ps = sgtbx.parse_string(HallSymbol)
    SgOps = sgtbx.SgOps(ps)
  except RuntimeError, e:
    print "-->" + ps.string() + "<--"
    print ("-" * (ps.where() + 3)) + "^"
    raise
  return SgOps

def Write_SHELX_LATT_SYMM(SgOps):
  Z = SgOps.getConventionalCentringTypeSymbol()
  Z_dict = {
    "P": 1,
    "I": 2,
    "R": 3,
    "F": 4,
    "A": 5,
    "B": 6,
    "C": 7,
  }
  try:
    LATT_N = Z_dict[Z]
  except:
    print "Error: Lattice type not supported by SHELX."
    return

  # N must be made negative if the structure is non-centrosymmetric.
  if (SgOps.isCentric()):
    if (not SgOps.isOriginCentric()):
      print "Error:"
      print "SHELX manual: If the structure is centrosymmetric, the"
      print "              origin MUST lie on a center of symmetry."
      return
    LATT_N = -LATT_N;

  print "LATT", LATT_N

  # The operator x,y,z is always assumed, so MUST NOT be input.
  for i in xrange(1, SgOps.nSMx()): print "SYMM", SgOps(i)

inp = GetFormData()

try:
  SgOps = Symbol_to_SgOps(inp.sgsymbol, inp.convention)
  SgType = SgOps.getSpaceGroupType()
  print "Space group: (%d) %s" % (
    SgType.SgNumber(), SgOps.BuildLookupSymbol(SgType))
  print
  Write_SHELX_LATT_SYMM(SgOps)

except RuntimeError, e:
  print e
except:
  ei = sys.exc_info()
  print traceback.format_exception_only(ei[0], ei[1])[0]
