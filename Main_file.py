import numpy as np
import pandapower as pp
import pandas as pd


### put all the varaibles here ###

V_HV = 230 #kilo-V base voltage
P_Nuc = 1084.35 #MW active power of nuclear power 
P_RoR =  292.02
P_FV = #7203
P_Wind=#20
P_Gas=   #5865.91 
P_ST = #202



Q_dis = 0
PF=0.98



#Basic net
net = pp.create_empty_network(f_hz=50.0, sn_mva=1, add_stdtypes=True)


pp.create_bus(net, name='Bus 0', vn_kv = V_HV, geodata=(300,100))       #0
pp.create_bus(net, name='Bus 1', vn_kv = V_HV, geodata=(200,100))       #1
pp.create_bus(net, name='Bus 2', vn_kv = 36, geodata=(200,100))         #2
pp.create_bus(net, name='Bus 3', vn_kv = V_HV, geodata=(400,100))       #3
pp.create_bus(net, name='Bus 4', vn_kv = 25, geodata=(400,100))         #4
pp.create_bus(net, name='Bus 5', vn_kv = V_HV, geodata=(300,200))       #5
pp.create_bus(net, name='Bus 6', vn_kv = 25, geodata=(300,200))         #6
pp.create_bus(net, name='Bus 7', vn_kv = V_HV, geodata=(400,200))       #7
pp.create_bus(net, name='Bus 8', vn_kv = 36, geodata=(400,200))         #8
pp.create_bus(net, name='Bus 9', vn_kv = V_HV, geodata=(300,300))       #9
pp.create_bus(net, name='Bus 10', vn_kv = 25, geodata=(300,300))        #10
pp.create_bus(net, name='Bus 11', vn_kv = V_HV, geodata=(100,200))      #11
pp.create_bus(net, name='Bus 12', vn_kv = 25,  geodata=(100,200))       #12
pp.create_bus(net, name='Bus 13', vn_kv = V_HV,  geodata=(0,100))       #13
pp.create_bus(net, name='Bus 14', vn_kv = 36,  geodata=(0,100))         #14
pp.create_bus(net, name='Bus 15', vn_kv = V_HV,  geodata=(100,0))       #15
pp.create_bus(net, name='Bus 16', vn_kv = 25,  geodata=(100,25))        #16



### Generator Definition ###

pp.create_gen(net, 2, name='Hydro ST', p_mw=P_ST, vm_pu=1.05)
pp.create_gen(net, 4, name='Wind', p_mw=P_Wind, vm_pu=1.05)
pp.create_gen(net, 8, name='Nuclear', p_mw=P_Nuc, vm_pu=1.05)
pp.create_gen(net, 10, name='Gas', p_mw=P_Gas, vm_pu=1.05)
pp.create_gen(net, 12, name='Hydro RoR', p_mw=P_RoR, vm_pu=1.05)
pp.create_gen(net, 16, name='PV', p_mw=P_FV, vm_pu=1.05)

#pp.create_sgen(net, 11, name='Dismantled Plant', p_mw=0, q_mvar=Q_dis)
#pp.create_ext_grid(net, 0)  #Slack bus will be bus 0



net.gen



### Load definition ### Falta Definir reactiva de las cargas

def get_reactive(P,PF):
    Q = P*np.tan(np.arccos(PF))
    return Q


pp.create_load(net, 0, name = 'Load_1', p_mw=demand*0.4, q_mvar=get_reactive(P_II, PF))
pp.create_load(net, 6, name = 'Load_2', p_mw=demand*0.4, q_mvar=get_reactive(P_II, PF))
pp.create_load(net, 14, name = 'Load_3', p_mw=demand*0.2, q_mvar=get_reactive(P_II, PF))





### Trafo definition ### Revisar trafos Load ( aun no definida la carga por lo que hayq ue definir aun la potencia del trafo 3,5,7)


pp.create_transformer_from_parameters(net, hv_bus = 1, lv_bus = 2, sn_mva = 250, vn_hv_kv = 230, vn_lv_kv = 36, vk_percent = 10, vkr_percent = 0, pfe_kw = 0, i0_percent = 0, name = 'T1')
pp.create_transformer_from_parameters(net, hv_bus = 3, lv_bus = 4, sn_mva = 25, vn_hv_kv = 230, vn_lv_kv = 25, vk_percent = 10, vkr_percent = 0, pfe_kw = 0, i0_percent = 0, name = 'T2')
pp.create_transformer_from_parameters(net, hv_bus = 5, lv_bus = 6, sn_mva = 3000, vn_hv_kv = 230, vn_lv_kv = 25, vk_percent = 10, vkr_percent = 0, pfe_kw = 0, i0_percent = 0, name = 'T3')
pp.create_transformer_from_parameters(net, hv_bus = 7, lv_bus = 8, sn_mva = 1100, vn_hv_kv = 230, vn_lv_kv = 36, vk_percent = 10, vkr_percent = 0, pfe_kw = 0, i0_percent = 0, name = 'T4')
pp.create_transformer_from_parameters(net, hv_bus = 9, lv_bus = 10, sn_mva = 6000, vn_hv_kv = 230, vn_lv_kv = 25, vk_percent = 10, vkr_percent = 0, pfe_kw = 0, i0_percent = 0, name = 'T5')
pp.create_transformer_from_parameters(net, hv_bus = 11, lv_bus = 12, sn_mva = 300, vn_hv_kv = 230, vn_lv_kv = 25, vk_percent = 10, vkr_percent = 0, pfe_kw = 0, i0_percent = 0, name = 'T6')
pp.create_transformer_from_parameters(net, hv_bus = 13, lv_bus = 14, sn_mva = 8000, vn_hv_kv = 230, vn_lv_kv = 25, vk_percent = 10, vkr_percent = 0, pfe_kw = 0, i0_percent = 0, name = 'T7')
pp.create_transformer_from_parameters(net, hv_bus = 15, lv_bus = 16, sn_mva = 7500, vn_hv_kv = 230, vn_lv_kv = 25, vk_percent = 10, vkr_percent = 0, pfe_kw = 0, i0_percent = 0, name = 'T8')

from math import sqrt, pi , log

#--------------------------------------------------------------------#
# Double line Line
#--------------------------------------------------------------------#

class DoubleLineParam:
    def __init__(self) -> None:
        pass
        # Distances
        a = 6   #m
        b = 8   #m
        c = a   #m
        d = a #m
        e = a   #m

        d_A1A2 = sqrt((d+e)**2 + a**2) #m
        d_A1B1 = sqrt((abs(b-a)/2)**2 + d**2)    #m
        d_A1B2 = sqrt(((a+b)/2)**2 + d**2)    #m
        d_A2B1 = sqrt(((b+c)/2)**2 + e**2)   #m
        d_A2B2 = sqrt((abs(b-c)/2)**2 + e**2)    #m
        d_A1C1 = sqrt((abs(c-a)/2)**2 + (d+e)**2)    #m  / Suposition that a = c
        d_A1C2 = a    #m
        d_A2C1 = c    #m
        d_A2C2 = d_A1C1    #m
        d_B1B2 = b    #m
        d_B1C1 = d_A2B2  #m
        d_B1C2 = d_A1B2    #m
        d_B2C1 = d_A2B1  #m
        d_B2C2 = d_A1B1  #m
        d_C1C2 = d_A1A2  #m
        
        # Conductor Characteristics

        # 54Al + 7Ac
        # Type Cardenal
        self.R = 0.062   # Ohms/km (AC resistance)
        d = 30.40   # diameter in mm
        r = d/2
        kg = 0.809  #
        self.G = 0 # In this case we consider Admittance negligible# Conductor Characteristics

        # GMR Calculation


        GMR_A = (kg*r*d_A1A2) ** (1/2)
        GMR_B = (kg*r*d_B1B2) ** (1/2)
        GMR_C = (kg*r*d_C1C2) ** (1/2)
        GMR = (GMR_A*GMR_B*GMR_C) **(1/3)

        # GMD Calculation

        GMD_AB = (d_A1B1*d_A1B2*d_A2B1*d_A2B2) ** (1/4)
        GMD_BC = (d_B1C1*d_B1C2*d_B2C1*d_B2C2) ** (1/4)
        GMD_CA = (d_A1C1*d_A1C2*d_A2C1*d_A2C2) ** (1/4)

        GMD = (GMD_AB*GMD_BC*GMD_CA) **(1/3)

        # Req Calculation

        Req_A = (r*d_A1A2) ** (1/2)
        Req_B = (r*d_B1B2) ** (1/2)
        Req_C = (r*d_C1C2) ** (1/2)

        Req = (Req_A*Req_B*Req_C) ** (1/3)

        # Inductance Calculation

        self.L = 0.2*log((GMD*1000)/GMR) #mH/km  / Should give around 1 mH/km

        f= 50 # Hz
        self.Xl = 2*pi*f*self.L/1000 # Ohm/km

        # Capacitance

        self.C = 1000/(18*log(GMD*1000/Req)) # nF/km / around 0-20nF/km in overhead lines

        # Print results

        print('\u0332Double Line Parameters:\u0332\n',)
        print('R = ',self.R, ' Ohms/km')
        print('L = ',self.L,' mH/km')
        print('Xl = ',self.Xl,' Ohms/km')
        print('C = ',self.C, ' nF/km')
        print('G = ',self.G, ' 1/Ohms·km')


class SimpleLineParam:
    def __init__(self) -> None:
        # Distances

        a = 12 #m
        b = 3 #m

        d_AB = sqrt((a/2)**2 + b**2) #m
        d_AC = a    #m
        d_BC = d_AB #m

        # Conductor Characteristics

        # 54Al + 7Ac
        # Type Cardenal

        self.R = 0.062   # Ohms/km (AC resistance)
        d = 30.40   # diameter in mm
        kg = 0.809  #
        self.G = 0 # In this case we consider Admittance negligible

        # Inductance calculation

        GMD = (d_AB+d_BC+d_AC) ** (1/3) 
        GMR = kg*(d/2)
        self.L = 0.2*log((GMD*1000)/GMR) #mH/km  / Should give around 1 mH/km
        f= 50 # Hz
        self.Xl = 2*pi*f*self.L/1000 # Ohm/km


        # Capacitance

        Req = d/2
        self.C = 1000/(18*log(GMD*1000/Req)) # nF/kn / around 0-20nF/km in overhead lines











#####################################################################################



dbLine = DoubleLineParam()
sLine = SimpleLineParam()
bdLine = BundleLineParam()

pp.create_line_from_parameters(net, from_bus = 0, to_bus = 1, length_km = 100, r_ohm_per_km = dbLine.R, x_ohm_per_km = dbLine.Xl, c_nf_per_km = dbLine.C , max_i_ka = 2*max_i, name='L1')
pp.create_line_from_parameters(net, from_bus = 0, to_bus = 3, length_km = 100, r_ohm_per_km = dbLine.R, x_ohm_per_km = dbLine.Xl, c_nf_per_km = dbLine.C , max_i_ka = 2*max_i, name='L2')
pp.create_line_from_parameters(net, from_bus = 0, to_bus = 5, length_km = 100, r_ohm_per_km = sLine.R, x_ohm_per_km = sLine.Xl, c_nf_per_km = sLine.C , max_i_ka = max_i, name='L3')
pp.create_line_from_parameters(net, from_bus = 5, to_bus = 7, length_km = 140, r_ohm_per_km = sLine.R, x_ohm_per_km = sLine.Xl, c_nf_per_km = sLine.C , max_i_ka = max_i, name='L4')
pp.create_line_from_parameters(net, from_bus = 9, to_bus = 10, length_km = 100, r_ohm_per_km = dbLine.R, x_ohm_per_km = dbLine.Xl, c_nf_per_km = dbLine.C , max_i_ka = 2*max_i, name='L5')
pp.create_line_from_parameters(net, from_bus = 5, to_bus = 11, length_km = 200, r_ohm_per_km = sLine.R, x_ohm_per_km = sLine.Xl, c_nf_per_km = sLine.C , max_i_ka = max_i, name='L6')
pp.create_line_from_parameters(net, from_bus = 11, to_bus = 13, length_km = 140, r_ohm_per_km = sLine.R, x_ohm_per_km = sLine.Xl, c_nf_per_km = sLine.C , max_i_ka = max_i, name='L7')
pp.create_line_from_parameters(net, from_bus = 13, to_bus = 15, length_km = 140, r_ohm_per_km = sLine.R, x_ohm_per_km = sLine.Xl, c_nf_per_km = sLine.C , max_i_ka = max_i, name='L8')

#pp.runpp(net,max_iteration=20)
pp.diagnostic(net)
print(net.load)
print(net.bus)
print(net.trafo)
print(net.line)
pp.to_json(net,'net.json')

