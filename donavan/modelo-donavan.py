from pyomo.environ import *

# Dados do problema para teste do modelo
# Cada grão possui 3 atributos: Volume máximo (m³), Densidade (t/m³) e Receita ($/m³)
# Pode ser adicionado mais grãos conforme necessidade
grains = {
    'Grão A': {'V': 10, 'D': 0.5, 'R': 100},
    'Grão B': {'V': 15, 'D': 0.3, 'R': 80},
    'Grão C': {'V': 20, 'D': 0.4, 'R': 200},
    #...
}

V_max = 25  # Volume total disponível no caminhão (m³)
T_max = 10  # Capacidade total do caminhão (t)

# Modelo
model = ConcreteModel()

# Lista de grãos
G = grains.keys()

# Variáveis de decisão: uma para cada grão
model.x = Var(G, domain=NonNegativeReals)

# Função objetivo
model.obj = Objective(expr=sum(grains[g]['R'] * model.x[g] for g in grains), sense=maximize)

# Restrições
model.volume_constraint = Constraint(expr=sum(model.x[g] for g in grains) <= V_max)
model.weight_constraint = Constraint(expr=sum(grains[g]['D'] * model.x[g] for g in grains) <= T_max)
model.volume_limits = ConstraintList()
for g in grains:
    model.volume_limits.add(model.x[g] <= grains[g]['V'])

# Solução
solver = SolverFactory('glpk')
solver.solve(model)

# Resultados
print('Solução ótima:')
for g in grains:
    print('>', g, ':', model.x[g](), 'm³', ' | Receita $:', grains[g]['R'] * model.x[g]())
print('Volume Total:',model.volume_constraint(), 'm³')    
print(f'Receita total: $',model.obj())