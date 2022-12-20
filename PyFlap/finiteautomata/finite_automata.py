import copy
class FiniteAutomata:
    def __init__(self, raw_fa):
        self.finite_automata = self.clean_fa(raw_fa)
        self.final_states = self.get_final_states()
        self.initial_state = self.get_initial_state()

    # AUXILIAR  FUNCTIONS TO MANAGE FINITE AUTOMATA
    def clean_fa(self, finite_automata):
        filtered_fa =  {'nodes': [], 'edges': []}
        for node in finite_automata["nodes"]:
            filtered_fa["nodes"].append(node['data'])
        for edge in finite_automata["edges"]:
            filtered_fa["edges"].append(edge['data'])

        for edge in filtered_fa['edges']:
            if(edge['label'] == None):
                filtered_fa['edges'][filtered_fa['edges'].index(edge)] = {'source': edge['source'], 'target': edge['target'], 'label': 'λ'}

        return filtered_fa

    def get_final_states(self):
        final_states = []
        for state in self.finite_automata["nodes"]:
            if state.get('is_final', False):
                final_states.append(state)

        return final_states

    def get_initial_state(self):
        for state in self.finite_automata["nodes"]:
            if state.get('is_initial', False):
                return state

    def get_in_degree(self, state_id): #verifica quantas transições 'entram' no estado
        degree = 0
        for edge in self.finite_automata['edges']:
            if(edge['target'] == state_id):
                degree = degree + 1

        return degree

    def get_out_degree(self, state_id): #verifica quantas transições 'entram' no estado
        degree = 0
        for edge in self.finite_automata['edges']:
            if(edge['source'] == state_id):
                degree = degree + 1
        return degree

    def set_initial_state(self, new_initial_state_id):
        # Removing current initial state
        for state in self.finite_automata['nodes']:
            if(state['id'] == self.initial_state['id']):
                self.finite_automata['nodes'][self.finite_automata['nodes'].index(state)]['is_initial'] = False
        
        # Adding new one
        for state in self.finite_automata['nodes']:
            if(state['id'] == new_initial_state_id):
                self.finite_automata['nodes'][self.finite_automata['nodes'].index(state)]['is_initial'] = True
                self.initial_state = state
                return self.finite_automata

        return None

    def add_new_state(self, state):
        self.finite_automata['nodes'].append(state)
        return self.finite_automata
       
    def add_new_transition(self, source, target, value): # passa o id da source, target e o label da transicao
        new_transition = {'source': source, 'target': target, 'label': value}
        
        #print(f"\n\n                 adding new transition {new_transition}   \n                     Before {self.finite_automata}\n\n")
        
        for edge in self.finite_automata['edges']:
            if(edge['source'] == source and edge['target'] == target):
                self.finite_automata['edges'][self.finite_automata['edges'].index(edge)]['label'] = value+'|'+self.finite_automata['edges'][self.finite_automata['edges'].index(edge)]['label']
                return 
        
        self.finite_automata['edges'].append(new_transition)
        #print(f"\n                     After {self.finite_automata}\n\n")
        return self.finite_automata

    
    
    def unmark_all_final_states(self):
        for state in self.finite_automata['nodes']:
            if(state.get('is_final', False)):
                self.finite_automata['nodes'][self.finite_automata['nodes'].index(state)]['is_final'] = False
        return self.finite_automata

    def set_final_state(self, state_id):
        for state in self.finite_automata['nodes']:
            if(state['id'] == state_id):
                self.finite_automata['nodes'][self.finite_automata['nodes'].index(state)]['is_final'] = True
                self.final_states.append(state)
                return self.finite_automata

    def check_self_loop(self, state_id):
        for edge in self.finite_automata['edges']:
            if(edge['source'] == state_id and edge['target'] == state_id):
                return True 
        return False
    
    def get_self_loops(self, state_id):
        self_loops = []
        if(self.check_self_loop(state_id)):
            for edge in self.finite_automata['edges']:
                if(edge['source'] == state_id and edge['target'] == state_id):
                    self_loops.append(edge)
        return self_loops

    def remove_empty_transition_self_loops(self):
        all_self_loops = []
        for state in self.finite_automata['nodes']:
            all_self_loops = all_self_loops +  self.get_self_loops(state['id'])

        for loop in all_self_loops:
            if(loop in self.finite_automata['edges'] and loop['label'] == 'λ'):
                self.finite_automata['edges'].remove(loop)

    def is_dead_state(self, state_id):
        for node in self.finite_automata['nodes']:
            if(node['id'] == state_id):
              if(not node.get('is_final')):
                  for edge in self.finite_automata['edges']:
                      if(edge['source'] == state_id and edge['target'] != state_id):
                          return False
        return True

    def unify_multiple_transitions(self):
        new_transitions = copy.deepcopy(self.finite_automata['edges'])
        new_transitions_to_add = []
        num_of_transitions = len(self.finite_automata['edges'])
        for i in range(0, num_of_transitions):
            remove_i = False
            for j in range(i+1, num_of_transitions):
                source_i = self.finite_automata['edges'][i]['source']
                target_i = self.finite_automata['edges'][i]['target']
                
                source_j = self.finite_automata['edges'][j]['source']
                target_j = self.finite_automata['edges'][j]['target']
                
                if(source_i == source_j and target_i == target_j):
                    label_i = self.finite_automata['edges'][i]['label']
                    label_j = self.finite_automata['edges'][j]['label']
                    
                    new_label = label_i+"|"+label_j
                    
                    new_transition = {"source": source_i, "target": target_i, "label": new_label}

                    new_transitions.remove(self.finite_automata['edges'][j])
                    new_transitions.append(new_transition)
                    
                    remove_i = True
                
            if(remove_i):
                new_transitions.remove(self.finite_automata['edges'][i])
            
        new_transitions = new_transitions + new_transitions_to_add
        
        self.finite_automata['edges'] = copy.deepcopy(new_transitions)
        
        return self.finite_automata
    
    def transform_empty_transition(self, transition_label):
        if(transition_label == 'λ'):
            transition_label = ''
        return transition_label

    def remove_state_aux(self, state_id):
        
        edges_to_remove = []
        for edge in self.finite_automata['edges']:
            if(edge['source'] == state_id or edge['target'] == state_id):
                edges_to_remove.append(edge)
        
        for edge in edges_to_remove:
            self.finite_automata['edges'].remove(edge)

        for node in self.finite_automata['nodes']:
            if(node['id'] == state_id):
                self.finite_automata['nodes'].remove(node)
                return True
            
        return False
    
    def is_dead(self, state):
        if(state.get('is_final', False)):
            return False
        for edge in self.finite_automata['edges']:
            if(edge['source'] == state['id'] and edge['target'] != state['id']):
                return False
        return True 

    def remove_all_dead_states(self):
        dead_list = []
        for node in self.finite_automata['nodes']:
            if(self.is_dead(node)):
                dead_list.append(node['id'])
        
        for state_id in dead_list:
            self.remove_state_aux(state_id)
        
        return
    

    # SOURCE: https://rpruim.github.io/m252/S19/from-class/models-of-computation/dfanfa-to-regular-expression.html
    def convert_fa_to_regex(self):
        finite_automata = copy.deepcopy(self.finite_automata)
        
        # #print(f'\n Clean FA: {self.finite_automata} \n\n')
        
        # #print(f'\n FINAL STATES: {self.final_states}')
        
        # #print(f'\n INITIAL STATE: {self.initial_state}')
        
        # #print(f"\n IN DEGREE q0: {self.get_in_degree('q0')}")
        
        # #print(f"\n OUT DEGREE q0: {self.get_out_degree('q0')}")
        
        # 0 - Remove all self loops with empty transition
        self.remove_empty_transition_self_loops()
        # 1 - Create a new initial state with a λ transition to the old start state (if its 'in degree' is != 0)
        #if(self.get_in_degree(self.initial_state['id']) > 0):
        new_initial_state = {'id': 'A', 'is_initial': False}
        self.add_new_state(new_initial_state)
        self.finite_automata['edges'].append({'source': 'A', 'target': self.initial_state['id'], 'label': 'λ'})
        self.set_initial_state('A')
        
        # 2 - Create a new final state with a λ transition from all old final states We can skip this step if there is exactly one final state and it has out-degree 0.)
        if(len(self.final_states) == 1 and self.get_out_degree(self.final_states[0]['id']) == 0):
            pass
        else:
            new_final_state = {'id': 'B', 'is_final': False}
            self.add_new_state(new_final_state)
            
            for state in self.final_states:
                self.finite_automata['edges'].append({'source': state['id'], 'target': 'B', 'label': 'λ'})
            
            # The new final state will be the ONLY final state
            self.unmark_all_final_states()
            self.set_final_state('B')
            
            
        # 3 - For each intermediate state (neither final or initial) check for self loops
        regex = []
        
        # Unify multiple edges (same Source and Target)
        self.unify_multiple_transitions()
        
        # 4 - Eliminate the states and connect  the edges
        def remove_state(state):
            #print(f"\n\ncurrent state {state} \n\n")
            if(not state.get('is_final', False) and not state.get('is_initial', False)): # Not initial neither final
                #if(self.check_self_loop(state['id'])): # If has self loop
                new_transitions = []
                transitions_to_remove = []
                self_loops = self.get_self_loops(state['id'])
                for transition in self.finite_automata['edges']:
                    remove_transition = False
                    if(transition['target'] == state['id'] and not transition in self_loops): # For each transition where our state is the target (SOURCE -> state -> TARGET)
                        #print(f"\n  TRANSITION  {transition} \n")
                        current_source = transition['source'] # We get the source
                        current_label_1 = transition['label']
                        for transition2 in self.finite_automata['edges']: # We search for the transitions where our state is the source
                            if(transition2['source'] == state['id'] and not transition2 in self_loops):
                                #print(f"\n      TRANSITION 2 {transition2} \n")
                                current_target = transition2['target']
                                current_label_2 = transition2['label']
                                #print(f"\n      CURRENT SOURCE {current_source}, CURRENT TARGET {current_target}\n")
                                # HERE WE MERGE THE LABELS FROM THE TRANSITIONS (EDGES)
                                # Verify if any of the labels has an "or" (|)
                                final_label_list = []
                                label_pairs = []
                                if(current_label_1 and '|' in current_label_1):
                                    if(current_label_2 and '|' in current_label_2):
                                        label_list_1 = current_label_1.split('|')
                                        label_list_2 = current_label_2.split('|')
                                        for label in label_list_1:
                                            for label2 in label_list_2:
                                                label_pairs.append([label, label2])
                                    else:
                                        label_list_1 = current_label_1.split('|')
                                        for label in label_list_1:
                                            label_pairs.append([label, current_label_2])
                                else:
                                    if(current_label_2 and '|' in current_label_2):
                                        label_list_2 = current_label_2.split('|')
                                        for label2 in label_list_2:
                                            label_pairs.append([current_label_1, label2])
                                    else:
                                        label_pairs.append([current_label_1, current_label_2])
                                
                                for pair in label_pairs:
                                    pair[0] = self.transform_empty_transition(pair[0])
                                    pair[1] = self.transform_empty_transition(pair[1])
                                    
                                    #print(f"\n          PAIR {pair} \n")
                                    if(len(self_loops) > 0):
                                        for self_loop in self_loops:
                                            split_self_loop = self_loop['label'].split('|')
                                            for self_loop_transition in split_self_loop:
                                                if(len(split_self_loop) > 1):
                                                    label_to_append = pair[0]+'('+(self_loop['label'])+')*'+pair[1]
                                                else:
                                                    label_to_append = pair[0]+'('+(self_loop_transition)+')*'+pair[1]
                                                if(not label_to_append in final_label_list):
                                                        final_label_list.append(label_to_append)
                                                if(not self_loop in transitions_to_remove):
                                                    transitions_to_remove.append(self_loop)
                                                ##print(f"\n\n NEW TRANSITION ({pair[0]}({transition})*{pair[1]})\n\n")
                                    # OLD LOOPS TREATMENT
                                    # if(len(self_loops) > 0):
                                    #     for self_loop in self_loops:
                                    #         for self_loop_transition in self_loop['label'].split('|'):
                                    #             final_label_list.append(pair[0]+'('+(self_loop_transition)+')*'+pair[1])
                                    #             if(not self_loop in transitions_to_remove):
                                    #                 transitions_to_remove.append(self_loop)
                                    #             ##print(f"\n\n NEW TRANSITION ({pair[0]}({transition})*{pair[1]})\n\n")
                                            
                                    else:
                                        final_label_list.append(pair[0]+pair[1])
                                
                                #print(f"\n      FINAL LABEL LIST {final_label_list} \n")
                                final_label = '|'.join(final_label_list) 
                                # REVIEW `current_target`
                                nt = {'source': current_source, 'target': current_target, 'label': final_label}
                                #print(f"\n      New transition to be added {nt} \n")
                                if(not nt in new_transitions):
                                    new_transitions.append(nt)
                                    
                                
                                #print(f"\n      TRANSITIONS TO REMOVE BEFORE ADD TRANSITION 2 {transitions_to_remove} \n")
                                if(not transition2 in transitions_to_remove):
                                    transitions_to_remove.append(transition2)
                                    remove_transition = True
                                    
                                #print(f"\n      TRANSITIONS TO REMOVE AFTER ADD TRANSITION 2 {transitions_to_remove} \n")     
                    
                    #print(f"\n  TRANSITIONS TO REMOVE BEFORE ADD TRANSITION 1 {transitions_to_remove} \n")
                    if(remove_transition):
                        if(not transition in transitions_to_remove):
                            transitions_to_remove.append(transition)
                    #print(f"\n  TRANSITIONS TO REMOVE AFTER ADD TRANSITION 1 {transitions_to_remove} \n")

                
                    
                #print(f"\nEDGES BEFORE: {self.finite_automata['edges']}\n")
                for transition_remove in transitions_to_remove:
                    #print(f"\nTRANSITION BEING REMOVED: {transition_remove}\n")
                    self.finite_automata['edges'].remove(transition_remove)
                #print(f"\nEDGES AFTER: {self.finite_automata['edges']}\n")
                
                for new_transition in new_transitions:
                    #print(f"\nNEW TRANSITION BEING ADDED: {transition_remove}\n")
                    #self.finite_automata['edges'].append(new_transition)
                    self.add_new_transition(new_transition['source'], new_transition['target'], new_transition['label'])
                        
                        
                self.finite_automata['nodes'].remove(state)
                ##print(f"\n\n CURRENT AUTOMAT {self.finite_automata}\n\n\n")
        
        #print("============================================================================== \n==============================================================================\n==============================================================================\n==============================================================================")
        
        #print(f"\n\n FA before remove dead states {self.finite_automata} \n\n")
        self.remove_all_dead_states()
        #print(f"\n\n FA afeter remove dead states {self.finite_automata} \n\n")
        
        cpy_nodes = copy.deepcopy(self.finite_automata["nodes"])
        for state in cpy_nodes:
            remove_state(state)
            
        regex = ''
        
        #print(f"\n\n\n LAST #PRINT {self.finite_automata['edges']} \n\n\n")
        if (len(self.finite_automata['edges']) == 1):
            regex = '(' + self.finite_automata['edges'][0]['label'] + ')'
        else:
            for edge in self.finite_automata['edges']:
                if(edge['source'] == 'A' and edge['target'] == 'B'):
                    regex = '('+edge['label']+')'
                    ##print(f"\n\nREGEX: {regex}\n\n")
                    return regex

        return regex
