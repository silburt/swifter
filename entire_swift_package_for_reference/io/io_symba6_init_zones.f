c************************************************************************
c                          IO_SYMBA6_INIT_ZONES.F
c************************************************************************
c
c  Purpose:  This subroutine reads in the number or radial and 
c            azimuthal zones for the encounter search algorithm from
c            a file. 
c
c  Input:    inznfile    ==>  The zone input file
c
c  Output:   nrz        ==>  Number of radial search zones  
c            naz        ==>  Number of azimuthal search zones  
c            nsect      ==>  Total number of sectors
c                             (both are integer scalars)
c
c  Author:  cba
c  Date:    3/2/99
c  Last Modified:

      subroutine io_symba6_init_zones(inznfile,nrz,naz,nsect)

      include 'io.inc'
      include '../symba6/symba6.inc'

c.. Inputs
      character*(*) inznfile

c.. Outputs
      integer nrz,naz,nsect

c.. Executable code

      call io_open(7,inznfile,'old','formatted',ierr)

      read(7,*) nrz, naz

      write(*,*) 'Number of radial search zones:    ', nrz
      write(*,*) 'Number of azimuthal search zones: ', naz

      if( (naz .lt. 1) .or. (nrz .lt. 3)) then
          write(*,*) ' '
          write(*,*) 'The number of radial zones ',
     &               'must be greater than 3!!!'
          write(*,*) 'The number of azimuthal zones ',
     &               'must be greater than 0!!!'
          write(*,*) ' '
          write(*,*) ' naz = ',naz,'  nrz = ',nrz
          call util_exit(1)
      endif

      nsect = nrz*naz

      write(*,*) 'Total number of search sectors:  ',nsect

      if (nsect .gt. NSECTMAX) then
          write(*,*) ' '
          write(*,*) 'The number of sectors is greater than NSECTMAX!!!'
          write(*,*) ' '
          write(*,*) 'NSECTMAX = ',NSECTMAX
          write(*,*)
          call util_exit(1)
      endif


      close(unit=7)

      return
      end                ! io_symba6_init_zones
c------------------------------------------------------------------------
