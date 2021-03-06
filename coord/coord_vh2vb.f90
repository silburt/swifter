!**********************************************************************************************************************************
!
!  Unit Name   : coord_vh2vb
!  Unit Type   : subroutine
!  Project     : Swifter
!  Package     : coord
!  Language    : Fortran 90/95
!
!  Description : Convert from heliocentric to barycentric coordinates, planet velocities only
!
!  Input
!    Arguments : npl          : number of planets
!                swifter_pl1P : pointer to head of Swifter planet structure linked-list
!    Terminal  : none
!    File      : none
!
!  Output
!    Arguments : swifter_pl1P : pointer to head of Swifter planet structure linked-list
!                msys         : total system mass
!    Terminal  : none
!    File      : none
!
!  Invocation  : CALL coord_vh2vb(npl, swifter_pl1P, msys)
!
!  Notes       : Adapted from Hal Levison's Swift routine coord_vh2b.f
!
!**********************************************************************************************************************************
SUBROUTINE coord_vh2vb(npl, swifter_pl1P, msys)

! Modules
     USE module_parameters
     USE module_swifter
     USE module_interfaces, EXCEPT_THIS_ONE => coord_vh2vb
     IMPLICIT NONE

! Arguments
     INTEGER(I4B), INTENT(IN)  :: npl
     REAL(DP), INTENT(OUT)     :: msys
     TYPE(swifter_pl), POINTER :: swifter_pl1P

! Internals
     INTEGER(I4B)              :: i
     REAL(DP), DIMENSION(NDIM) :: vtmp
     TYPE(swifter_pl), POINTER :: swifter_plP

! Executable code
     swifter_plP => swifter_pl1P
     msys = swifter_plP%mass
     vtmp(:) = (/ 0.0_DP, 0.0_DP, 0.0_DP /)
     DO i = 2, npl
          swifter_plP => swifter_plP%nextP
          msys = msys + swifter_plP%mass
          vtmp(:) = vtmp(:) + swifter_plP%mass*swifter_plP%vh(:)
     END DO
     swifter_plP => swifter_pl1P
     swifter_plP%vb(:) = -vtmp(:)/msys
     vtmp(:) = swifter_plP%vb(:)
     DO i = 2, npl
          swifter_plP => swifter_plP%nextP
          swifter_plP%vb(:) = swifter_plP%vh(:) + vtmp(:)
     END DO

     RETURN

END SUBROUTINE coord_vh2vb
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
