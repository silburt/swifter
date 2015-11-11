!**********************************************************************************************************************************
!
!  Unit Name   : helio_lindrift
!  Unit Type   : subroutine
!  Project     : Swifter
!  Package     : helio
!  Language    : Fortran 90/95
!
!  Description : Perform linear drift of planets due to barycentric momentum of Sun
!
!  Input
!    Arguments : npl          : number of planets
!                swifter_pl1P : pointer to head of Swifter planet structure linked-list
!                dt           : time step
!    Terminal  : none
!    File      : none
!
!  Output
!    Arguments : swifter_pl1P : pointer to head of Swifter planet structure linked-list
!                pt           : negative barycentric velocity of the Sun
!    Terminal  : none
!    File      : none
!
!  Invocation  : CALL helio_lindrift(npl, swifter_pl1P, dt, pt)
!
!  Notes       : Adapted from Hal Levison's Swift routine helio_lindrift.f
!
!**********************************************************************************************************************************
SUBROUTINE helio_lindrift(npl, swifter_pl1P, dt, pt)

! Modules
     USE module_parameters
     USE module_swifter
     USE module_interfaces, EXCEPT_THIS_ONE => helio_lindrift
     IMPLICIT NONE

! Arguments
     INTEGER(I4B), INTENT(IN)               :: npl
     REAL(DP), INTENT(IN)                   :: dt
     REAL(DP), DIMENSION(NDIM), INTENT(OUT) :: pt
     TYPE(swifter_pl), POINTER              :: swifter_pl1P

! Internals
     INTEGER(I4B)              :: i
     TYPE(swifter_pl), POINTER :: swifter_plP

! Executable code
     pt(:) = (/ 0.0_DP, 0.0_DP, 0.0_DP /)
     swifter_plP => swifter_pl1P
     DO i = 2, npl
          swifter_plP => swifter_plP%nextP
          pt(:) = pt(:) + swifter_plP%mass*swifter_plP%vb(:)
     END DO
     pt(:) = pt(:)/swifter_pl1P%mass
     swifter_plP => swifter_pl1P
     DO i = 2, npl
          swifter_plP => swifter_plP%nextP
          swifter_plP%xh(:) = swifter_plP%xh(:) + pt(:)*dt
     END DO

     RETURN

END SUBROUTINE helio_lindrift
!**********************************************************************************************************************************
!
!  Author(s)   : David E. Kaufmann
!
!  Revision Control System (RCS) Information
!
!  Source File : $RCSfile$
!  Full Path   : $Source$
!  Revision    : $Revision$
!  Date        : $Date$
!  Programmer  : $Author$
!  Locked By   : $Locker$
!  State       : $State$
!
!  Modification History:
!
!  $Log$
!**********************************************************************************************************************************
