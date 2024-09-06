'''
Created on Feb 19, 2019

@author: gravity
'''

class MyClass(object):
    '''
    classdocs
    '''


    def __init__(self, params):
        '''
        Constructor
        '''
    def getInitialStateVector(this)
    #[stateVectorObj,epochDataObj,health_flag]=
        # =================================================================
        '''            
        FUNCTION
           Computes the initial state vector.
         INPUTS
            
         OUTPUTS 
           stateVectorObj : instance of 'OrbStateVector' class including 
                            initial state vector parameters   
           epochDataObj   : instance of 'OrbEpochData' class including
                            observations and auxiliary data at initial
                            time of epoch
        '''
        # =================================================================               
        # Set auxiliary variables
        c = 299792458;          # speed of light in vacum (m/sec)
        lambda_L1=(c/1575.42e6); # wavelength of L1 carrier
        lambda_L2=(c/1227.60e6); # wavelength of L2 carrier
        # Initialize the state vector parameters
        position=[];velocity=[];
        atmDragCoef=[];solarRadCoef=[]; empAccel=[]; corelTime=[]; 
        recClcBias=[];recClcDrift=[]; recDriftRate = []; ambBias=[]; stateFateTime=[];        
        # Find the initial position and velocity
        # For Code and GRAPHIC observations
        if strcmp(this.filtSet.obsType,'Code') || \
            strcmp(this.filtSet.obsType,'Graphic') || strcmp(this.filtSet.obsType,'P1')|| \
            strcmp(this.filtSet.obsType,'C1-P2') || strcmp(this.filtSet.obsType,'P1-P2')||\
            strcmp(this.filtSet.obsType,'IFphase'): 
            # Read the data at first three epoch and compute the kinematic
            # position
            i=1;
            print('Filter Initialization') ##ok<NOPRT>
            while i<4
            # Read observation data
            if strcmp(this.filtSet.obsType,'Code'):
                if i ==2:
                    [orbEDobj{i},health_flag]= \
                        this.obsFileObj.getNextObs('Code',1);
                else:  [orbEDobj{i},health_flag]= \
                                       this.obsFileObj.getNextObs('Code',2);
                      end
              elseif strcmp(this.filtSet.obsType,'Graphic')
                      if i ==2
                          [orbEDobj{i},health_flag]= ...
                                       this.obsFileObj.getNextObs('Graphic',1); 
                      else
                          [orbEDobj{i},health_flag]= ...
                                       this.obsFileObj.getNextObs('Graphic',2);
                      end
              elseif strcmp(this.filtSet.obsType,'IFphase')
                  [orbEDobj{i},health_flag]= ...
                                       this.obsFileObj.getNextObs('IFphase',1);
                  
              elseif strcmp(this.filtSet.obsType,'P1')
             
                  if i ==2
                      [orbEDobj{i},health_flag]= ...
                                   this.obsFileObj.getNextObs('P1',1); 
                  else
                      [orbEDobj{i},health_flag]= ...
                                   this.obsFileObj.getNextObs('P1',2);
                  end
              elseif strcmp(this.filtSet.obsType,'C1-P2')
             
                  if i ==2
                      [orbEDobj{i},health_flag]= ...
                                   this.obsFileObj.getNextObs('C1-P2',1); 
                  else
                      [orbEDobj{i},health_flag]= ...
                                   this.obsFileObj.getNextObs('C1-P2',2);
                  end
               elseif strcmp(this.filtSet.obsType,'P1-P2')
             
                  if i ==2
                      [orbEDobj{i},health_flag]= ...
                                   this.obsFileObj.getNextObs('P1-P2',1); 
                  else
                      [orbEDobj{i},health_flag]= ...
                                   this.obsFileObj.getNextObs('P1-P2',2);
                  end
              end
                  if get(FateTime(orbEDobj{i}.epochFateTime),'MJD')<get(this.filtSet.beginFateTime,'MJD')
                      #disp(strcat('Search the observation file for the filter beginning,obs time:', ...
                                   #num2str(orbEDobj{i}.epochFateTime)))
                      continue;
                  end
                # Compute kinematic position
                  if health_flag==0 # Skip the unhealty data
                      if strcmp(this.filtSet.obsType,'Code') || strcmp(this.filtSet.obsType,'Graphic')
                          tic
                          [x{i},output]=this.kinematicPositioning(orbEDobj{i}.epochFateTime, ...
                                                      orbEDobj{i}.obs.C1,...
                                                      orbEDobj{i}.svn);
                         toc
                      elseif strcmp(this.filtSet.obsType,'IFphase')
                          tic
                          [x{i},output]=this.kinematicPositioning(orbEDobj{i}.epochFateTime, ...
                                                      orbEDobj{i}.obs.IFphase,...
                                                      orbEDobj{i}.svn);
                          toc
                      elseif strcmp(this.filtSet.obsType,'P1') 
                          [x{i},output]=this.kinematicPositioning(orbEDobj{i}.epochFateTime, ...
                                                      orbEDobj{i}.obs.P1,...
                                                      orbEDobj{i}.svn);
                      elseif strcmp(this.filtSet.obsType,'C1-P2')||...
                          strcmp(this.filtSet.obsType,'P1-P2')
                          [x{i},output]=this.kinematicPositioning(orbEDobj{i}.epochFateTime, ...
                                                      orbEDobj{i}.obs.ionof,...
                                                      orbEDobj{i}.svn);                            
                      end
                   i=i+1;
                  end
              end
              position=x{2}(1:3); stateFateTime=orbEDobj{2}.epochFateTime; 
              epochDataObj=orbEDobj{2}; 
              epochDataObj.gpsPos = output.GPS_pos;
              epochDataObj.gpsClcCorr = output.GPSclc_corr;
          # For Code and GRAPHIC observations              
           elseif strcmp(this.filtSet.obsType,'NavSol') 
                # Read observation data
              [orbEDobj,health_flag]= this.obsFileObj.getNextObs('NavSol',1);
           
                  position=orbEDobj.obs.NavSol(1:3);
                  velocity=orbEDobj.obs.NavSol(4:6);
                  epochDataObj=orbEDobj;    
                  stateFateTime=orbEDobj.epochFateTime; 
           else
               error('Observation type are not supported')              
           end
        # Compute velocity at second epoch by numerical difrentiation
          if strcmp(this.filtSet.obsType,'Code') || ...
             strcmp(this.filtSet.obsType,'Graphic') || ...
             strcmp(this.filtSet.obsType,'P1')||...
             strcmp(this.filtSet.obsType,'C1-P2') || ...
             strcmp(this.filtSet.obsType,'P1-P2') || ...
             strcmp(this.filtSet.obsType,'IFphase')
             # Convert the time into second and normalized 
               epo1=FateTime(orbEDobj{1}.epochFateTime);
               epo2=FateTime(orbEDobj{2}.epochFateTime);
               epo3=FateTime(orbEDobj{3}.epochFateTime);
               t3s=minus(epo3,epo1);t2s=minus(epo2,epo1);t1s=minus(epo1,epo1);
             # Use numerical difrentiation to compute velocity at middle point
               v=this.numDiffSOLag(t1s,t2s,t3s,x{1}(1:3,1),x{2}(1:3,1),x{3}(1:3,1),t2s); 
               velocity=v; 
          end
        # Set Dynamic Model Parameters
          if (this.filtSet.enableDynModParam==1) || ...
             (this.filtSet.enableDynModParam==2)
             # Set Initial atmospheric drag coefficient
               atmDragCoef=this.filtSet.initVal.atmDragCoef(:);
             # Set Initial solar radiation coefficient
                solarRadCoef=this.filtSet.initVal.solarRadCoef(:);
             # Set empirical accelerations
               empAccel=this.filtSet.initVal.empAccel(:);
             # Set Markov process corelletaion time
              if (this.filtSet.enableDynModParam==2)
                 corelTime=this.filtSet.initVal.corelTime(:);
              end
          end
        # Set Measurement Model Parameters
          if strcmp(this.filtSet.obsType,'Code') || ...
             strcmp(this.filtSet.obsType,'Graphic') || ...
             strcmp(this.filtSet.obsType,'P1')|| ...
             strcmp(this.filtSet.obsType,'C1-P2') || ...
             strcmp(this.filtSet.obsType,'P1-P2')|| ...
             strcmp(this.filtSet.obsType,'IFphase')
             # Set the receiver clock bias
               recClcBias= x{2}(4); 
               if this.filtSet.stat.std.procNoise.recClcDrift
                 recClcDrift= x{2}(5);
                 recDriftRate= x{2}(6);
               end
             # Compute the initial ambiguity bias for 'Graphic' observables
               if strcmp(this.filtSet.obsType,'Graphic')
                  # (Code range - Phase Range) 
                    ambBias=(orbEDobj{2}.obs.C1-(orbEDobj{2}.obs.L1*lambda_L1))./2;
               elseif strcmp(this.filtSet.obsType,'IFphase')
                  ambBias1=(orbEDobj{2}.obs.P1-(orbEDobj{2}.obs.L1*lambda_L1))./2; 
                  ambBias2=(orbEDobj{2}.obs.P2-(orbEDobj{2}.obs.L2*lambda_L2))./2; 
                  ambBias = (ambBias1+ambBias2)/2;
               end
                   
                   
          end
        # Set the initial covariance matrix
           std_diag=[];
          # Set covariance matrix for position and velocity
            std_diag=[ std_diag; this.filtSet.stat.std.init.posXYZ(:); ...
                                 this.filtSet.stat.std.init.velXYZ(:)];
          # Set covariance matrix for dynamic model parameters
            if (this.filtSet.enableDynModParam==1) || ...
               (this.filtSet.enableDynModParam==2)                    
                std_diag=[ std_diag; this.filtSet.stat.std.init.atmDragCoeff(:); ...
                                     this.filtSet.stat.std.init.solarRadCoeff(:); ...
                                     this.filtSet.stat.std.init.empAccellRTN(:) ];
                if (this.filtSet.enableDynModParam==2)
                   std_diag=[ std_diag; this.filtSet.stat.std.init.corelTime(:)];
                end
            end
          # Set covariance matrix for measurement model parameters
            if strcmp(this.filtSet.obsType,'Code') || ...
               strcmp(this.filtSet.obsType,'Graphic')|| ...
               strcmp(this.filtSet.obsType,'P1')|| ...
               strcmp(this.filtSet.obsType,'C1-P2') || ...
               strcmp(this.filtSet.obsType,'P1-P2') || ...
               strcmp(this.filtSet.obsType,'IFphase')
                if this.filtSet.stat.std.procNoise.recClcDrift
                   std_diag=[std_diag;this.filtSet.stat.std.init.recClcBias(:);...
                       this.filtSet.stat.std.init.recClcDrift(:);this.filtSet.stat.std.init.recDriftRate(:)];
                else
                  std_diag=[std_diag;this.filtSet.stat.std.init.recClcBias(:)];
                end
               if strcmp(this.filtSet.obsType,'Graphic')|| ...
                       strcmp(this.filtSet.obsType,'IFphase')
                  std_diag=[std_diag;ones(length(ambBias),1)* ...
                            this.filtSet.stat.std.init.ambiguityBias(:)];
               end
            end
          # Set the whole covariance matrix
            P=diag(std_diag.^2);
        # Create an instance of 'OrbStateVector' class to store variables
          # Store the state parameters
          if this.filtSet.stat.std.procNoise.recClcDrift
            stateVectorObj=OrbStateVector(position,velocity,atmDragCoef, ...
                                          solarRadCoef, empAccel,corelTime, ...
                                          recClcBias,recClcDrift,recDriftRate, ambBias, stateFateTime);
          else
           stateVectorObj=OrbStateVector(position,velocity,atmDragCoef, ...
                                          solarRadCoef, empAccel,corelTime, ...
                                          recClcBias, ambBias, stateFateTime);
          end
          # Store the covariance matrix
           stateVectorObj.stateCov=P;
        end