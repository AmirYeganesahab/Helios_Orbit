'''
Created on Mar 13, 2019

@author: geomatics
'''
import numpy as np
import sys
from functools import reduce
class poly( ):
    
    def __init__(self, x ,y, order, fetch = 'statisticalNormalize' ):
        self.x = x
        self.y = y
        self.N = order
        self.fetch = fetch
    
    '''
        %POLYFIT Fit polynomial to data.
        %   P = POLYFIT(X,Y,N) finds the coefficients of a polynomial P(X) of
        %   degree N that fits the data Y best in a least-squares sense. P is a
        %   row vector of length N+1 containing the polynomial coefficients in
        %   descending powers, P(1)*X^N + P(2)*X^(N-1) +...+ P(N)*X + P(N+1).
        %
        %   [P,S] = POLYFIT(X,Y,N) returns the polynomial coefficients P and a
        %   structure S for use with POLYVAL to obtain error estimates for
        %   predictions.  S contains fields for the triangular factor (R) from a QR
        %   decomposition of the Vandermonde matrix of X, the degrees of freedom
        %   (df), and the norm of the residuals (normr).  If the data Y are random,
        %   an estimate of the covariance matrix of P is (Rinv*Rinv')*normr^2/df,
        %   where Rinv is the inverse of R.
        %
        %   [P,S,MU] = POLYFIT(X,Y,N) finds the coefficients of a polynomial in
        %   XHAT = (X-MU(1))/MU(2) where MU(1) = MEAN(X) and MU(2) = STD(X). This
        %   centering and scaling transformation improves the numerical properties
        %   of both the polynomial and the fitting algorithm.
        %
        %   Warning messages result if N is >= length(X), if X has repeated, or
        %   nearly repeated, points, or if X might need centering and scaling.
        %
        %   Example: simple linear regression with polyfit
        %
        %     % Fit a polynomial p of degree 1 to the (x,y) data:
        %       x = 1:50;
        %       y = -0.3*x + 2*randn(1,50);
        %       p = polyfit(x,y,1);
        %
        %     % Evaluate the fitted polynomial p and plot:
        %       f = polyval(p,x);
        %       plot(x,y,'o',x,f,'-')
        %       legend('data','linear fit')
        %
        %   Class support for inputs X,Y:
        %      float: double, single
    '''
    def back_substitution(self, A: np.ndarray, b: np.ndarray) -> np.ndarray:
        n = b.size
        x = np.zeros_like(b)
        if A[n-1, n-1] == 0:
            raise ValueError
        for i in range(n-1, 0, -1):
            x[i] = A[i, i]/b[i]
            for j in range (i-1, 0, -1):
                A[i, i] += A[j, i]*x[i]
        return x
    def warnIfLargeConditionNumber(self,R):
        if isinstance(R, (float, int)):
            flag = (np.linalg.cond(R) > 1e+10);
        else:
            flag = (np.linalg.cond(R) > 1e+05);
        return flag
    def fit(self):
        if len(self.x)!= len(self.y):
            raise AttributeError('XY Size Mismatch')
        if self.fetch is 'statisticalNormalize':
            mu = [np.mean(self.x), np.std(self.x, ddof = 1)]
            x = (self.x - mu[0])/mu[1]
        else:
            mu = None
        # Construct the Vandermonde matrix V = [x.^n ... x.^2 x ones(size(x))]
        V = np.vander(x,self.N+1)
        # Solve least squares problem p = V\y to get polynomial coefficients p.
        Q,R = np.linalg.qr(V)
        # Rx = Q'y
        b = np.dot(np.transpose(Q),self.y)
        #back substitution
        if np.linalg.matrix_rank(R) == len(x):
            par = np.linalg.lstsq(R, b, 17)
            par = np.linalg.lstsq(V, x, 17)
        else:
            raise ValueError('rank deff')
        reduce(np.dot,[np.transpose(R),R,np.transpose(R),b])
        # Issue warnings.
        if np.shape(R)[1] > np.shape(R)[0]:
            raise Warning('polyfit:PolyNotUnique')

        S = {}
        r = self.y - np.dot(V,parameters)
        # S is a structure containing three elements: the triangular factor
        # from a QR decomposition of the Vandermonde matrix, the degrees of
        # freedom and the norm of the residuals.
        S['R'] = R
        S['df'] = max(0,len(self.y) - (self.N+1))
        S['normr'] = np.linalg.norm(r)
    
        return parameters, S, mu