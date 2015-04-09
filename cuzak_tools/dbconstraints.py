
PrimKeys = {
    'PAR': ['id'],
    'BUD': ['id'],
    'CABU': ['bud_id','typbud_kod','cislo_domovni'],
    'ZPOCHN': ['kod'],
    'DRUPOZ': ['kod'],
    'ZPVYPO': ['kod'],
    'ZDPAZE': ['kod'],
    'ZPURVY': ['kod'],
    'TYPBUD': ['kod'],
    'MAPLIS': ['id'],
    'KATUZE': ['kod'],
    'OBCE': ['kod'],
    'CASOBC': ['kod'],
    'OKRESY': ['kod'],
    'KRAJE': ['kod'],
    'RZO': ['id'],
    'ZPVYBU': ['kod'],
    'JED': ['id'],
    'TYPJED': ['kod'],
    'ZPVYJE': ['kod'],
    'BDP': ['par_id','bpej_kod'],
    'OPSUB': ['id'],
    'VLA': ['id'],
    'CHAROS': ['kod'],
    'TEL': ['id'],
    'JPV': ['id'],
    'TYPRAV': ['kod'],
    'RIZENI': ['id'],
    'RIZKU': ['rizeni_id','katuze_kod'],
    'OBJRIZ': ['id'],
    'PRERIZ': ['rizeni_id','typpre_kod'],
    'UCAST': ['id'],
    'ADRUC': ['ucast_id','typ_adresy'],
    'LISTIN': ['id'],
    'DUL': ['kod'],
    'LDU': ['listin_id','dul_kod'],
    'TYPLIS': ['kod'],
    'TYPPRE': ['kod'],
    'TYPRIZ': ['kod'],
    'TYPUCA': ['kod'],
    'UCTYP': ['ucast_id','typuca_kod'],
    'RL': ['id'],
#     'OBESMF': [],
    'SOBR': ['id'],
    'SBP': ['id'],
    # NOTE: op_id jsem mel null a tim padem nesli ty data pridat
    # tak uz neni primarni klic ...
    # to same pro dpm_id,
    # predpokladam, ze i pro ostatni krom poradove_cislo_bodu
    # takze nema smysl mit pro SBM info o primarnich klicich 
#     'SBM': ['poradove_cislo_bodu', 'dpm_id', 'hbpej_id'], # 'op_id'],
    'KODCHB': ['kod'],
    'TYPSOS': ['kod'],
    'HP': ['id'],
    'OP': ['id'],
    'OB': ['id'],
    'DPM': ['id'],
    'OBBP': ['id'],
    'TYPPPD': ['kod'],
    'HBPEJ': ['id'],
    'OBPEJ': ['id'],
    'NZ': ['id'],
    'ZPMZ': ['katuze_kod','cislo_zpmz'],
    'NZZP': ['nz_id','zpmz_cislo_zpmz','zpmz_katuze_kod'],
    'SPOL': ['id'],
}


#ForKeys={'SOBR': [['sobr_fk1','zpmz','katuze_kod','cislo_zpmz','katuze_kod','cislo_zpmz'],['sobr_fk2','kody_char_q_bodu','kodchb_kod','kod'],
#         'SBP': [['sbp_fk1','dalsi_prvky_mapy','dpm_id','id'],['sbp_fk2','hranice_parcel','hp_id','id'],['sbp_fk3','obrazy_budov','ob_id','id'],['sbp_fk4','souradnice_obrazu','bp_id','id']
#         'SBM': [['sbm_fk1','dalsi_prvky_mapy','dpm_id'],['sbm_fk2','hranice_bpej','hbpej_id'],['sbm_fk3','obrazy_parcel','op_id']
#         }

ForKeys = {
    'PAR' : [
        ('drupoz','drupoz_kod','kod'),
        ('katuze','katuze_kod','kod'),
        ('katuze','katuze_kod_puv','kod'),
        ('maplis','maplis_kod','kod'),
        ('zdpaze','zdpaze_kod','kod'),
        ('tel','tel_id','id'),
        ('zpurvy','zpurvy_kod','kod'),
        ('zpvypo','zpvypa_kod','kod'),
        ('pkn','pkn_id','id'),
        ('rizeni','rizeni_id_vzniku','id'),
        ('par','par_id','id'),
        ('bud','bud_id','id')
    ],
    'BUD' : [
        ('casobc','caobce_kod','kod'),
        ('typbud','typbud_kod','kod'),
        ('rizeni','rizeni_id_vzniku','id'),
        ('zpvybu','zpvybu_kod','kod'),
        ('tel','tel_id','id')
    ],
    'CABU': [
        ('bud','bud_id','id'),
        ('typbud','typbud_kod','kod')
    ],
    'DRUPOZ'  : [
      ('typppd','typppd_kod','kod')
    ],
    'ZPVYPO'  : [
        ('typppd','typppd_kod','kod')
    ],
    'KATUZE'  : [('obce','obce_kod','kod')],
    'OBCE'  : [('okresy','okresy_kod','kod')],
    'CASOBC'  : [('obce','obce_kod','kod')],
    'OKRESY'  : [('kraje','kraje_kod','kod')],
    'RZO'  : [
        ('zpochn','zpochn_kod','kod'),
        ('par','par_id','id'),
        ('bud','bud_id','id'),
        ('jed','jed_id','id')
    ],
    'JED'  : [
        ('bud','bud_id','id'),
        ('typjed','typjed_kod','kod'),
        ('zpvyje','zpvyje_kod','kod'),
        ('tel','tel_id','id')
    ],
    'BDP'  : [('par','par_id','id')],
    'OPSUB'  : [('charos','charos_kod','kod')],
    'VLA'  : [
        ('opsub','opsub_id','id'),
        ('tel','tel_id','id'),
        ('typrav','typrav_kod','kod')
    ],
    'TEL'  : [('katuze','katuze_kod','kod')],
    'JPV'  : [
        ('bud','bud_id_k','id'),
        ('bud','bud_id_pro','id'),
        ('par','par_id_k','id'),
        ('jed','jed_id_k','id'),
        ('jed','jed_id_pro','id'),
        ('opsub','opsub_id_pro','id'),
        ('opsub','opsub_id_k','id'),
        ('par','par_id_pro','id'),
        ('typrav','typrav_kod','kod'),
        ('tel','tel_id','id')
    ],
    'TYPRAV'  : [('typpre','typpre_kod','kod')],
    'RIZENI'  : [('typriz','typriz_kod','kod')],
    'RIZKU'  : [
        ('katuze','katuze_kod','kod'),
        ('rizeni','rizeni_id','id')
    ],
    'OBJRIZ'  : [
        ('rizeni','rizeni_id','id'),
        ('bud','bud_id','id'),
        ('par','par_id','id'),
        ('jed','jed_id','id')
    ],
    'PRERIZ'  : [
        ('rizeni','rizeni_id','id'),
        ('typpre','typpre_kod','kod')],
    'UCAST'  : [('rizeni','rizeni_id','id')],
    'ADRUC'  : [('ucast','ucast_id','id')],
    'LISTIN'  : [('typlis','typlis_kod','kod'), ('rizeni','rizeni_id','id')],
    'LDU'  : [
        ('dul','dul_kod','kod'),
        ('listin','listin_id','id')],
    'UCTYP'  : [
        ('ucast','ucast_id','id'),
        ('typuca','typuca_kod','kod')],
    'RL'  : [
        ('listin','listin_id','id'),
        ('par','par_id','id'),
        ('bud','bud_id','id'),
        ('jed','jed_id','id'),
        ('opsub','opsub_id','id'),
        ('jpv','jpv_id','id')],
    'SOBR': [('zpmz','katuze_kod','katuze_kod','cislo_zpmz','cislo_zpmz'),
             ('kody_char_q_bodu','kodchb_kod','kod')],
    'SBP' : [
        ('dpm','dpm_id','id'),
        ('hp','hp_id','id'),
        ('ob','ob_id','id'),
        ('sobr','bp_id','id')
    ],
    'SBM': [('dalsi_prvky_mapy','dpm_id'),
            ('hranice_bpej','hbpej_id'),
            ('obrazy_parcel','op_id')],
    'HP'  : [('par','par_id_1','id'),
             ('par','par_id_2','id')],
    'OB'  : [('bud','bud_id','id')],
    'OP'  : [('par','par_id','id')],
    'DPM' : [('sobr','bp_id','id')],
    'OBBP': [('sobr','bp_id','id')],
    'NZ': [('rizeni','rizeni_id','id')],
    'ZPMZ': [('katuze','katuze_kod','kod'),
             ('typsos','typsos_kod','kod')]
}


def createPK(table, cursor):
    """ Udela primarni klic na dane tabulce podle info v dbconstraints.py """
    try:
        s = 'ALTER TABLE %s ADD CONSTRAINT %s_pk PRIMARY KEY(%s);'
        tname = table.lower()
        pks = PrimKeys[table]
        cursor.execute(s % (tname, tname, ','.join(pks)))
    except (IndexError, KeyError):
        print 'table %s nema PK? Divne ...' % table


def createFKs(table, cursor):
    qtmp = 'ALTER TABLE %s ADD CONSTRAINT %s FOREIGN KEY(%s) REFERENCES %s(%s)'
    try:
        keys = ForKeys[table]
        for idx, k in enumerate(keys):
            refTable, col, refCol = k
            q = qtmp % (table.lower(), 'FK_%i' % idx, col, refTable, refCol)
            cursor.execute(q)
    except (IndexError, KeyError):
        pass
