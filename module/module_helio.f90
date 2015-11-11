!**********************************************************************************************************************************
!
!  Unit Name   : module_helio
!  Unit Type   : module
!  Project     : SWIFTER
!  Package     : module
!  Language    : Fortran 90/95
!
!  Description : Definition of data and structures specific to the Democratic Heliocentric Method
!
!  Input
!    Arguments : N/A
!    Terminal  : N/A
!    File      : N/A
!
!  Output
!    Arguments : N/A
!    Terminal  : N/A
!    File      : N/A
!
!  Invocation  : N/A
!
!  Notes       : 
!
!**********************************************************************************************************************************
MODULE module_helio

     USE module_parameters
     USE module_swifter
     IMPLICIT NONE

     TYPE helio_pl
          REAL(DP), DIMENSION(NDIM) :: ah       ! total heliocentric acceleration
          REAL(DP), DIMENSION(NDIM) :: ahi      ! heliocentric acceleration due to interactions
          TYPE(swifter_pl)          :: swifter  ! SWIFTER planet structure
          TYPE(helio_pl), POINTER   :: prevP    ! pointer to previous HELIO planet
          TYPE(helio_pl), POINTER   :: nextP    ! pointer to next HELIO planet
     END TYPE helio_pl

     TYPE helio_tp
          REAL(DP), DIMENSION(NDIM) :: ah       ! total heliocentric acceleration
          REAL(DP), DIMENSION(NDIM) :: ahi      ! heliocentric acceleration due to interactions
          TYPE(swifter_tp)          :: swifter  ! SWIFTER test particle structure
          TYPE(helio_tp), POINTER   :: prevP    ! pointer to previous HELIO test particle
          TYPE(helio_tp), POINTER   :: nextP    ! pointer to next HELIO test particle
     END TYPE helio_tp

END MODULE module_helio
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
