!**********************************************************************************************************************************
!
!  Unit Name   : coord_vb2vh
!  Unit Type   : subroutine
!  Project     : Swifter
!  Package     : coord
!  Language    : Fortran 90/95
!
!  Description : Convert from barycentric to heliocentric coordinates, planet velocities only
!
!  Input
!    Arguments : npl          : number of planets
!                swifter_pl1P : pointer to head of Swifter planet structure linked-list
!    Terminal  : none
!    File      : none
!
!  Output
!    Arguments : swifter_pl1P : pointer to head of Swifter planet structure linked-list
!    Terminal  : none
!    File      : none
!
!  Invocation  : CALL coord_vb2vh(npl, swifter_pl1P)
!
!  Notes       : Adapted from Hal Levison's Swift routine coord_vb2h.f
!
!**********************************************************************************************************************************
SUBROUTINE coord_vb2vh(npl, swifter_pl1P)

! Modules
     USE module_parameters
     USE module_swifter
     USE module_interfaces, EXCEPT_THIS_ONE => coord_vb2vh
     IMPLICIT NONE

! Arguments
     INTEGER(I4B), INTENT(IN)  :: npl
     TYPE(swifter_pl), POINTER :: swifter_pl1P

! Internals
     INTEGER(I4B)              :: i
     REAL(DP), DIMENSION(NDIM) :: vtmp
     TYPE(swifter_pl), POINTER :: swifter_plP

! Executable code
     vtmp(:) = (/ 0.0_DP, 0.0_DP, 0.0_DP /)
     swifter_plP => swifter_pl1P
     DO i = 2, npl
          swifter_plP => swifter_plP%nextP
          vtmp(:) = vtmp(:) - swifter_plP%mass*swifter_plP%vb(:)
     END DO
     vtmp(:) = vtmp(:)/swifter_pl1P%mass
     swifter_pl1P%vb(:) = vtmp(:)
     swifter_plP => swifter_pl1P
     DO i = 2, npl
          swifter_plP => swifter_plP%nextP
          swifter_plP%vh(:) = swifter_plP%vb(:) - vtmp(:)
     END DO

     RETURN

END SUBROUTINE coord_vb2vh
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
