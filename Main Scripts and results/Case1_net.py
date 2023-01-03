import numpy as np
import pandapower as pp
import pandas as pd
from pandapower.plotting import simple_plotly, pf_res_plotly

### put all the varaibles here ###


net = pp.from_json('net.json')
l=[]
cases=[0,1,2,3,4]

for i in range(len(net.bus)):
    l.append('V'+str(i+1))


for i in range(len(net.line)):
    l.append('L' + str(i+1))
    

    
results = pd.DataFrame(index = cases, columns = l)



def grid_iteration(i):
    D = [5910.340038, 7198.457475, 6502.515621, 6996.075596, 4175.259554]
    PV = [1131.17518, 0, 5645.115621, 4421.27899, 0]
    W = [1490.823559, 71.98678755, 0, 1309.017234, 2369.185922]
    PC = [0, 0, 226.95, 110.5906281, 0]
    PD = [201.9, 0, 0, 0, 0]
    PH = [292.02, 292.02, 0, 292.02, 292.02]
    
    
    V_HV = 400 #kilo-V base voltage
    P_Nuc = 1083.5 #MW active power of nuclear power 
    P_RoR =  PH[i]
    P_FV = PV[i]
    P_Wind = W[i]
    P_STD = PD[i]
    P_STC = PC[i]
    
    demand= D[i]
    
    
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
    
    pp.create_gen(net, 6, name='Hydro ST', p_mw=P_STD, vm_pu=1.05)
    pp.create_gen(net, 8, name='Wind', p_mw=P_Wind, vm_pu=1.05)
    pp.create_gen(net, 2, name='Nuclear', p_mw=P_Nuc, vm_pu=1.05)
    pp.create_gen(net, 3, name='Hydro RoR', p_mw=P_RoR, vm_pu=1.05)
    pp.create_gen(net, 5, name='PV', p_mw=P_FV, vm_pu=1.05)
    
    
    pp.create_ext_grid(net, 0, name = 'Gas')  #Slack bus will be bus 10 (gas)
    
    
    
    net.gen
    
    
    
    ### Load definition ### Falta Definir reactiva de las cargas
    
    def get_reactive(P,PF):
        Q = P*np.tan(np.arccos(PF))
        return Q
    
    
    pp.create_load(net, 1, name = 'Load_1', p_mw=demand*0.4, q_mvar=get_reactive(demand*0.4, PF))
    pp.create_load(net, 7, name = 'Load_2', p_mw=demand*0.4, q_mvar=get_reactive(demand*0.4, PF))
    pp.create_load(net, 4, name = 'Load_3', p_mw=demand*0.2, q_mvar=get_reactive(demand*0.2, PF))
    pp.create_load(net, 6, name = 'Hydro_Charge', p_mw=P_STC, q_mvar=get_reactive(P_STC, PF))
    
    
    
    
    ### Trafo definition ### Revisar trafos Load ( aun no definida la carga por lo que hayq ue definir aun la potencia del trafo 3,5,7)
    
    
    
    #Lines
    
    
    pp.create_line_from_parameters(net, from_bus = 0, to_bus = 1, length_km = 100, r_ohm_per_km = 0.005775, x_ohm_per_km = 0.240949, c_nf_per_km = 14.709559 , max_i_ka = 4.652, name='L1') 
    
    pp.create_line_from_parameters(net, from_bus = 1, to_bus = 2, length_km = 140, r_ohm_per_km = 0.01155, x_ohm_per_km = 0.172456, c_nf_per_km = 21.133759, max_i_ka = 2.326, name='L2')
    
    pp.create_line_from_parameters(net, from_bus = 1, to_bus = 7, length_km = 100, r_ohm_per_km = 0.00645, x_ohm_per_km = 0.241807, c_nf_per_km = 14.656532, max_i_ka = 4.384, name='L3')
    
    pp.create_line_from_parameters(net, from_bus = 1, to_bus = 3, length_km = 200, r_ohm_per_km = 0.018075, x_ohm_per_km = 0.24898, c_nf_per_km = 14.209873 , max_i_ka = 2.440, name='L4')
    
    pp.create_line_from_parameters(net, from_bus = 3, to_bus = 4, length_km = 140, r_ohm_per_km = 0.01445, x_ohm_per_km = 0.247238, c_nf_per_km = 14.311345 , max_i_ka = 2.788, name='L5')
    
    pp.create_line_from_parameters(net, from_bus = 4, to_bus = 5, length_km = 140, r_ohm_per_km = 0.00645, x_ohm_per_km = 0.241807, c_nf_per_km = 14.656532 , max_i_ka = 4.384, name='L6')
    
    pp.create_line_from_parameters(net, from_bus = 7, to_bus = 8, length_km = 100, r_ohm_per_km = 0.00645, x_ohm_per_km = 0.241807, c_nf_per_km = 14.656532 , max_i_ka = 4.384, name='L7')
    
    pp.create_line_from_parameters(net, from_bus = 7, to_bus = 6, length_km = 100, r_ohm_per_km = 0.00905, x_ohm_per_km = 0.243549, c_nf_per_km = 14.532293 , max_i_ka = 3.664, name='L8')
    
    pp.create_line_from_parameters(net, from_bus = 5, to_bus = 6, length_km = 140, r_ohm_per_km = 0.00645, x_ohm_per_km = 0.241807, c_nf_per_km = 14.656532 , max_i_ka = 4.384, name='L9')
    
    pp.create_line_from_parameters(net, from_bus = 0, to_bus = 3, length_km = 223.61, r_ohm_per_km = 0.00905, x_ohm_per_km = 0.243549, c_nf_per_km = 14.532293 , max_i_ka = 3.664, name='L10')
    
    pp.create_line_from_parameters(net, from_bus = 6, to_bus = 1, length_km = 140, r_ohm_per_km = 0.01445, x_ohm_per_km = 0.247238, c_nf_per_km = 14.311345 , max_i_ka = 2.788, name='L11')
    
    #pp.runpp(net,max_iteration=20)
    
    pp.diagnostic(net)
    print(net.load)
    print(net.bus)
    print(net.trafo)
    print(net.line)
    pf_res_plotly(net)
    pp.to_json(net,'net'+str(i)+'.json')
    
    
    
    for j in range(len(net.bus)):
        results['V'+str(j+1)][i] = net.res_bus['vm_pu'][j]
    
    for j in range(len(net.line)):
        results['L'+str(j+1)][i] = net.res_line['loading_percent'][j]
   
    
    
    return 


