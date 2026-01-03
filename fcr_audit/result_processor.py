"""
Result Processor
Processes and validates Claude API responses for FCR audit.
"""

import json
from typing import Dict, Any, List, Optional


class ResultProcessor:
    """Processes Claude API audit responses."""
    
    def __init__(self):
        """Initialize result processor."""
        pass
    
    def process_response(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process and validate Claude API response.
        
        Args:
            response: Raw response from Claude API
            
        Returns:
            Processed and validated audit results
        """
        # Validate response structure
        validated = self._validate_response(response)
        
        # Extract and structure data
        processed = {
            "obligor_name": validated.get("obligor_name", ""),
            "outstanding_limit": validated.get("outstanding_limit", ""),
            "questions": self._process_questions(validated.get("questions", [])),
            "pillar_scores": validated.get("pillar_scores", {}),
            "weighted_pillar_scores": validated.get("weighted_pillar_scores", {}),
            "issues_raised": validated.get("issues_raised", []),
        }
        
        return processed
    
    def _validate_response(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate response structure.
        
        Args:
            response: Raw response
            
        Returns:
            Validated response
        """
        if not isinstance(response, dict):
            raise ValueError("Response must be a dictionary")
        
        # Ensure required fields exist
        validated = {
            "obligor_name": response.get("obligor_name", ""),
            "outstanding_limit": response.get("outstanding_limit", ""),
            "questions": response.get("questions", []),
            "pillar_scores": response.get("pillar_scores", {}),
            "weighted_pillar_scores": response.get("weighted_pillar_scores", {}),
            "issues_raised": response.get("issues_raised", []),
        }
        
        # Validate questions
        if not isinstance(validated["questions"], list):
            validated["questions"] = []
        
        # Ensure we have 16 questions
        if len(validated["questions"]) < 16:
            # Try to fill missing questions
            validated["questions"] = self._fill_missing_questions(validated["questions"])
        
        return validated
    
    def _fill_missing_questions(self, questions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Fill in missing questions if response is incomplete.
        
        Args:
            questions: List of question responses
            
        Returns:
            Complete list with 16 questions
        """
        from .audit_prompt import AuditPrompt
        
        question_numbers = {q.get("question_number") for q in questions if isinstance(q, dict)}
        
        complete_questions = []
        for i in range(1, 17):
            # Find existing question or create placeholder
            existing = next((q for q in questions if q.get("question_number") == i), None)
            
            if existing:
                complete_questions.append(existing)
            else:
                # Create placeholder question
                question_info = AuditPrompt.get_question_by_number(i)
                complete_questions.append({
                    "question_number": i,
                    "question_text": question_info["text"] if question_info else f"Question {i}",
                    "score": 1,  # Default to lowest score if missing
                    "justification": "Question not addressed in response",
                    "citation": "N/A",
                    "pillar": question_info["pillar"] if question_info else "Unknown",
                    "finding": "Response incomplete - question not evaluated"
                })
        
        return complete_questions
    
    def _process_questions(self, questions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Process and validate individual questions.
        
        Args:
            questions: List of question dictionaries
            
        Returns:
            Processed questions
        """
        processed = []
        
        for q in questions:
            if not isinstance(q, dict):
                continue
            
            processed_q = {
                "question_number": q.get("question_number", 0),
                "question_text": q.get("question_text", ""),
                "score": self._validate_score(q.get("score", 1)),
                "justification": q.get("justification", ""),
                "citation": q.get("citation", "N/A"),
                "pillar": q.get("pillar", "Unknown"),
                "finding": q.get("finding") if q.get("score", 1) <= 2 else None,
            }
            
            processed.append(processed_q)
        
        # Sort by question number
        processed.sort(key=lambda x: x["question_number"])
        
        return processed
    
    def _validate_score(self, score: Any) -> int:
        """
        Validate and normalize score.
        
        Args:
            score: Score value
            
        Returns:
            Validated score (1-4)
        """
        try:
            score_int = int(score)
            if score_int < 1:
                return 1
            elif score_int > 4:
                return 4
            return score_int
        except (ValueError, TypeError):
            return 1  # Default to lowest score if invalid
    
    def extract_issues(self, processed_response: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Extract all issues (questions with score <= 2).
        
        Args:
            processed_response: Processed audit response
            
        Returns:
            List of issues
        """
        issues = []
        
        for q in processed_response.get("questions", []):
            if q.get("score", 4) <= 2:
                issues.append({
                    "question_number": q.get("question_number"),
                    "question_text": q.get("question_text"),
                    "score": q.get("score"),
                    "finding": q.get("finding", q.get("justification", "")),
                    "pillar": q.get("pillar"),
                })
        
        return issues
    
    def get_summary_stats(self, processed_response: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get summary statistics from processed response.
        
        Args:
            processed_response: Processed audit response
            
        Returns:
            Summary statistics
        """
        questions = processed_response.get("questions", [])
        
        if not questions:
            return {
                "total_questions": 0,
                "average_score": 0,
                "critical_issues": 0,
                "significant_issues": 0,
                "adequate_responses": 0,
                "excellent_responses": 0,
            }
        
        scores = [q.get("score", 1) for q in questions]
        
        return {
            "total_questions": len(questions),
            "average_score": sum(scores) / len(scores) if scores else 0,
            "critical_issues": sum(1 for s in scores if s == 1),
            "significant_issues": sum(1 for s in scores if s == 2),
            "adequate_responses": sum(1 for s in scores if s == 3),
            "excellent_responses": sum(1 for s in scores if s == 4),
        }

