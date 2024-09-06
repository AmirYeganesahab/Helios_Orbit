'''
Created on Feb 23, 2019

@author: geomatics
'''

class kinematic(object):
    '''
    classdocs
    '''


    def __init__(self, params):
        '''
        Constructor
        '''
        pass
    def getGpsSatParam(this,t,x,sv_no,recClcBias):
        # outputs: [GPS_pos,GPSclc_corr,GPS_Tgd]
        # ==================================================================
        '''                                           
        # FUNCTION
        #   Computes the GPS position and GPS satellite clock error at
        #   signal transmission time via  light time iteration
        # INPUTS
        #   epoch : epoch number
        #   t     : receiver date and time, (GPS time)
        #   x     : receiver position vector
        #   sv_no : satellite vehicle number
        #   recClcBias : receiver clock bias
        # OUTPUTS
        #   GPS_pos     : GPS positions for given satellites, [m]
        #   GPSclc_corr : GPS clock cprrections for given satellites, [m]
        #   GPS_Tgd     : Intrumental delays for given satellites, [m]
        '''
        # ==================================================================

        # Set Constants
        Omegae = 7.292115147e-5;  # Earth rotation rate (rad/sec)
        c=299792458;              # speed of light 
        # Check the file
        epo = FateTime(t) - recClcBias/c;
        if isnumeric(this.current_t):
            this.loadObsFile(epo)
        elif (floor(get(this.current_t,'MJD')) != floor(get(epo,'MJD'))):             
            this.loadObsFile(epo)
                  
        # Compute GPS satellite coordinates using light time iteration
        
        tau0=0.072*ones(length(sv_no),1);
        
        for i=1:length(sv_no)
           d_p=1;
           while d_p>0.0001
              # Approimate transmition time
                epo_trans=minus(epo,tau0(i));  
              # Get GPS satellite coordinates
                coordsBr = GetSatCoord(this.brdEphData,sv_no(i),epo_trans);
                GPS_pos(1,i)=coordsBr.x;
                GPS_pos(2,i)=coordsBr.y;
                GPS_pos(3,i)=coordsBr.z;
                GPSclc_corr(i,1)=coordsBr.dt;
                GPS_Tgd(i,1)=coordsBr.Tgd;
              # Earth rotation correction
                omegae_dot_dt = Omegae*tau0(i);  
                R3 = [  cos(omegae_dot_dt)   sin(omegae_dot_dt) 0;
                        -sin(omegae_dot_dt)  cos(omegae_dot_dt) 0;
                        0                    0                  1];
                GPS_pos(:,i)=R3*GPS_pos(:,i);
              # Compute Geometric range
                p=sqrt((power(GPS_pos(1,i)-x(1),2)+ ...
                        power(GPS_pos(2,i)-x(2),2)+ ...
                        power(GPS_pos(3,i)-x(3),2)));
              # Compute new time delay
                tau=p/c;
                d_p=abs(c*(tau-tau0(i)));
                tau0(i)=tau;
           end
        end
        # Compute the return values
        GPS_pos=GPS_pos';           # GPS Satellite position    
        GPSclc_corr=GPSclc_corr.*c; # GPS Satellite clock correction 
        GPS_Tgd=c*GPS_Tgd*0;          # GPS instrumental delay
        end