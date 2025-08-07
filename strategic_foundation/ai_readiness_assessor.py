"""
AI Readiness Assessment Tool
Comprehensive organizational AI readiness evaluation with capability gap analysis
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Tuple, Any
import json
from datetime import datetime


class ReadinessDimension(Enum):
    STRATEGIC_ALIGNMENT = "strategic_alignment"
    LEADERSHIP_COMMITMENT = "leadership_commitment"
    DATA_MATURITY = "data_maturity"
    TECHNICAL_INFRASTRUCTURE = "technical_infrastructure"
    TALENT_CAPABILITIES = "talent_capabilities"
    ORGANIZATIONAL_CULTURE = "organizational_culture"
    CHANGE_MANAGEMENT = "change_management"
    GOVERNANCE_ETHICS = "governance_ethics"


class MaturityScore(Enum):
    NASCENT = 1      # 0-20%: Initial awareness, ad-hoc activities
    EMERGING = 2     # 21-40%: Some structured approaches, limited scale
    DEVELOPING = 3   # 41-60%: Systematic approach, moderate scale
    ADVANCED = 4     # 61-80%: Mature processes, enterprise scale
    OPTIMIZING = 5   # 81-100%: Continuous improvement, industry leading


@dataclass
class AssessmentQuestion:
    dimension: ReadinessDimension
    question: str
    weight: float
    scoring_guide: Dict[int, str]
    follow_up_questions: List[str] = field(default_factory=list)


@dataclass
class DimensionAssessment:
    dimension: ReadinessDimension
    raw_score: float
    weighted_score: float
    maturity_level: MaturityScore
    strengths: List[str] = field(default_factory=list)
    gaps: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
    priority: str = "medium"  # high, medium, low


@dataclass
class ReadinessReport:
    organization_name: str
    assessment_date: datetime
    overall_score: float
    overall_maturity: MaturityScore
    dimension_scores: Dict[ReadinessDimension, DimensionAssessment]
    top_strengths: List[str]
    critical_gaps: List[str]
    priority_recommendations: List[str]
    implementation_roadmap: Dict[str, List[str]]
    estimated_timeline_months: int


class AIReadinessAssessor:
    """
    Comprehensive AI readiness assessment tool for enterprise organizations
    """
    
    def __init__(self):
        self.assessment_questions = self._initialize_questions()
        self.industry_benchmarks = self._load_industry_benchmarks()
    
    def conduct_assessment(self, organization_name: str, responses: Dict[str, int]) -> ReadinessReport:
        """Conduct comprehensive AI readiness assessment"""
        
        # Calculate dimension scores
        dimension_assessments = {}
        total_weighted_score = 0
        total_weight = 0
        
        for dimension in ReadinessDimension:
            assessment = self._assess_dimension(dimension, responses)
            dimension_assessments[dimension] = assessment
            total_weighted_score += assessment.weighted_score
            total_weight += self._get_dimension_weight(dimension)
        
        # Calculate overall score and maturity
        overall_score = total_weighted_score / total_weight if total_weight > 0 else 0
        overall_maturity = self._score_to_maturity(overall_score)
        
        # Generate insights
        top_strengths = self._identify_top_strengths(dimension_assessments)
        critical_gaps = self._identify_critical_gaps(dimension_assessments)
        priority_recommendations = self._generate_priority_recommendations(dimension_assessments)
        implementation_roadmap = self._create_implementation_roadmap(dimension_assessments)
        timeline = self._estimate_timeline(dimension_assessments, overall_score)
        
        return ReadinessReport(
            organization_name=organization_name,
            assessment_date=datetime.now(),
            overall_score=overall_score,
            overall_maturity=overall_maturity,
            dimension_scores=dimension_assessments,
            top_strengths=top_strengths,
            critical_gaps=critical_gaps,
            priority_recommendations=priority_recommendations,
            implementation_roadmap=implementation_roadmap,
            estimated_timeline_months=timeline
        )
    
    def generate_capability_gap_analysis(self, report: ReadinessReport) -> Dict[str, Any]:
        """Generate detailed capability gap analysis with prioritization"""
        
        gaps_analysis = {
            "critical_gaps": [],
            "moderate_gaps": [],
            "minor_gaps": [],
            "gap_priorities": {},
            "resource_requirements": {},
            "quick_wins": []
        }
        
        for dimension, assessment in report.dimension_scores.items():
            if assessment.maturity_level.value <= 2:  # Nascent or Emerging
                gap_info = {
                    "dimension": dimension.value,
                    "current_maturity": assessment.maturity_level.value,
                    "gaps": assessment.gaps,
                    "impact": self._assess_gap_impact(dimension, assessment.maturity_level),
                    "effort": self._assess_effort_required(dimension, assessment.maturity_level)
                }
                
                if assessment.maturity_level.value == 1:
                    gaps_analysis["critical_gaps"].append(gap_info)
                else:
                    gaps_analysis["moderate_gaps"].append(gap_info)
                
                # Identify quick wins (high impact, low effort)
                if gap_info["impact"] >= 4 and gap_info["effort"] <= 2:
                    gaps_analysis["quick_wins"].append({
                        "dimension": dimension.value,
                        "opportunity": f"Quick improvement in {dimension.value}",
                        "expected_benefit": "High impact with minimal resources"
                    })
        
        return gaps_analysis
    
    def create_development_roadmap(self, report: ReadinessReport) -> Dict[str, Any]:
        """Create detailed development roadmap with phases and milestones"""
        
        roadmap = {
            "phase_1_foundation": {
                "duration_months": 3,
                "objectives": [],
                "activities": [],
                "success_metrics": {}
            },
            "phase_2_development": {
                "duration_months": 6,
                "objectives": [],
                "activities": [],
                "success_metrics": {}
            },
            "phase_3_maturation": {
                "duration_months": 9,
                "objectives": [],
                "activities": [],
                "success_metrics": {}
            }
        }
        
        # Prioritize dimensions based on current maturity and strategic importance
        prioritized_dimensions = self._prioritize_dimensions(report.dimension_scores)
        
        for phase_name, phase_data in roadmap.items():
            phase_number = int(phase_name.split("_")[1])
            
            for dimension, assessment in prioritized_dimensions[:3]:  # Focus on top 3 per phase
                if assessment.maturity_level.value < phase_number + 2:  # Room for improvement
                    phase_data["objectives"].append(f"Improve {dimension.value} maturity")
                    phase_data["activities"].extend(assessment.recommendations[:2])
                    phase_data["success_metrics"][dimension.value] = min(5, assessment.maturity_level.value + 1)
        
        return roadmap
    
    def _initialize_questions(self) -> List[AssessmentQuestion]:
        """Initialize comprehensive assessment questions across all dimensions"""
        
        questions = [
            # Strategic Alignment
            AssessmentQuestion(
                dimension=ReadinessDimension.STRATEGIC_ALIGNMENT,
                question="How well are AI initiatives aligned with business strategy?",
                weight=0.15,
                scoring_guide={
                    1: "No clear connection between AI and business strategy",
                    2: "Some AI projects exist but limited strategic alignment",
                    3: "AI initiatives generally support business objectives",
                    4: "AI is integral to achieving strategic goals",
                    5: "AI drives competitive advantage and strategic differentiation"
                }
            ),
            
            # Leadership Commitment
            AssessmentQuestion(
                dimension=ReadinessDimension.LEADERSHIP_COMMITMENT,
                question="What level of commitment do senior leaders show for AI transformation?",
                weight=0.15,
                scoring_guide={
                    1: "Limited awareness or interest from leadership",
                    2: "Some leadership interest but inconsistent support",
                    3: "Moderate leadership support with allocated resources",
                    4: "Strong leadership commitment with clear accountability",
                    5: "Leadership champions AI transformation organization-wide"
                }
            ),
            
            # Data Maturity
            AssessmentQuestion(
                dimension=ReadinessDimension.DATA_MATURITY,
                question="How mature are your data management and governance capabilities?",
                weight=0.15,
                scoring_guide={
                    1: "Data is siloed with poor quality and governance",
                    2: "Basic data management with some quality issues",
                    3: "Structured data governance with moderate quality",
                    4: "Advanced data management with high quality standards",
                    5: "Best-in-class data platform enabling AI at scale"
                }
            ),
            
            # Technical Infrastructure
            AssessmentQuestion(
                dimension=ReadinessDimension.TECHNICAL_INFRASTRUCTURE,
                question="How ready is your technical infrastructure for AI workloads?",
                weight=0.12,
                scoring_guide={
                    1: "Legacy systems with no AI-ready infrastructure",
                    2: "Some modern systems but limited AI capabilities",
                    3: "Adequate infrastructure with some AI tools",
                    4: "Modern infrastructure well-suited for AI deployment",
                    5: "Cloud-native, scalable AI-optimized infrastructure"
                }
            ),
            
            # Talent Capabilities
            AssessmentQuestion(
                dimension=ReadinessDimension.TALENT_CAPABILITIES,
                question="What is the current state of AI talent and skills in your organization?",
                weight=0.13,
                scoring_guide={
                    1: "No dedicated AI talent or skills",
                    2: "Limited AI skills scattered across teams",
                    3: "Some AI expertise with basic capabilities",
                    4: "Strong AI team with proven track record",
                    5: "World-class AI talent driving innovation"
                }
            ),
            
            # Organizational Culture
            AssessmentQuestion(
                dimension=ReadinessDimension.ORGANIZATIONAL_CULTURE,
                question="How supportive is your organizational culture toward AI adoption?",
                weight=0.12,
                scoring_guide={
                    1: "Resistance to change and new technologies",
                    2: "Cautious approach with some cultural barriers",
                    3: "Generally open to AI with moderate enthusiasm",
                    4: "Embraces AI with strong innovation culture",
                    5: "AI-first mindset embedded in organizational DNA"
                }
            ),
            
            # Change Management
            AssessmentQuestion(
                dimension=ReadinessDimension.CHANGE_MANAGEMENT,
                question="How effective are your change management capabilities?",
                weight=0.10,
                scoring_guide={
                    1: "No formal change management processes",
                    2: "Basic change management with limited success",
                    3: "Structured change management with moderate results",
                    4: "Advanced change management with high success rates",
                    5: "Exceptional change management enabling rapid transformation"
                }
            ),
            
            # Governance & Ethics
            AssessmentQuestion(
                dimension=ReadinessDimension.GOVERNANCE_ETHICS,
                question="How mature are your AI governance and ethics frameworks?",
                weight=0.08,
                scoring_guide={
                    1: "No AI governance or ethics considerations",
                    2: "Basic awareness but no formal frameworks",
                    3: "Initial governance structures with some policies",
                    4: "Comprehensive governance with clear ethics guidelines",
                    5: "Leading-edge responsible AI governance and ethics"
                }
            )
        ]
        
        return questions
    
    def _assess_dimension(self, dimension: ReadinessDimension, responses: Dict[str, int]) -> DimensionAssessment:
        """Assess individual dimension based on responses"""
        
        dimension_questions = [q for q in self.assessment_questions if q.dimension == dimension]
        
        if not dimension_questions:
            return DimensionAssessment(
                dimension=dimension,
                raw_score=0,
                weighted_score=0,
                maturity_level=MaturityScore.NASCENT
            )
        
        total_score = 0
        total_weight = 0
        
        for question in dimension_questions:
            response_key = f"{dimension.value}_{hash(question.question) % 1000}"
            response = responses.get(response_key, 3)  # Default to middle score
            total_score += response * question.weight
            total_weight += question.weight
        
        raw_score = total_score / total_weight if total_weight > 0 else 0
        weighted_score = raw_score * self._get_dimension_weight(dimension)
        maturity_level = self._score_to_maturity(raw_score)
        
        # Generate dimension-specific insights
        strengths, gaps, recommendations = self._generate_dimension_insights(dimension, maturity_level)
        priority = self._assess_dimension_priority(dimension, maturity_level)
        
        return DimensionAssessment(
            dimension=dimension,
            raw_score=raw_score,
            weighted_score=weighted_score,
            maturity_level=maturity_level,
            strengths=strengths,
            gaps=gaps,
            recommendations=recommendations,
            priority=priority
        )
    
    def _get_dimension_weight(self, dimension: ReadinessDimension) -> float:
        """Get strategic weight for each dimension"""
        weights = {
            ReadinessDimension.STRATEGIC_ALIGNMENT: 1.0,
            ReadinessDimension.LEADERSHIP_COMMITMENT: 1.0,
            ReadinessDimension.DATA_MATURITY: 0.9,
            ReadinessDimension.TECHNICAL_INFRASTRUCTURE: 0.8,
            ReadinessDimension.TALENT_CAPABILITIES: 0.9,
            ReadinessDimension.ORGANIZATIONAL_CULTURE: 0.8,
            ReadinessDimension.CHANGE_MANAGEMENT: 0.7,
            ReadinessDimension.GOVERNANCE_ETHICS: 0.6
        }
        return weights.get(dimension, 1.0)
    
    def _score_to_maturity(self, score: float) -> MaturityScore:
        """Convert numerical score to maturity level"""
        if score <= 1.0:
            return MaturityScore.NASCENT
        elif score <= 2.0:
            return MaturityScore.EMERGING
        elif score <= 3.0:
            return MaturityScore.DEVELOPING
        elif score <= 4.0:
            return MaturityScore.ADVANCED
        else:
            return MaturityScore.OPTIMIZING
    
    def _generate_dimension_insights(self, dimension: ReadinessDimension, maturity: MaturityScore) -> Tuple[List[str], List[str], List[str]]:
        """Generate dimension-specific strengths, gaps, and recommendations"""
        
        insights = {
            ReadinessDimension.STRATEGIC_ALIGNMENT: {
                MaturityScore.NASCENT: (
                    [],
                    ["No clear AI strategy", "Disconnected from business goals"],
                    ["Develop AI vision statement", "Align AI initiatives with business strategy"]
                ),
                MaturityScore.EMERGING: (
                    ["Some strategic awareness"],
                    ["Inconsistent strategic alignment"],
                    ["Create AI strategy document", "Establish governance board"]
                ),
                MaturityScore.DEVELOPING: (
                    ["Basic strategic framework"],
                    ["Limited strategic integration"],
                    ["Enhance strategy integration", "Develop success metrics"]
                ),
                MaturityScore.ADVANCED: (
                    ["Strong strategic alignment"],
                    ["Opportunity for deeper integration"],
                    ["Optimize strategic outcomes", "Expand competitive advantage"]
                ),
                MaturityScore.OPTIMIZING: (
                    ["Exemplary strategic integration", "AI drives competitive advantage"],
                    [],
                    ["Share best practices", "Lead industry transformation"]
                )
            },
            # Add similar insights for other dimensions...
        }
        
        default_insights = ([], ["Assessment needed"], ["Conduct detailed evaluation"])
        return insights.get(dimension, {}).get(maturity, default_insights)
    
    def _assess_dimension_priority(self, dimension: ReadinessDimension, maturity: MaturityScore) -> str:
        """Assess priority level for dimension improvement"""
        
        # Strategic dimensions get higher priority
        strategic_dimensions = [
            ReadinessDimension.STRATEGIC_ALIGNMENT,
            ReadinessDimension.LEADERSHIP_COMMITMENT,
            ReadinessDimension.DATA_MATURITY
        ]
        
        if dimension in strategic_dimensions and maturity.value <= 2:
            return "high"
        elif maturity.value <= 1:
            return "high"
        elif maturity.value <= 3:
            return "medium"
        else:
            return "low"
    
    def _identify_top_strengths(self, assessments: Dict[ReadinessDimension, DimensionAssessment]) -> List[str]:
        """Identify organization's top strengths across dimensions"""
        
        strengths = []
        for assessment in assessments.values():
            if assessment.maturity_level.value >= 4:  # Advanced or Optimizing
                strengths.extend(assessment.strengths)
        
        return strengths[:5]  # Return top 5 strengths
    
    def _identify_critical_gaps(self, assessments: Dict[ReadinessDimension, DimensionAssessment]) -> List[str]:
        """Identify critical capability gaps requiring immediate attention"""
        
        critical_gaps = []
        for assessment in assessments.values():
            if assessment.priority == "high":
                critical_gaps.extend(assessment.gaps)
        
        return critical_gaps[:5]  # Return top 5 critical gaps
    
    def _generate_priority_recommendations(self, assessments: Dict[ReadinessDimension, DimensionAssessment]) -> List[str]:
        """Generate prioritized recommendations based on assessment results"""
        
        recommendations = []
        
        # Sort assessments by priority and maturity level
        sorted_assessments = sorted(
            assessments.items(),
            key=lambda x: (x[1].priority == "high", -x[1].maturity_level.value)
        )
        
        for dimension, assessment in sorted_assessments:
            if assessment.priority in ["high", "medium"]:
                recommendations.extend(assessment.recommendations[:2])
        
        return recommendations[:8]  # Return top 8 recommendations
    
    def _create_implementation_roadmap(self, assessments: Dict[ReadinessDimension, DimensionAssessment]) -> Dict[str, List[str]]:
        """Create phased implementation roadmap"""
        
        roadmap = {
            "immediate_actions": [],
            "short_term_goals": [],
            "medium_term_objectives": [],
            "long_term_vision": []
        }
        
        for assessment in assessments.values():
            if assessment.priority == "high":
                roadmap["immediate_actions"].extend(assessment.recommendations[:1])
            elif assessment.priority == "medium":
                roadmap["short_term_goals"].extend(assessment.recommendations[:1])
            else:
                roadmap["medium_term_objectives"].extend(assessment.recommendations[:1])
        
        return roadmap
    
    def _estimate_timeline(self, assessments: Dict[ReadinessDimension, DimensionAssessment], overall_score: float) -> int:
        """Estimate transformation timeline in months"""
        
        base_timeline = 18  # Base 18 months
        
        # Adjust based on overall maturity
        if overall_score <= 2.0:
            timeline_multiplier = 1.5
        elif overall_score <= 3.0:
            timeline_multiplier = 1.2
        elif overall_score <= 4.0:
            timeline_multiplier = 1.0
        else:
            timeline_multiplier = 0.8
        
        # Count high priority gaps
        high_priority_count = sum(1 for a in assessments.values() if a.priority == "high")
        priority_months = high_priority_count * 2
        
        return int(base_timeline * timeline_multiplier + priority_months)
    
    def _assess_gap_impact(self, dimension: ReadinessDimension, maturity: MaturityScore) -> int:
        """Assess the business impact of capability gaps (1-5 scale)"""
        
        strategic_impact = {
            ReadinessDimension.STRATEGIC_ALIGNMENT: 5,
            ReadinessDimension.LEADERSHIP_COMMITMENT: 5,
            ReadinessDimension.DATA_MATURITY: 4,
            ReadinessDimension.TALENT_CAPABILITIES: 4,
            ReadinessDimension.TECHNICAL_INFRASTRUCTURE: 3,
            ReadinessDimension.ORGANIZATIONAL_CULTURE: 3,
            ReadinessDimension.CHANGE_MANAGEMENT: 2,
            ReadinessDimension.GOVERNANCE_ETHICS: 2
        }
        
        base_impact = strategic_impact.get(dimension, 3)
        maturity_penalty = max(0, 3 - maturity.value)  # Lower maturity = higher impact
        
        return min(5, base_impact + maturity_penalty)
    
    def _assess_effort_required(self, dimension: ReadinessDimension, maturity: MaturityScore) -> int:
        """Assess effort required to improve capability (1-5 scale)"""
        
        effort_factors = {
            ReadinessDimension.STRATEGIC_ALIGNMENT: 2,  # Easier to improve
            ReadinessDimension.LEADERSHIP_COMMITMENT: 2,
            ReadinessDimension.GOVERNANCE_ETHICS: 2,
            ReadinessDimension.CHANGE_MANAGEMENT: 3,
            ReadinessDimension.ORGANIZATIONAL_CULTURE: 4,  # Harder to change
            ReadinessDimension.DATA_MATURITY: 4,
            ReadinessDimension.TECHNICAL_INFRASTRUCTURE: 4,
            ReadinessDimension.TALENT_CAPABILITIES: 5  # Most difficult
        }
        
        return effort_factors.get(dimension, 3)
    
    def _prioritize_dimensions(self, assessments: Dict[ReadinessDimension, DimensionAssessment]) -> List[Tuple[ReadinessDimension, DimensionAssessment]]:
        """Prioritize dimensions for development focus"""
        
        return sorted(
            assessments.items(),
            key=lambda x: (
                x[1].priority == "high",
                -self._get_dimension_weight(x[0]),
                -x[1].maturity_level.value
            ),
            reverse=True
        )
    
    def _load_industry_benchmarks(self) -> Dict[str, Dict]:
        """Load industry-specific benchmarks for comparison"""
        
        # This would typically load from a database or configuration file
        return {
            "financial_services": {
                "average_scores": {
                    "strategic_alignment": 3.2,
                    "data_maturity": 3.8,
                    "governance_ethics": 4.1
                }
            },
            "healthcare": {
                "average_scores": {
                    "strategic_alignment": 2.8,
                    "data_maturity": 3.1,
                    "governance_ethics": 3.9
                }
            },
            "manufacturing": {
                "average_scores": {
                    "strategic_alignment": 3.1,
                    "technical_infrastructure": 3.6,
                    "data_maturity": 3.4
                }
            }
        }


def main():
    """Example usage of the AI Readiness Assessor"""
    assessor = AIReadinessAssessor()
    
    # Example responses (in practice, these would come from a survey or interview)
    sample_responses = {
        "strategic_alignment_123": 3,
        "leadership_commitment_456": 4,
        "data_maturity_789": 2,
        "technical_infrastructure_012": 3,
        "talent_capabilities_345": 2,
        "organizational_culture_678": 3,
        "change_management_901": 3,
        "governance_ethics_234": 2
    }
    
    # Conduct assessment
    report = assessor.conduct_assessment("TechCorp", sample_responses)
    
    print(f"AI Readiness Assessment for {report.organization_name}")
    print(f"Overall Score: {report.overall_score:.1f}/5.0")
    print(f"Overall Maturity: {report.overall_maturity.name}")
    print(f"Estimated Timeline: {report.estimated_timeline_months} months")
    
    # Generate capability gap analysis
    gap_analysis = assessor.generate_capability_gap_analysis(report)
    print(f"\nCritical Gaps: {len(gap_analysis['critical_gaps'])}")
    print(f"Quick Win Opportunities: {len(gap_analysis['quick_wins'])}")
    
    # Create development roadmap
    roadmap = assessor.create_development_roadmap(report)
    print(f"\nDevelopment Roadmap Created with {len(roadmap)} phases")


if __name__ == "__main__":
    main()