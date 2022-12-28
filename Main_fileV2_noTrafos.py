import numpy as np
import pandapower as pp
import pandas as pd
from pandapower.plotting import simple_plotly, pf_res_plotly

### put all the varaibles here ###

V_HV = 400 #kilo-V base voltage
P_Nuc = 108.35*10 #MW active power of nuclear power 
P_RoR =  29.02*10
P_FV = 123.13*10
P_Wind=223.57*10
P_ST = 40.8*10

demand= 457.56*10


Q_dis = 0
PF=0.98



#Basic net
net = pp.create_empty_network(f_hz=50.0, sn_mva=1, add_stdtypes=True)


pp.create_bus(net, name='Bus 0', vn_kv = V_HV, geodata=(0,100))       
pp.create_bus(net, name='Bus 1', vn_kv = V_HV, geodata=(0, 0))       
pp.create_bus(net, name='Bus 2', vn_kv = V_HV, geodata=(140,0))       
pp.create_bus(net, name='Bus 3', vn_kv = V_HV, geodata=(-200,0))      
pp.create_bus(net, name='Bus 4', vn_kv = V_HV, geodata=(-300,-100))      
pp.create_bus(net, name='Bus 5', vn_kv = V_HV, geodata=(-200,-200))       
pp.create_bus(net, name='Bus 6', vn_kv = V_HV, geodata=(-100,-100))      
pp.create_bus(net, name='Bus 7', vn_kv = V_HV,  geodata=(0,-100))       
pp.create_bus(net, name='Bus 8', vn_kv = V_HV,  geodata=(100,-100))       



### Generator Definition ###

pp.create_gen(net, 6, name='Hydro ST', p_mw=P_ST, vm_pu=1.03)
pp.create_gen(net, 8, name='Wind', p_mw=P_Wind, vm_pu=1.02)
pp.create_gen(net, 2, name='Nuclear', p_mw=P_Nuc, vm_pu=1.02)
pp.create_gen(net, 3, name='Hydro RoR', p_mw=P_RoR, vm_pu=1.01)
pp.create_gen(net, 5, name='PV', p_mw=P_FV, vm_pu=1.03)


pp.create_ext_grid(net, 0, name = 'Gas')  #Slack bus will be bus 10 (gas)



net.gen



### Load definition ### Falta Definir reactiva de las cargas

def get_reactive(P,PF):
    Q = P*np.tan(np.arccos(PF))
    return Q


pp.create_load(net, 1, name = 'Load_1', p_mw=demand*0.4, q_mvar=get_reactive(demand*0.4, PF))
pp.create_load(net, 7, name = 'Load_2', p_mw=demand*0.4, q_mvar=get_reactive(demand*0.4, PF))
pp.create_load(net, 4, name = 'Load_3', p_mw=demand*0.2, q_mvar=get_reactive(demand*0.2, PF))





### Trafo definition ### Revisar trafos Load ( aun no definida la carga por lo que hayq ue definir aun la potencia del trafo 3,5,7)



#Lines
max_i=2000

pp.create_line_from_parameters(net, from_bus = 0, to_bus = 1, length_km = 100, r_ohm_per_km = 0.00385, x_ohm_per_km = 0.249302164, c_nf_per_km = 13.66843238 , max_i_ka = 6.978, name='L1') 

pp.create_line_from_parameters(net, from_bus = 1, to_bus = 2, length_km = 140, r_ohm_per_km = 0.005775, x_ohm_per_km = 0.259024222, c_nf_per_km = 13.66843238 , max_i_ka = 4.652, name='L2')

pp.create_line_from_parameters(net, from_bus = 1, to_bus = 7, length_km = 100, r_ohm_per_km = 0.0231, x_ohm_per_km = 0.395412005, c_nf_per_km = 9.165699678 , max_i_ka = 1.163, name='L3')

pp.create_line_from_parameters(net, from_bus = 1, to_bus = 3, length_km = 200, r_ohm_per_km = 0.00385, x_ohm_per_km = 0.249302164, c_nf_per_km = 13.66843238 , max_i_ka = 6.978, name='L4')

pp.create_line_from_parameters(net, from_bus = 3, to_bus = 4, length_km = 140, r_ohm_per_km = 0.00385, x_ohm_per_km = 0.249302164, c_nf_per_km = 13.66843238 , max_i_ka = 6.978, name='L5')

pp.create_line_from_parameters(net, from_bus = 4, to_bus = 5, length_km = 140, r_ohm_per_km = 0.00385, x_ohm_per_km = 0.249302164, c_nf_per_km = 13.66843238 , max_i_ka = 6.978, name='L6')

pp.create_line_from_parameters(net, from_bus = 7, to_bus = 8, length_km = 100, r_ohm_per_km = 0.01155, x_ohm_per_km = 0.178402754, c_nf_per_km = 20.39932257 , max_i_ka = 2.326, name='L7')

pp.create_line_from_parameters(net, from_bus = 7, to_bus = 6, length_km = 100, r_ohm_per_km = 0.0231, x_ohm_per_km = 0.395412005, c_nf_per_km = 9.165699678 , max_i_ka = 1.163, name='L8')

#pp.runpp(net,max_iteration=20)

pp.diagnostic(net)
print(net.load)
print(net.bus)
print(net.trafo)
print(net.line)
pf_res_plotly(net)
pp.to_json(net,'net.json')

