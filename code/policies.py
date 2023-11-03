class senate:
    def __init__(self, ds, fem_dict,
                 study_ = 'beam'):
        self.study_ = study_ 
        # dfsk = ds.Sketches
        self.A = ds.Sketches
        self.Xr_mean  = ds.Sketches.mean()
        self.Xr_range = ds.Sketches.max()-ds.Sketches.min()
        self.dfsk     = ds.Sketches
        self.fem_dict = fem_dict
      def sigma_greedy(self, 
                     gamma_ = 0.45,
                     metric_set = 'S.Max.', # S.Mises
                     logging_get = False,):
        '''
        

        Parameters
        ----------
        gamma_ : TYPE, optional
            DESCRIPTION. The default is 0.45.
        metric_set : TYPE, optional
            DESCRIPTION. The default is 'S.Max.'.
        # S.Mises                     logging_get : TYPE, optional
            DESCRIPTION. The default is False.
        
        Returns
        -------
        df_res : TYPE
            DESCRIPTION.

        '''
        N = 100
        self.policy_name = 'sigma-conservative'
        id_ = np.random.randint(1,99) # id pro expr_i.
        df_res = pd.DataFrame(data= np.zeros([N,5]), 
                              columns=['eps', 'sigma', 'status', 'policy type' , 'gamma']
                              )
        
        if logging_get: logging.basicConfig(filename=f'../logs_b/app_{id_}.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
        
        plen = self.dfsk.shape[1]
        gamma = gamma_
        # sigma_seek = 100
        s = 10000
        eps = 9000
        
        
        
        for i in range(N):
            if s > eps: # 'Explore'
                j = np.random.choice(2,plen)
                msg, status_ = 'Explore', 1
            else: 
                j = j
                # tady by melo byt neco jako q table
                msg, status_ = 'Exploit', 0
                eps = s
            
            
            x = self.Xr_mean + np.random.randn(plen) * j * self.Xr_range * gamma
            x = x.round(2)
    
            tree = spatial.KDTree(self.dfsk)
            tq = tree.query(x)
            id_dp = tq[1]
            x_ = self.A.iloc[ tree.query(x)[1] ]
        
            # sigma_ = self.fem_dict["DP-{:03d}".format(id_dp)]['S.MaxLoc11'].max()
            # sigma_ = fem_dict["DP-{:03d}".format(id_dp)]['S.MaxLoc10'].max()
            if self.study_ == 'beam':
                sigma_ = self.fem_dict["DP-{:03d}".format(id_dp)][metric_set].max()
            
            s = sigma_
            if sigma_ == 0: print("DP-{:03d}".format(id_dp))
            df_res.iloc[i,:] = [eps, s, status_, id_, gamma_]
            
            
            message_1 = f'tq: {tq[1]}, vals:{x_.values}'
            message_2 = str(sigma_)
            if logging_get:
                logging.warning([f'{message_2} \n {message_1} \n {msg}',
                                 '/n',
                                 f'update policy: {id_dp}, {msg}, {eps},  '
                                 ] 
                                 )
            
    
            # print(f'update policy: {id_dp}, {msg}, {eps},  ')
        return df_res                   
  def sigma_greedy_0(self, 
                     gamma_ = 0.45,
                     metric_set = 'S.Max.', # S.Mises
                     logging_get = False,):
        '''
        

        Parameters
        ----------
        gamma_ : TYPE, optional
            DESCRIPTION. The default is 0.45.
        metric_set : TYPE, optional
            DESCRIPTION. The default is 'S.Max.'.
        # S.Mises                     logging_get : TYPE, optional
            DESCRIPTION. The default is False.

        Returns
        -------
        df_res : TYPE
            DESCRIPTION.

        '''
        self.policy_name = 'sigma-explorer'
        N = 100
        id_ = np.random.randint(1,99) # id pro expr_i.
        df_res = pd.DataFrame(data= np.zeros([N,5]), 
                              columns=['eps', 'sigma', 'status', 'policy type' , 'gamma']
                              )
        
        if logging_get: logging.basicConfig(filename=f'../logs_b/app_{id_}.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
        
        plen = self.dfsk.shape[1]
        gamma = gamma_
        s = 10000
        eps = 9000
        
        
        x = self.Xr_mean 
        for i in range(N):
            if s > eps: # 'Explore'
                j = np.random.choice(2,plen)
                msg, status_ = 'Explore', 1
            else: 
                j = j
                # tady by melo byt neco jako q table
                msg, status_ = 'Exploit', 0
                eps = s
                        
            x = (x + np.random.randn(plen) * j * self.Xr_range * gamma ).round(2)

            tree = spatial.KDTree(self.dfsk)
            tq = tree.query(x)
            id_dp = tq[1]
            x_ = self.A.iloc[ tree.query(x)[1] ]
        
            # sigma_ = self.fem_dict["DP-{:03d}".format(id_dp)]['S.MaxLoc11'].max()
            # sigma_ = fem_dict["DP-{:03d}".format(id_dp)]['S.MaxLoc10'].max()
            if self.study_ == 'beam':
                sigma_ = self.fem_dict["DP-{:03d}".format(id_dp)][metric_set].max()
            
            s = sigma_
            if sigma_ == 0: print("DP-{:03d}".format(id_dp))
            df_res.iloc[i,:] = [eps, s, status_, id_, gamma_]
      return df_res
