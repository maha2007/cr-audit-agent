"""
Scoring Calculator
Calculates weighted pillar scores and generates summary statistics.
"""

from typing import Dict, Any, List
from .audit_prompt import AuditPrompt


class ScoringCalculator:
    """Calculates weighted scores for FCR audit pillars."""
    
    def __init__(self):
        """Initialize scoring calculator."""
        self.pillar_weights = AuditPrompt.PILLARS
    
    def calculate_pillar_scores(self, questions: List[Dict[str, Any]]) -> Dict[str, float]:
        """
        Calculate unweighted average scores for each pillar.
        
        Args:
            questions: List of question responses with scores
            
        Returns:
            Dictionary mapping pillar names to average scores
        """
        pillar_scores = {}
        pillar_counts = {}
        
        # Initialize all pillars
        for pillar in self.pillar_weights.keys():
            pillar_scores[pillar] = 0.0
            pillar_counts[pillar] = 0
        
        # Sum scores by pillar
        for q in questions:
            pillar = q.get("pillar", "")
            score = q.get("score", 1)
            
            if pillar in pillar_scores:
                pillar_scores[pillar] += score
                pillar_counts[pillar] += 1
        
        # Calculate averages
        for pillar in pillar_scores.keys():
            if pillar_counts[pillar] > 0:
                pillar_scores[pillar] = pillar_scores[pillar] / pillar_counts[pillar]
            else:
                pillar_scores[pillar] = 0.0
        
        return pillar_scores
    
    def calculate_weighted_scores(self, pillar_scores: Dict[str, float]) -> Dict[str, float]:
        """
        Calculate weighted pillar scores.
        
        Args:
            pillar_scores: Unweighted pillar scores
            
        Returns:
            Dictionary mapping pillar names to weighted scores
        """
        weighted_scores = {}
        
        for pillar, weight in self.pillar_weights.items():
            unweighted_score = pillar_scores.get(pillar, 0.0)
            weighted_scores[pillar] = unweighted_score * weight
        
        return weighted_scores
    
    def calculate_overall_score(self, weighted_scores: Dict[str, float]) -> float:
        """
        Calculate overall weighted score.
        
        Args:
            weighted_scores: Weighted pillar scores
            
        Returns:
            Overall score (sum of weighted scores)
        """
        return sum(weighted_scores.values())
    
    def get_pillar_summary(self, questions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Get comprehensive pillar summary.
        
        Args:
            questions: List of question responses
            
        Returns:
            Comprehensive summary dictionary
        """
        pillar_scores = self.calculate_pillar_scores(questions)
        weighted_scores = self.calculate_weighted_scores(pillar_scores)
        overall_score = self.calculate_overall_score(weighted_scores)
        
        # Count issues by pillar
        issues_by_pillar = {}
        for pillar in self.pillar_weights.keys():
            issues_by_pillar[pillar] = sum(
                1 for q in questions 
                if q.get("pillar") == pillar and q.get("score", 4) <= 2
            )
        
        total_issues = sum(issues_by_pillar.values())
        
        return {
            "pillar_scores": pillar_scores,
            "weighted_pillar_scores": weighted_scores,
            "overall_score": overall_score,
            "issues_by_pillar": issues_by_pillar,
            "total_issues": total_issues,
        }
    
    def get_question_pillar_mapping(self) -> Dict[int, str]:
        """
        Get mapping of question numbers to pillars.
        
        Returns:
            Dictionary mapping question numbers to pillar names
        """
        mapping = {}
        for q in AuditPrompt.QUESTIONS:
            mapping[q["number"]] = q["pillar"]
        return mapping

