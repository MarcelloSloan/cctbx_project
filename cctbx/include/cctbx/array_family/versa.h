// $Id$
/* Copyright (c) 2001 The Regents of the University of California through
   E.O. Lawrence Berkeley National Laboratory, subject to approval by the
   U.S. Department of Energy. See files COPYRIGHT.txt and
   cctbx/LICENSE.txt for further details.

   Revision history:
     Feb 2002: Created (R.W. Grosse-Kunstleve)
 */

#ifndef CCTBX_ARRAY_FAMILY_VERSA_H
#define CCTBX_ARRAY_FAMILY_VERSA_H

#include <cctbx/array_family/versa_plain.h>

namespace cctbx { namespace af {

  template <typename ElementType,
            typename AccessorType = grid<1>,
            typename BaseArrayType = shared_plain<ElementType> >
  class versa : public versa_plain<ElementType, AccessorType, BaseArrayType>
  {
    public:
      typedef versa<ElementType, AccessorType, BaseArrayType> this_type;

      CCTBX_ARRAY_FAMILY_TYPEDEFS

      typedef BaseArrayType base_array_type;
      typedef versa_plain<ElementType, AccessorType, BaseArrayType> base_class;
      typedef typename base_class::handle_type handle_type;

      typedef AccessorType accessor_type;
      typedef typename accessor_type::index_type index_type;
      typedef versa<ElementType> one_dim_type;
      typedef typename one_dim_type::accessor_type one_dim_accessor_type;

      versa()
      {}

      explicit
      versa(const AccessorType& ac)
        : base_class(ac)
      {}

      versa(const AccessorType& ac, reserve_flag)
        : base_class(ac, reserve_flag())
      {}

      explicit
      versa(long n0)
        : base_class(n0)
      {}

      versa(const AccessorType& ac, const ElementType& x)
        : base_class(ac, x)
      {}

      versa(long n0, const ElementType& x)
        : base_class(n0, x)
      {}

#if !(defined(BOOST_MSVC) && BOOST_MSVC <= 1200) // VC++ 6.0
      // non-std
      template <typename InitFunctorType>
      versa(const AccessorType& ac, InitFunctorType ftor)
        : base_class(ac, ftor)
      {}

      // non-std
      template <typename InitFunctorType>
      versa(long n0, InitFunctorType ftor)
        : base_class(n0, ftor)
      {}
#endif

      versa(const base_class& other)
        : base_class(other)
      {}

      versa(const base_class& other, weak_ref_flag)
        : base_class(other, weak_ref_flag())
      {}

      versa(const base_array_type& other,
            const AccessorType& ac)
        : base_class(other, ac)
      {}

      versa(const base_array_type& other,
            long n0)
        : base_class(other, n0)
      {}

      versa(const base_array_type& other,
            const AccessorType& ac,
            const ElementType& x)
        : base_class(other, ac, x)
      {}

      versa(const base_array_type& other,
            long n0,
            const ElementType& x)
        : base_class(other, n0, x)
      {}

      versa(handle_type* other_handle, const AccessorType& ac)
        : base_class(other_handle, ac)
      {}

      versa(handle_type* other_handle, long n0)
        : base_class(other_handle, n0)
      {}

      versa(handle_type* other_handle, const AccessorType& ac,
                  const ElementType& x)
        : base_class(other_handle, ac)
      {}

      versa(handle_type* other_handle, long n0,
                  const ElementType& x)
        : base_class(other_handle, n0)
      {}

      one_dim_type as_1d() {
        return one_dim_type(*this, one_dim_accessor_type(this->size()));
      }

      this_type
      deep_copy() const {
        base_array_type c(this->begin(), this->end());
        return this_type(c, this->m_accessor);
      }

      this_type
      weak_ref() const {
        return this_type(*this, weak_ref_flag());
      }
  };

}} // namespace cctbx::af

#endif // CCTBX_ARRAY_FAMILY_VERSA_H
