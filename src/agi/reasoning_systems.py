# Advanced Reasoning Systems for Artificial General Intelligence (AGI)

import random

class DeductiveReasoning:
    def __init__(self):
        self.rules = []

    def add_rule(self, premises, conclusion):
        # Each rule is a tuple of (set of premises, conclusion)
        self.rules.append((set(premises), conclusion))

    def reason(self, facts):
        # Deduce conclusions from the facts using the rules
        conclusions = set()
        for premises, conclusion in self.rules:
            if premises.issubset(facts):
                conclusions.add(conclusion)
        return conclusions

class InductiveReasoning:
    def __init__(self):
        self.observations = []

    def observe(self, instance):
        self.observations.append(instance)

    def generalize(self):
        # Probabilistic generalization based on the frequency of observations
        if not self.observations:
            return None
        observation_counts = {obs: self.observations.count(obs) for obs in set(self.observations)}
        total_observations = len(self.observations)
        probabilities = {obs: count / total_observations for obs, count in observation_counts.items()}
        return max(probabilities, key=probabilities.get), probabilities

class AbductiveReasoning:
    def __init__(self):
        self.hypotheses = []

    def generate_hypothesis(self, observation):
        # Generate multiple hypotheses for a given observation
        hypothesis = f"Possible explanation for {observation}"
        self.hypotheses.append(hypothesis)
        return hypothesis

    def evaluate_hypotheses(self, evidence):
        # Rank hypotheses based on how well they match the evidence
        ranked_hypotheses = sorted(
            self.hypotheses, 
            key=lambda hyp: sum(1 for item in evidence if item in hyp), 
            reverse=True
        )
        return ranked_hypotheses

class EthicalReasoning:
    def __init__(self, ethical_rules=None):
        if ethical_rules is None:
            ethical_rules = ['do no harm', 'ensure fairness']
        self.ethical_rules = ethical_rules

    def evaluate_decision(self, decision):
        # Evaluate the decision against ethical rules
        for rule in self.ethical_rules:
            if rule == 'do no harm' and 'harmful' in decision.lower():
                return False
            if rule == 'ensure fairness' and 'unfair' in decision.lower():
                return False
        return True

class CognitiveReasoningSystem:
    def __init__(self):
        self.deductive = DeductiveReasoning()
        self.inductive = InductiveReasoning()
        self.abductive = AbductiveReasoning()
        self.ethical = EthicalReasoning()

    def process_facts(self, facts):
        deductive_conclusions = self.deductive.reason(facts)
        inductive_generalization, probabilities = self.inductive.generalize()
        abductive_hypotheses = self.abductive.evaluate_hypotheses(facts)
        
        reasoning_output = {
            'deductive': deductive_conclusions,
            'inductive': {'generalization': inductive_generalization, 'probabilities': probabilities},
            'abductive': abductive_hypotheses
        }

        # Evaluate reasoning output against ethical considerations
        ethical_decisions = {
            'deductive': self.ethical.evaluate_decision(str(deductive_conclusions)),
            'inductive': self.ethical.evaluate_decision(str(inductive_generalization)),
            'abductive': self.ethical.evaluate_decision(str(abductive_hypotheses[0] if abductive_hypotheses else ""))
        }

        return reasoning_output, ethical_decisions

# Example of usage
if __name__ == "__main__":
    reasoning_system = CognitiveReasoningSystem()

    # Add rules for deductive reasoning
    reasoning_system.deductive.add_rule({'Socrates is a man'}, 'Socrates is mortal')
    reasoning_system.deductive.add_rule({'All men are mortal'}, 'Socrates is mortal')
    reasoning_system.deductive.add_rule({'It is raining'}, 'The ground will be wet')

    # Observe instances for inductive reasoning
    reasoning_system.inductive.observe('The sun rises in the east')
    reasoning_system.inductive.observe('The sun rises in the east')
    reasoning_system.inductive.observe('The sun rises in the east')
    reasoning_system.inductive.observe('The sun sets in the west')

    # Generate a hypothesis for abductive reasoning
    reasoning_system.abductive.generate_hypothesis('The ground is wet')

    # Process facts using all reasoning systems
    facts = {'Socrates is a man', 'All men are mortal', 'The ground is wet'}
    conclusions, ethical_evaluation = reasoning_system.process_facts(facts)
    
    print("Conclusions:", conclusions)
    print("Ethical Evaluation:", ethical_evaluation)
