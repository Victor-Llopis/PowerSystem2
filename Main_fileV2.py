import numpy as np
import pandapower as pp
import pandas as pd
from pandapower.plotting import simple_plotly, pf_res_plotly

### put all the varaibles here ###

V_HV = 230 #kilo-V base voltage
P_Nuc = 108.35 #MW active power of nuclear power 
P_RoR =  29.02
P_FV = 123.13
P_Wind=223.57
P_ST = 40.8

demand= 457.56


Q_dis = 0
PF=-0.98



#Basic net
net = pp.create_empty_network(f_hz=50.0, sn_mva=1, add_stdtypes=True)


pp.create_bus(net, name='Bus 0', vn_kv = V_HV, geodata=(300,100))       #0
pp.create_bus(net, name='Bus 1', vn_kv = V_HV, geodata=(200,100))       #1
pp.create_bus(net, name='Bus 2', vn_kv = 36, geodata=(190,95))         #2
pp.create_bus(net, name='Bus 3', vn_kv = V_HV, geodata=(400,100))       #3
pp.create_bus(net, name='Bus 4', vn_kv = 25, geodata=(410,110))         #4
pp.create_bus(net, name='Bus 5', vn_kv = V_HV, geodata=(300,200))       #5
pp.create_bus(net, name='Bus 6', vn_kv = 25, geodata=(310,210))         #6
pp.create_bus(net, name='Bus 7', vn_kv = V_HV, geodata=(400,200))       #7
pp.create_bus(net, name='Bus 8', vn_kv = 36, geodata=(410,210))         #8
pp.create_bus(net, name='Bus 9', vn_kv = V_HV, geodata=(300,300))       #9
pp.create_bus(net, name='Bus 10', vn_kv = 25, geodata=(310,310))        #10
pp.create_bus(net, name='Bus 11', vn_kv = V_HV, geodata=(100,200))      #11
pp.create_bus(net, name='Bus 12', vn_kv = 25,  geodata=(95,210))       #12
pp.create_bus(net, name='Bus 13', vn_kv = V_HV,  geodata=(0,100))       #13
pp.create_bus(net, name='Bus 14', vn_kv = 36,  geodata=(10,100))         #14
pp.create_bus(net, name='Bus 15', vn_kv = V_HV,  geodata=(100,0))       #15
pp.create_bus(net, name='Bus 16', vn_kv = 25,  geodata=(110,25))        #16



### Generator Definition ###

pp.create_gen(net, 2, name='Hydro ST', p_mw=P_ST, vm_pu=1.05)
pp.create_gen(net, 4, name='Wind', p_mw=P_Wind, vm_pu=1.05)
pp.create_gen(net, 8, name='Nuclear', p_mw=P_Nuc, vm_pu=1.05)
pp.create_gen(net, 12, name='Hydro RoR', p_mw=P_RoR, vm_pu=1.05)
pp.create_gen(net, 16, name='PV', p_mw=P_FV, vm_pu=1.05)


pp.create_ext_grid(net, 10, name = 'Gas')  #Slack bus will be bus 10 (gas)



net.gen



### Load definition ### Falta Definir reactiva de las cargas

def get_reactive(P,PF):
    Q = P*np.tan(np.arccos(PF))
    return Q


pp.create_load(net, 0, name = 'Load_1', p_mw=demand*0.4, q_mvar=get_reactive(demand*0.4, PF))
pp.create_load(net, 6, name = 'Load_2', p_mw=demand*0.4, q_mvar=get_reactive(demand*0.4, PF))
pp.create_load(net, 14, name = 'Load_3', p_mw=demand*0.2, q_mvar=get_reactive(demand*0.2, PF))





### Trafo definition ### Revisar trafos Load ( aun no definida la carga por lo que hayq ue definir aun la potencia del trafo 3,5,7)


pp.create_transformer_from_parameters(net, hv_bus = 1, lv_bus = 2, sn_mva = 500, vn_hv_kv = 230, vn_lv_kv = 36, vk_percent = 10, vkr_percent = 0, pfe_kw = 0, i0_percent = 0, name = 'T1')
pp.create_transformer_from_parameters(net, hv_bus = 3, lv_bus = 4, sn_mva = 2500, vn_hv_kv = 230, vn_lv_kv = 25, vk_percent = 10, vkr_percent = 0, pfe_kw = 0, i0_percent = 0, name = 'T2')
pp.create_transformer_from_parameters(net, hv_bus = 5, lv_bus = 6, sn_mva = 3000, vn_hv_kv = 230, vn_lv_kv = 25, vk_percent = 10, vkr_percent = 0, pfe_kw = 0, i0_percent = 0, name = 'T3')
pp.create_transformer_from_parameters(net, hv_bus = 7, lv_bus = 8, sn_mva = 1100, vn_hv_kv = 230, vn_lv_kv = 36, vk_percent = 10, vkr_percent = 0, pfe_kw = 0, i0_percent = 0, name = 'T4')
pp.create_transformer_from_parameters(net, hv_bus = 9, lv_bus = 10, sn_mva = 6000, vn_hv_kv = 230, vn_lv_kv = 25, vk_percent = 10, vkr_percent = 0, pfe_kw = 0, i0_percent = 0, name = 'T5')
pp.create_transformer_from_parameters(net, hv_bus = 11, lv_bus = 12, sn_mva = 300, vn_hv_kv = 230, vn_lv_kv = 25, vk_percent = 10, vkr_percent = 0, pfe_kw = 0, i0_percent = 0, name = 'T6')
pp.create_transformer_from_parameters(net, hv_bus = 13, lv_bus = 14, sn_mva = 8000, vn_hv_kv = 230, vn_lv_kv = 36, vk_percent = 10, vkr_percent = 0, pfe_kw = 0, i0_percent = 0, name = 'T7')
pp.create_transformer_from_parameters(net, hv_bus = 15, lv_bus = 16, sn_mva = 7500, vn_hv_kv = 230, vn_lv_kv = 25, vk_percent = 10, vkr_percent = 0, pfe_kw = 0, i0_percent = 0, name = 'T8')




#Lines
max_i=2000

pp.create_line_from_parameters(net, from_bus = 0, to_bus = 1, length_km = 100, r_ohm_per_km = 0.0917, x_ohm_per_km = 0.423220, c_nf_per_km = 12.383041 , max_i_ka = 5260, name='L1')
pp.create_line_from_parameters(net, from_bus = 0, to_bus = 3, length_km = 100, r_ohm_per_km = 0.144, x_ohm_per_km = 0.4409438, c_nf_per_km = 13.767966 , max_i_ka = 3980, name='L2')
pp.create_line_from_parameters(net, from_bus = 0, to_bus = 5, length_km = 100, r_ohm_per_km = 0.01445, x_ohm_per_km = 0.2476399, c_nf_per_km = 14.287797 , max_i_ka = 6930, name='L3')
pp.create_line_from_parameters(net, from_bus = 5, to_bus = 7, length_km = 140, r_ohm_per_km = 0.01445, x_ohm_per_km = 0.2476399, c_nf_per_km = 14.287797 , max_i_ka = 6930, name='L4')
pp.create_line_from_parameters(net, from_bus = 5, to_bus = 9, length_km = 100, r_ohm_per_km = 0.009025, x_ohm_per_km = 0.2444496, c_nf_per_km = 14.495705, max_i_ka = 9100, name='L5')
pp.create_line_from_parameters(net, from_bus = 5, to_bus = 11, length_km = 200, r_ohm_per_km = 0.01805, x_ohm_per_km = 0.1794581, c_nf_per_km = 20.274288, max_i_ka = 9100, name='L6')
pp.create_line_from_parameters(net, from_bus = 11, to_bus = 13, length_km = 140, r_ohm_per_km = 0.02035, x_ohm_per_km = 0.1803362, c_nf_per_km = 20.098525 , max_i_ka = 8510, name='L7')
pp.create_line_from_parameters(net, from_bus = 13, to_bus = 15, length_km = 140, r_ohm_per_km = 0.0116, x_ohm_per_km = 0.1718931, c_nf_per_km = 21.206053, max_i_ka = 11650, name='L8')

#pp.runpp(net,max_iteration=20)

pp.diagnostic(net)
print(net.load)
print(net.bus)
print(net.trafo)
print(net.line)
pf_res_plotly(net)
pp.to_json(net,'net.json')

