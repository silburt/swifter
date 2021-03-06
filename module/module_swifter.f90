!**********************************************************************************************************************************
!
!  Unit Name   : module_swifter
!  Unit Type   : module
!  Project     : SWIFTER
!  Package     : module
!  Language    : Fortran 90/95
!
!  Description : Definition of data and structures generic to all integrators
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
MODULE module_swifter

     USE module_parameters
     IMPLICIT NONE

     TYPE swifter_pl
          INTEGER(I4B)              :: id     ! external identifier
          INTEGER(I4B)              :: status ! status
          REAL(DP)                  :: mass   ! mass
          REAL(DP)                  :: radius ! radius
          REAL(DP)                  :: rhill  ! Hill's sphere radius
          REAL(DP), DIMENSION(NDIM) :: xh     ! heliocentric position
          REAL(DP), DIMENSION(NDIM) :: vh     ! heliocentric velocity
          REAL(DP), DIMENSION(NDIM) :: xb     ! barycentric position
          REAL(DP), DIMENSION(NDIM) :: vb     ! barycentric velocity
          TYPE(swifter_pl), POINTER :: prevP  ! pointer to previous planet
          TYPE(swifter_pl), POINTER :: nextP  ! pointer to next planet
     END TYPE swifter_pl

     TYPE swifter_tp
          INTEGER(I4B)              :: id     ! external identifier
          INTEGER(I4B)              :: status ! status
          INTEGER(I4B)              :: isperi ! perihelion passage flag
          REAL(DP)                  :: peri   ! perihelion distance
          REAL(DP)                  :: atp    ! semimajor axis following perihelion passage
          REAL(DP), DIMENSION(NDIM) :: xh     ! heliocentric position
          REAL(DP), DIMENSION(NDIM) :: vh     ! heliocentric velocity
          REAL(DP), DIMENSION(NDIM) :: xb     ! barycentric position
          REAL(DP), DIMENSION(NDIM) :: vb     ! barycentric velocity
          TYPE(swifter_tp), POINTER :: prevP  ! pointer to previous test particle
          TYPE(swifter_tp), POINTER :: nextP  ! pointer to next test particle
     END TYPE swifter_tp

END MODULE module_swifter
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
