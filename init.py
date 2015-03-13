PrimKeys={'PAR': [['par_pk','id']],
          'BUD': [['bud_pk','id']],
          'CABU': [['ak_cb_pk','bud_id','typbud_kod','cislo_domovni']],
          'ZPOCHN': [['zpochn_pk','kod']],
          'DRUPOZ': [['drupoz_pk','kod']],
          'ZPVYPO': [['zpvypo_pk','kod']],
          'ZDPAZE': [['zdpaze_pk','kod']],
          'ZPURVY': [['zpurvy_pk','kod']],
          'TYPBUD': [['typbud_pk','kod']],
          'MAPLIS': [['maplis_pk','id']],
          'KATUZE': [['katuze_pk','kod']],
          'OBCE': [['obce_pk','kod']],
          'CASOBC': [['caobce_pk','kod']],
          'OKRESY': [['okresy_pk','kod']],
          'KRAJE': [['sc_kraje_pk','kod']],
          'RZO': [['rzo_pk','id']],
          'ZPVYBU': [['zpvybu_pk','kod']],
          'JED': [['jed_pk','id']],
          'TYPJED': [['typjed_pk','kod']],
          'ZPVYJE': [['zpvyje_pk','kod']],
          'BDP': [['bdp_pk','par_id','bpej_kod']],
          'OPSUB': [['opsub_pk','id']],
          'VLA': [['vla_pk','id']],
          'CHAROS': [['charos_pk','kod']],
          'TEL': [['tel_pk','id']],
          'JPV': [['jpv_pk','id']],
          'TYPRAV': [['typrav_pk','kod']],
          'RIZENI': [['rizeni_pk','id']],
          'RIZKU': [['katriz_pk','rizeni_id','katuze_kod']],
          'OBJRIZ': [['objriz_pk','id']],
          'PRERIZ': [['preriz_pk','rizeni_id','typpre_kod']],
          'UCAST': [['ucast_pk','id']],
          'ADRUC': [['adruc_pk','ucast_id','typ_adresy']],
          'LISTIN': [['listin_pk','id']],
          'DUL': [['dul_pk','kod']],
          'LDU': [['lisdu_pk','listin_id','dul_kod']],
          'TYPLIS': [['typlis_pk','kod']],
          'TYPPRE': [['typpre_pk','kod']],
          'TYPRIZ': [['typriz_pk','kod']],
          'TYPUCA': [['typuca_pk','kod']],
          'UCTYP': [['uctyp_pk','ucast_id','typuca_kod']],
          'RL': [['rl_pk','id']],
          'OBESMF': [],
          'SOBR': [['sobr_pk','id']],
          'SBP': [['sbp_pk','id']],
          'SBM': [],
          'KODCHB': [['kodchb_pk','kod']],
          'TYPSOS': [['typos_pk','kod']],
          'HP': [['hp_pk','id']],
          'OP': [['op_pk','id']],
          'OB': [['ob_pk','id']],
          'DPM': [['dpm_pk','id']],
          'OBBP': [['obbp_pk','id']],
          'TYPPPD': [['typppd_pk','kod']],
          'HBPEJ': [['hbpej_pk','id']],
          'OBPEJ': [['obpej_pk','id']],
          'NZ': [['nz_pk','id']],
          'ZPMZ': [['zpmz_pk','katuze_kod','cislo_zpmz']],
          'NZZP': [['nzzp_pk','nz_id','zpmz_cislo_zpmz','zpmz_katuze_kod']],
          'SPOL': [['spol_pk','id']],
          }

          
#ForKeys={'SOBR': [['sobr_fk1','zpmz','katuze_kod','cislo_zpmz','katuze_kod','cislo_zpmz'],['sobr_fk2','kody_char_q_bodu','kodchb_kod','kod']],
#         'SBP': [['sbp_fk1','dalsi_prvky_mapy','dpm_id','id'],['sbp_fk2','hranice_parcel','hp_id','id'],['sbp_fk3','obrazy_budov','ob_id','id'],['sbp_fk4','souradnice_obrazu','bp_id','id']]
#         'SBM': [['sbm_fk1','dalsi_prvky_mapy','dpm_id'],['sbm_fk2','hranice_bpej','hbpej_id'],['sbm_fk3','obrazy_parcel','op_id']]
#         }

ForKeys={'PAR' : [['par_fk1','drupoz','drupoz_kod','kod'],['par_fk2','katuze','katuze_kod','kod'],['par_fk3','katuze','katuze_kod_puv','kod'],['par_fk4','maplis','maplis_kod','kod'],['par_fk5','zdpaze','zdpaze_kod','kod'],['par_fk6','tel','tel_id','id'],['par_fk7','zpurvy','zpurvy_kod','kod'],['par_fk8','zpvypo','zpvypa_kod','kod'],['par_fk9','pkn','pkn_id','id'],['par_fk10','rizeni','rizeni_id_vzniku','id'],['par_fk12','par','par_id','id'],['par_fk13','bud','bud_id','id']],
         'BUD' : [['bud_fk1','casobc','caobce_kod','kod'],['bud_fk2','typbud','typbud_kod','kod'],['bud_fk3','rizeni','rizeni_id_vzniku','id'],['bud_fk5','zpvybu','zpvybu_kod','kod'],['bud_fk6','tel','tel_id','id']],
         'CABU': [['ak_cb_fk1','bud','bud_id','id'],['ak_cb_fk2','typbud','typbud_kod','kod']],
         'DRUPOZ'  : [['drupoz_fk1','typppd','typppd_kod','kod']],
         'ZPVYPO'  : [['zpvypo_fk1','typppd','typppd_kod','kod']],
         'KATUZE'  : [['katuze_fk1','obce','obce_kod','kod']],
         'OBCE'  : [['obce_fk1','okresy','okresy_kod','kod']],
         'CASOBC'  : [['casobc_fk1','obce','obce_kod','kod']],
         'OKRESY'  : [['okresy_fk1','kraje','kraje_kod','kod']],
         'RZO'  : [['rzo_fk1','zpochn','zpochn_kod','kod'],['rzo_fk2','par','par_id','id'],['rzo_fk3','bud','bud_id','id'],['rzo_fk4','jed','jed_id','id']],
         'JED'  : [['jed_fk1','bud','bud_id','id'],['jed_fk2','typjed','typjed_kod','kod'],['jed_fk5','zpvyje','zpvyje_kod','kod'],['jed_fk6','tel','tel_id','id']],
         'BDP'  : [['bdp_fk2','par','par_id','id']],
         'OPSUB'  : [['opsub_fk1','charos','charos_kod','kod']],
         'VLA'  : [['vla_fk4','opsub','opsub_id','id'],['vla_fk5','tel','tel_id','id'],['vla_fk6','typrav','typrav_kod','kod']],
         'TEL'  : [['tel_fk1','katuze','katuze_kod','kod']],
         'JPV'  : [['jpv_fk1','bud','bud_id_k','id'],['jpv_fk2','bud','bud_id_pro','id'],['jpv_fk3','par','par_id_k','id'],['jpv_fk4','jed','jed_id_k','id'],['jpv_fk5','jed','jed_id_pro','id'],['jpv_fk6','opsub','opsub_id_pro','id'],['jpv_fk7','opsub','opsub_id_k','id'],['jpv_fk8','par','par_id_pro','id'],['jpv_fk9','typrav','typrav_kod','kod'],['jpv_fk11','tel','tel_id','id']],
         'TYPRAV'  : [['typrav_typpre_fk1','typpre','typpre_kod','kod']],
         'RIZENI'  : [['rizeni_typriz_fk3','typriz','typriz_kod','kod']],
         'RIZKU'  : [['katriz_katuze_fk2','katuze','katuze_kod','kod'],['katriz_riyeni_fk1','rizeni','rizeni_id','id']],
         'OBJRIZ'  : [['objriz_rizeni_fk1','rizeni','rizeni_id','id'],['objriz_budovy_fk2','bud','bud_id','id'],['objriz_parcely_fk3','par','par_id','id'],['objriz_jednotky_fk4','jed','jed_id','id']],
         'PRERIZ'  : [['preriz_rizeni_fk1','rizeni','rizeni_id','id'],['preriz_typred_fk2','typpre','typpre_kod','kod']],
         'UCAST'  : [['ucast_rizeni_fk1','rizeni','rizeni_id','id']],
         'ADRUC'  : [['adruc_ucast_fk1','ucast','ucast_id','id']],
         'LISTIN'  : [['listin_t_listin_fk1','typlis','typlis_kod','kod'],['listin_rizeni_fk2','rizeni','rizeni_id','id']],
         'LDU'  : [['lisdu_dul_fk1','dul','dul_kod','kod'],['lisdu_listin_fk2','listin','listin_id','id']],
         'UCTYP'  : [['uctyp_ucast_fk1','ucast','ucast_id','id'],['uctyp_typuca_fk2','typuca','typuca_kod','kod']],
         'RL'  : [['rl_fk1','listin','listin_id','id'],['rl_fk2','par','par_id','id'],['rl_fk3','bud','bud_id','id'],['rl_fk4','jed','jed_id','id'],['rl_fk5','opsub','opsub_id','id'],['rl_fk6','jpv','jpv_id','id']],
         'SOBR': [['sobr_fk1','zpmz','katuze_kod','katuze_kod','cislo_zpmz','cislo_zpmz'],['sobr_fk2','kody_char_q_bodu','kodchb_kod','kod']], 
         'SBP' : [['sbp_fk1','dpm','dpm_id','id'],['sbp_fk2','hp','hp_id','id'],['sbp_fk3','ob','ob_id','id'],['sbp_fk4','sobr','bp_id','id']],
         'SBM': [['sbm_fk1','dalsi_prvky_mapy','dpm_id'],['sbm_fk2','hranice_bpej','hbpej_id'],['sbm_fk3','obrazy_parcel','op_id']],
         'HP'  : [['hp_fk1','par','par_id_1','id'],['hp_fk2','par','par_id_2','id']],
         'OB'  : [['ob_fk1','bud','bud_id','id']],
         'OP'  : [['op_fk1','par','par_id','id']],
         'DPM' : [['dpm_fk1','sobr','bp_id','id']],
         'OBBP': [['obbp_fk1','sobr','bp_id','id']],         
         'NZ': [['nz_rizeni_fk','rizeni','rizeni_id','id']],         
         'ZPMZ': [['zpmz_katuze_fk2','katuze','katuze_kod','kod'],['zpmz_typsos_fk3','typsos','typsos_kod','kod']],         
}

user="postgres"
pas="961983"
