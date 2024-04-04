import pandas as pd
import numpy as np
import xgboost

df_v = pd.read_csv(r'vehicle.csv',low_memory=False,header=0,encoding="ISO-8859-1")
df_p = pd.read_csv(r'person.csv',low_memory=False,header=0,encoding="ISO-8859-1")
df_a = pd.read_csv(r'accident.csv',low_memory=False,header=0,encoding="ISO-8859-1")
df_drf = pd.read_csv(r'driverrf.csv',low_memory=False,header=0,encoding="ISO-8859-1")
df_crf = pd.read_csv(r'crashrf.csv',low_memory=False,header=0,encoding="ISO-8859-1")

df_v['key'] = df_v.apply(lambda x: str(x['ST_CASE'])+'-'+str(x['VEH_NO']),axis = 1)

df_p = df_p[df_p['PER_TYP']==1]

df_p['key'] = df_p.apply(lambda x: str(x['ST_CASE'])+'-'+str(x['VEH_NO']),axis = 1)

use = {
"vehicle.csv":['STATE','VE_FORMS',"NUMOCCS","UNITTYPE","HIT_RUN","REG_STAT","OWNER","MOD_YEAR",
               "VPICBODYCLASS",'MAKE','BODY_TYP','ICFINALBODY','GVWR_FROM','GVWR_TO','TOW_VEH',
               'J_KNIFE','MCARR_I1','V_CONFIG','CARGO_BT','HAZ_INV','HAZ_PLAC','HAZ_CNO','HAZ_REL',
               'BUS_USE','SPEC_USE','EMER_USE','TRAV_SP','UNDERIDE','ROLLOVER','ROLINLOC','IMPACT1',
               'DEFORMED','TOWED','M_HARM','FIRE_EXP','DEATHS','DR_DRINK','DR_PRES','L_STATE','L_TYPE',
               'L_STATUS','CDL_STAT','L_ENDORS','L_COMPL','L_RESTRI','DR_HGT','DR_WGT','PREV_ACC','PREV_SUS1',
               'PREV_SUS2','PREV_SUS3','PREV_DWI','PREV_SPD','PREV_OTH','FIRST_MO','FIRST_YR','LAST_MO','LAST_YR'
               ,'SPEEDREL','VTRAFWAY','VNUM_LAN','VSPD_LIM','VALIGN','VPROFILE','VPAVETYP','VSURCOND','VTRAFCON',
               'VTCONT_F','P_CRASH1','P_CRASH2','P_CRASH3','PCRASH4','PCRASH5','ACC_TYPE'],
"accident.csv": ['PEDS','VE_TOTAL','PVH_INVL','PERMVIT','MONTH','DAY_WEEK','HOUR',
                 'ROUTE','RUR_URB','FUNC_SYS','NHS','HARM_EV','MAN_COLL','RELJCT1','TYP_INT','REL_ROAD',
                 'WRK_ZONE','LGT_COND','SCH_BUS','FATALS','DRUNK_DR','WEATHER'],
"person.csv": ['AGE','SEX','PER_TYP','INJ_SEV','REST_USE','REST_MIS','HELM_USE',
               'HELM_MIS','AIR_BAG','EJECTION','EJ_PATH','DRINKING','DRUGS','HOSPITAL','DOA','LAG_HRS','STR_VEH',
               'LOCATION','HISPANIC']
}

numerical = {
"vehicle.csv":['VE_FORMS',"NUMOCCS","MOD_YEAR",'GVWR_FROM','GVWR_TO','TRAV_SP','DEATHS','DR_HGT','DR_WGT','PREV_ACC','PREV_SUS1','PREV_SUS2','PREV_SUS3','PREV_DWI','PREV_SPD','PREV_OTH','VSPD_LIM']
,"accident.csv": [],
"person.csv":[]
}

special = {
"vehicle.csv":[["NUMOCCS","99",""],["UNITTYPE",'','0'],["MOD_YEAR",'9998',''],["MOD_YEAR",'9999',''],['GVWR_FROM','98',''],['GVWR_FROM','99',''],['GVWR_TO','98',''],['GVWR_TO','99',''],['TRAV_SP','997',''],['TRAV_SP','998',''],['TRAV_SP','999',''],['DR_HGT','998',''],['DR_HGT','999',''],['DR_WGT','997',''],['DR_WGT','998',''],['DR_WGT','999',''],['PREV_ACC','98',''],['PREV_ACC','99',''],['PREV_ACC','998',''],['PREV_SUS1','99',''],['PREV_SUS1','998',''],['PREV_SUS2','99',''],['PREV_SUS2','998',''],['PREV_SUS3','99',''],['PREV_SUS3','998',''],['PREV_DWI','99',''],['PREV_DWI','998',''],['PREV_SPD','99',''],['PREV_SPD','998',''],['PREV_OTH','99',''],['PREV_OTH','998',''],['VSPD_LIM','0',''],['VSPD_LIM','99',''],],
"accident.csv": [],
"person.csv":[]
}

df_a = df_a[['ST_CASE']+use['accident.csv']]

df_v = df_v[['key','ST_CASE']+use['vehicle.csv']]

df_p = df_p[['key']+use['person.csv']]

df_va = df_v.merge(df_a, how='inner', on='ST_CASE', left_on=None, right_on=None, left_index=False, right_index=False, sort=False, suffixes=('_x', ''), copy=True, indicator=False, validate=None)

df_vap = df_va.merge(df_p, how='inner', on='key', left_on=None, right_on=None, left_index=False, right_index=False, sort=False, suffixes=('_x', ''), copy=True, indicator=False, validate=None)

df_drf['key'] = df_drf.apply(lambda x: str(x['ST_CASE'])+'-'+str(x['VEH_NO']),axis = 1)

df_drf=df_drf[['key','DRIVERRF']]

new_class = {0:[0],1:[81,82,83,87],2:[16,37,84,95,96,86,97],3:[4,60,73,74,94,19,53,91],4:[8,10,12,13,36],5:[77,78,79],6:[21,22,57,80,85,88],7:[6,15,20,23,24,26,27,28,29,30,31,32,33,34,35,38,39,40,41,42,45,48,50,51,54,56,58,59,89,52,18]}
def change_class(s):
    for i in range(8):
        if s in new_class[i]:
            return i
        

df_drf['DRIVERRF'] = df_drf['DRIVERRF'].apply(lambda x:change_class(x))

df_all = df_vap.merge(df_drf, how='inner', on='key', left_on=None, right_on=None, left_index=False, right_index=False, sort=False, suffixes=('_x', '_y'), copy=True, indicator=False, validate=None)

df_all = df_all.drop(df_all[df_all['DRIVERRF']==0].index)
df_all = df_all.drop(df_all[df_all['DRIVERRF'] is None].index)

df_all = df_all.sample(frac=1).reset_index(drop=True)
df_all = df_all.astype('category') 

x=df_all[use['vehicle.csv']+use['accident.csv']+use['person.csv']]

n = df_all.shape[0]
x_train=x.iloc[:int(n*0.8),:]
y_train=y.iloc[:int(n*0.8)]
x_test=x.iloc[int(n*0.8):,:]
y_test=y.iloc[int(n*0.8):]

x_train.to_csv('x_train.csv', index=False) 
y_train.to_csv('y_train.csv', index=False) 
x_test.to_csv('x_test.csv', index=False) 
y_test.to_csv('y_test.csv', index=False) 