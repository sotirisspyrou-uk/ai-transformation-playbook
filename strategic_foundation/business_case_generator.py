"""
AI Business Case Generator
Automated business case development with ROI calculations and executive presentations
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Tuple, Any
import json
from datetime import datetime, timedelta
import numpy as np


class InvestmentType(Enum):
    INFRASTRUCTURE = "infrastructure"
    TALENT = "talent"
    TECHNOLOGY = "technology"
    TRAINING = "training"
    CONSULTING = "consulting"
    OPERATIONS = "operations"


class BenefitCategory(Enum):
    REVENUE_GROWTH = "revenue_growth"
    COST_REDUCTION = "cost_reduction"
    PRODUCTIVITY_IMPROVEMENT = "productivity_improvement"
    RISK_MITIGATION = "risk_mitigation"
    CUSTOMER_EXPERIENCE = "customer_experience"
    COMPLIANCE = "compliance"


class RiskLevel(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    VERY_HIGH = 4


@dataclass
class Investment:
    category: InvestmentType
    description: str
    year_1_cost: float
    year_2_cost: float
    year_3_cost: float
    ongoing_annual_cost: float = 0.0
    confidence_level: float = 0.85  # 0-1 scale


@dataclass
class Benefit:
    category: BenefitCategory
    description: str
    year_1_value: float
    year_2_value: float
    year_3_value: float
    ongoing_annual_value: float = 0.0
    confidence_level: float = 0.75  # 0-1 scale
    realization_probability: float = 0.80  # 0-1 scale


@dataclass
class RiskFactor:
    risk: str
    impact: RiskLevel
    probability: float  # 0-1 scale
    mitigation_strategy: str
    mitigation_cost: float = 0.0
    residual_impact: RiskLevel = RiskLevel.LOW


@dataclass
class Scenario:
    name: str
    probability: float
    roi_adjustment: float
    timeline_adjustment: int  # months
    description: str


@dataclass
class FinancialProjection:
    total_investment: float
    total_benefits: float
    net_present_value: float
    roi_percentage: float
    payback_period_months: int
    irr: float  # Internal Rate of Return
    yearly_cashflow: List[float]


@dataclass
class BusinessCase:
    organization_name: str
    initiative_name: str
    executive_summary: str
    strategic_alignment: str
    financial_projection: FinancialProjection
    investments: List[Investment]
    benefits: List[Benefit]
    risks: List[RiskFactor]
    scenarios: List[Scenario]
    implementation_timeline: Dict[str, int]  # phase -> months
    success_metrics: Dict[str, float]
    approval_recommendation: str
    created_date: datetime
    confidence_score: float


class BusinessCaseGenerator:
    """
    Automated business case generator for AI transformation initiatives
    """
    
    def __init__(self):
        self.industry_benchmarks = self._load_industry_benchmarks()
        self.investment_templates = self._initialize_investment_templates()
        self.benefit_models = self._initialize_benefit_models()
        self.risk_library = self._initialize_risk_library()
        self.discount_rate = 0.10  # 10% discount rate for NPV calculations
    
    def generate_business_case(
        self,
        organization_name: str,
        initiative_name: str,
        industry: str,
        organization_size: str,
        investment_budget: float,
        strategic_objectives: List[str],
        current_challenges: List[str]
    ) -> BusinessCase:
        """Generate comprehensive AI business case"""
        
        # Generate investments based on templates and budget
        investments = self._generate_investments(
            industry, organization_size, investment_budget
        )
        
        # Generate benefits based on objectives and industry benchmarks
        benefits = self._generate_benefits(
            industry, organization_size, strategic_objectives, investments
        )
        
        # Identify and assess risks
        risks = self._assess_risks(industry, organization_size, current_challenges)
        
        # Create financial projection
        financial_projection = self._calculate_financial_projection(investments, benefits)
        
        # Generate scenarios
        scenarios = self._generate_scenarios(industry, risks)
        
        # Create implementation timeline
        timeline = self._generate_implementation_timeline(investments, organization_size)
        
        # Define success metrics
        success_metrics = self._define_success_metrics(benefits, strategic_objectives)
        
        # Generate executive summary and recommendation
        executive_summary = self._generate_executive_summary(
            financial_projection, strategic_objectives, timeline
        )
        strategic_alignment = self._generate_strategic_alignment(strategic_objectives)
        recommendation = self._generate_approval_recommendation(financial_projection, risks)
        
        # Calculate overall confidence
        confidence_score = self._calculate_confidence_score(investments, benefits, risks)
        
        return BusinessCase(
            organization_name=organization_name,
            initiative_name=initiative_name,
            executive_summary=executive_summary,
            strategic_alignment=strategic_alignment,
            financial_projection=financial_projection,
            investments=investments,
            benefits=benefits,
            risks=risks,
            scenarios=scenarios,
            implementation_timeline=timeline,
            success_metrics=success_metrics,
            approval_recommendation=recommendation,
            created_date=datetime.now(),
            confidence_score=confidence_score
        )
    
    def perform_sensitivity_analysis(self, business_case: BusinessCase) -> Dict[str, Any]:
        """Perform sensitivity analysis on key variables"""
        
        sensitivity_results = {
            "base_case": {
                "npv": business_case.financial_projection.net_present_value,
                "roi": business_case.financial_projection.roi_percentage
            },
            "optimistic_case": {},
            "pessimistic_case": {},
            "variable_impact": {}
        }
        
        # Test optimistic scenario (+20% benefits, -10% costs)
        opt_investments = [self._adjust_investment(inv, 0.9) for inv in business_case.investments]
        opt_benefits = [self._adjust_benefit(ben, 1.2) for ben in business_case.benefits]
        opt_projection = self._calculate_financial_projection(opt_investments, opt_benefits)
        
        sensitivity_results["optimistic_case"] = {
            "npv": opt_projection.net_present_value,
            "roi": opt_projection.roi_percentage,
            "npv_change": opt_projection.net_present_value - business_case.financial_projection.net_present_value,
            "roi_change": opt_projection.roi_percentage - business_case.financial_projection.roi_percentage
        }
        
        # Test pessimistic scenario (-20% benefits, +15% costs)
        pess_investments = [self._adjust_investment(inv, 1.15) for inv in business_case.investments]
        pess_benefits = [self._adjust_benefit(ben, 0.8) for ben in business_case.benefits]
        pess_projection = self._calculate_financial_projection(pess_investments, pess_benefits)
        
        sensitivity_results["pessimistic_case"] = {
            "npv": pess_projection.net_present_value,
            "roi": pess_projection.roi_percentage,
            "npv_change": pess_projection.net_present_value - business_case.financial_projection.net_present_value,
            "roi_change": pess_projection.roi_percentage - business_case.financial_projection.roi_percentage
        }
        
        # Variable impact analysis
        variables = [
            ("Investment Cost", [0.8, 0.9, 1.1, 1.2]),
            ("Benefit Realization", [0.7, 0.85, 1.15, 1.3]),
            ("Timeline Delay", [0, 3, 6, 12])  # months
        ]
        
        for variable_name, test_values in variables:
            impacts = []
            for value in test_values:
                if variable_name == "Investment Cost":
                    test_investments = [self._adjust_investment(inv, value) for inv in business_case.investments]
                    test_projection = self._calculate_financial_projection(test_investments, business_case.benefits)
                elif variable_name == "Benefit Realization":
                    test_benefits = [self._adjust_benefit(ben, value) for ben in business_case.benefits]
                    test_projection = self._calculate_financial_projection(business_case.investments, test_benefits)
                else:  # Timeline Delay
                    # For timeline delay, adjust benefit timing
                    delayed_benefits = [self._delay_benefit(ben, value) for ben in business_case.benefits]
                    test_projection = self._calculate_financial_projection(business_case.investments, delayed_benefits)
                
                impacts.append({
                    "test_value": value,
                    "npv_impact": test_projection.net_present_value - business_case.financial_projection.net_present_value,
                    "roi_impact": test_projection.roi_percentage - business_case.financial_projection.roi_percentage
                })
            
            sensitivity_results["variable_impact"][variable_name] = impacts
        
        return sensitivity_results
    
    def generate_executive_presentation(self, business_case: BusinessCase) -> Dict[str, Any]:
        """Generate executive presentation materials"""
        
        presentation = {
            "title_slide": {
                "title": f"AI Business Case: {business_case.initiative_name}",
                "subtitle": f"Strategic AI Investment Proposal for {business_case.organization_name}",
                "date": business_case.created_date.strftime("%B %d, %Y"),
                "presenter": "AI Transformation Team"
            },
            "executive_summary": {
                "key_points": [
                    f"Investment Required: ${business_case.financial_projection.total_investment:,.0f}",
                    f"Expected ROI: {business_case.financial_projection.roi_percentage:.1f}%",
                    f"Payback Period: {business_case.financial_projection.payback_period_months} months",
                    f"Net Present Value: ${business_case.financial_projection.net_present_value:,.0f}"
                ],
                "recommendation": business_case.approval_recommendation
            },
            "strategic_rationale": {
                "alignment": business_case.strategic_alignment,
                "market_opportunity": self._generate_market_opportunity_slide(business_case),
                "competitive_advantage": self._generate_competitive_advantage_slide(business_case)
            },
            "financial_overview": {
                "investment_breakdown": self._create_investment_chart_data(business_case.investments),
                "benefit_projection": self._create_benefit_chart_data(business_case.benefits),
                "cashflow_timeline": self._create_cashflow_chart_data(business_case.financial_projection),
                "roi_comparison": self._create_roi_comparison_data(business_case)
            },
            "implementation_plan": {
                "timeline": business_case.implementation_timeline,
                "key_milestones": self._generate_key_milestones(business_case),
                "resource_requirements": self._generate_resource_requirements(business_case)
            },
            "risk_management": {
                "key_risks": [
                    {
                        "risk": risk.risk,
                        "impact": risk.impact.name,
                        "probability": f"{risk.probability*100:.0f}%",
                        "mitigation": risk.mitigation_strategy
                    }
                    for risk in business_case.risks[:5]  # Top 5 risks
                ],
                "risk_mitigation_investment": sum(risk.mitigation_cost for risk in business_case.risks)
            },
            "success_metrics": {
                "kpis": business_case.success_metrics,
                "measurement_framework": self._generate_measurement_framework(business_case),
                "reporting_schedule": "Monthly progress reviews with quarterly executive updates"
            },
            "next_steps": {
                "immediate_actions": [
                    "Secure executive approval and budget allocation",
                    "Establish AI transformation steering committee",
                    "Begin vendor evaluation and selection process",
                    "Initiate stakeholder communication plan"
                ],
                "decision_timeline": "Decision required within 30 days to meet projected timeline"
            }
        }
        
        return presentation
    
    def _generate_investments(self, industry: str, size: str, budget: float) -> List[Investment]:
        """Generate investment breakdown based on industry and organization size"""
        
        template = self.investment_templates.get(industry, self.investment_templates["default"])
        size_multipliers = {"small": 0.6, "medium": 1.0, "large": 1.4, "enterprise": 2.0}
        multiplier = size_multipliers.get(size.lower(), 1.0)
        
        investments = []
        remaining_budget = budget
        
        for inv_type, allocation_pct in template.items():
            if remaining_budget <= 0:
                break
                
            allocation = budget * allocation_pct * multiplier
            
            # Distribute across years
            year_1 = allocation * 0.6  # Front-loaded
            year_2 = allocation * 0.3
            year_3 = allocation * 0.1
            ongoing = allocation * 0.05  # 5% ongoing
            
            investment = Investment(
                category=InvestmentType(inv_type),
                description=self._get_investment_description(InvestmentType(inv_type)),
                year_1_cost=year_1,
                year_2_cost=year_2,
                year_3_cost=year_3,
                ongoing_annual_cost=ongoing,
                confidence_level=0.85
            )
            
            investments.append(investment)
            remaining_budget -= allocation
        
        return investments
    
    def _generate_benefits(self, industry: str, size: str, objectives: List[str], investments: List[Investment]) -> List[Benefit]:
        """Generate benefit projections based on strategic objectives and investments"""
        
        total_investment = sum(inv.year_1_cost + inv.year_2_cost + inv.year_3_cost for inv in investments)
        benchmark = self.industry_benchmarks.get(industry, self.industry_benchmarks["default"])
        
        benefits = []
        
        # Revenue growth benefits
        if any("revenue" in obj.lower() or "growth" in obj.lower() for obj in objectives):
            revenue_benefit = Benefit(
                category=BenefitCategory.REVENUE_GROWTH,
                description="AI-driven revenue growth through enhanced products and services",
                year_1_value=total_investment * benchmark["revenue_multiplier"] * 0.3,
                year_2_value=total_investment * benchmark["revenue_multiplier"] * 0.7,
                year_3_value=total_investment * benchmark["revenue_multiplier"] * 1.0,
                ongoing_annual_value=total_investment * benchmark["revenue_multiplier"] * 0.8,
                confidence_level=0.70,
                realization_probability=0.75
            )
            benefits.append(revenue_benefit)
        
        # Cost reduction benefits
        if any("cost" in obj.lower() or "efficiency" in obj.lower() for obj in objectives):
            cost_benefit = Benefit(
                category=BenefitCategory.COST_REDUCTION,
                description="Operational cost reduction through AI automation",
                year_1_value=total_investment * benchmark["cost_reduction_multiplier"] * 0.2,
                year_2_value=total_investment * benchmark["cost_reduction_multiplier"] * 0.5,
                year_3_value=total_investment * benchmark["cost_reduction_multiplier"] * 0.8,
                ongoing_annual_value=total_investment * benchmark["cost_reduction_multiplier"] * 0.9,
                confidence_level=0.80,
                realization_probability=0.85
            )
            benefits.append(cost_benefit)
        
        # Productivity improvements
        productivity_benefit = Benefit(
            category=BenefitCategory.PRODUCTIVITY_IMPROVEMENT,
            description="Employee productivity enhancement through AI tools",
            year_1_value=total_investment * benchmark["productivity_multiplier"] * 0.4,
            year_2_value=total_investment * benchmark["productivity_multiplier"] * 0.8,
            year_3_value=total_investment * benchmark["productivity_multiplier"] * 1.2,
            ongoing_annual_value=total_investment * benchmark["productivity_multiplier"] * 1.0,
            confidence_level=0.75,
            realization_probability=0.80
        )
        benefits.append(productivity_benefit)
        
        # Customer experience benefits
        if any("customer" in obj.lower() for obj in objectives):
            cx_benefit = Benefit(
                category=BenefitCategory.CUSTOMER_EXPERIENCE,
                description="Enhanced customer experience and satisfaction",
                year_1_value=total_investment * benchmark["customer_multiplier"] * 0.3,
                year_2_value=total_investment * benchmark["customer_multiplier"] * 0.6,
                year_3_value=total_investment * benchmark["customer_multiplier"] * 0.9,
                ongoing_annual_value=total_investment * benchmark["customer_multiplier"] * 0.8,
                confidence_level=0.65,
                realization_probability=0.70
            )
            benefits.append(cx_benefit)
        
        return benefits
    
    def _assess_risks(self, industry: str, size: str, challenges: List[str]) -> List[RiskFactor]:
        """Assess and prioritize transformation risks"""
        
        risks = []
        
        # Common risks from library
        common_risks = self.risk_library["common"]
        for risk_data in common_risks:
            risk = RiskFactor(
                risk=risk_data["risk"],
                impact=RiskLevel(risk_data["impact"]),
                probability=risk_data["probability"],
                mitigation_strategy=risk_data["mitigation"],
                mitigation_cost=risk_data["cost"]
            )
            risks.append(risk)
        
        # Industry-specific risks
        industry_risks = self.risk_library.get(industry, [])
        for risk_data in industry_risks:
            risk = RiskFactor(
                risk=risk_data["risk"],
                impact=RiskLevel(risk_data["impact"]),
                probability=risk_data["probability"],
                mitigation_strategy=risk_data["mitigation"],
                mitigation_cost=risk_data["cost"]
            )
            risks.append(risk)
        
        # Challenge-specific risks
        if any("data" in challenge.lower() for challenge in challenges):
            risks.append(RiskFactor(
                risk="Data quality issues impacting AI model performance",
                impact=RiskLevel.HIGH,
                probability=0.6,
                mitigation_strategy="Implement comprehensive data quality framework",
                mitigation_cost=50000
            ))
        
        if any("skill" in challenge.lower() or "talent" in challenge.lower() for challenge in challenges):
            risks.append(RiskFactor(
                risk="Insufficient AI talent and skills",
                impact=RiskLevel.HIGH,
                probability=0.7,
                mitigation_strategy="Aggressive hiring and training program",
                mitigation_cost=100000
            ))
        
        # Sort by risk score (impact * probability)
        risks.sort(key=lambda r: r.impact.value * r.probability, reverse=True)
        
        return risks[:10]  # Return top 10 risks
    
    def _calculate_financial_projection(self, investments: List[Investment], benefits: List[Benefit]) -> FinancialProjection:
        """Calculate comprehensive financial projections"""
        
        # Calculate total costs and benefits by year
        years = 5  # 5-year projection
        annual_costs = [0.0] * years
        annual_benefits = [0.0] * years
        
        # Investment costs
        for inv in investments:
            annual_costs[0] += inv.year_1_cost
            annual_costs[1] += inv.year_2_cost
            annual_costs[2] += inv.year_3_cost
            for year in range(3, years):
                annual_costs[year] += inv.ongoing_annual_cost
        
        # Benefit values
        for ben in benefits:
            expected_benefits = [
                ben.year_1_value * ben.confidence_level * ben.realization_probability,
                ben.year_2_value * ben.confidence_level * ben.realization_probability,
                ben.year_3_value * ben.confidence_level * ben.realization_probability
            ]
            
            annual_benefits[0] += expected_benefits[0]
            annual_benefits[1] += expected_benefits[1]
            annual_benefits[2] += expected_benefits[2]
            for year in range(3, years):
                annual_benefits[year] += ben.ongoing_annual_value * ben.confidence_level * ben.realization_probability
        
        # Calculate cash flows
        cashflow = [annual_benefits[i] - annual_costs[i] for i in range(years)]
        
        # Calculate NPV
        npv = sum(cf / ((1 + self.discount_rate) ** (i + 1)) for i, cf in enumerate(cashflow))
        
        # Calculate total investment and benefits
        total_investment = sum(annual_costs)
        total_benefits = sum(annual_benefits)
        
        # Calculate ROI
        roi_percentage = ((total_benefits - total_investment) / total_investment) * 100 if total_investment > 0 else 0
        
        # Calculate payback period
        cumulative_cf = 0
        payback_months = 0
        for year, cf in enumerate(cashflow):
            cumulative_cf += cf
            if cumulative_cf >= 0:
                payback_months = (year + 1) * 12
                break
        else:
            payback_months = years * 12  # Max projection period
        
        # Calculate IRR (simplified approximation)
        irr = self._calculate_irr(cashflow, total_investment)
        
        return FinancialProjection(
            total_investment=total_investment,
            total_benefits=total_benefits,
            net_present_value=npv,
            roi_percentage=roi_percentage,
            payback_period_months=payback_months,
            irr=irr,
            yearly_cashflow=cashflow
        )
    
    def _generate_scenarios(self, industry: str, risks: List[RiskFactor]) -> List[Scenario]:
        """Generate scenario analysis for business case"""
        
        scenarios = [
            Scenario(
                name="Base Case",
                probability=0.60,
                roi_adjustment=0.0,
                timeline_adjustment=0,
                description="Expected outcomes based on current planning assumptions"
            ),
            Scenario(
                name="Optimistic Case",
                probability=0.20,
                roi_adjustment=0.25,
                timeline_adjustment=-3,
                description="Accelerated adoption with higher than expected benefits"
            ),
            Scenario(
                name="Conservative Case",
                probability=0.15,
                roi_adjustment=-0.20,
                timeline_adjustment=6,
                description="Slower adoption with implementation challenges"
            ),
            Scenario(
                name="Risk Materialization",
                probability=0.05,
                roi_adjustment=-0.40,
                timeline_adjustment=12,
                description="Multiple high-impact risks materialize simultaneously"
            )
        ]
        
        return scenarios
    
    def _generate_implementation_timeline(self, investments: List[Investment], size: str) -> Dict[str, int]:
        """Generate implementation timeline by phase"""
        
        size_multipliers = {"small": 0.8, "medium": 1.0, "large": 1.2, "enterprise": 1.5}
        multiplier = size_multipliers.get(size.lower(), 1.0)
        
        base_timeline = {
            "planning_and_setup": 2,
            "infrastructure_deployment": 4,
            "pilot_implementation": 3,
            "training_and_adoption": 3,
            "scaling_and_optimization": 6,
            "full_deployment": 4
        }
        
        return {phase: int(months * multiplier) for phase, months in base_timeline.items()}
    
    def _define_success_metrics(self, benefits: List[Benefit], objectives: List[str]) -> Dict[str, float]:
        """Define measurable success metrics"""
        
        metrics = {}
        
        for benefit in benefits:
            if benefit.category == BenefitCategory.REVENUE_GROWTH:
                metrics["Revenue Growth %"] = 15.0
            elif benefit.category == BenefitCategory.COST_REDUCTION:
                metrics["Cost Reduction %"] = 20.0
            elif benefit.category == BenefitCategory.PRODUCTIVITY_IMPROVEMENT:
                metrics["Productivity Improvement %"] = 25.0
            elif benefit.category == BenefitCategory.CUSTOMER_EXPERIENCE:
                metrics["Customer Satisfaction Score"] = 4.5
        
        # Add objective-specific metrics
        if any("time" in obj.lower() for obj in objectives):
            metrics["Process Time Reduction %"] = 30.0
        
        if any("quality" in obj.lower() for obj in objectives):
            metrics["Quality Score Improvement %"] = 20.0
        
        # Standard transformation metrics
        metrics["Employee Adoption Rate %"] = 85.0
        metrics["Project Milestone Achievement %"] = 90.0
        metrics["ROI Achievement %"] = 100.0
        
        return metrics
    
    def _calculate_confidence_score(self, investments: List[Investment], benefits: List[Benefit], risks: List[RiskFactor]) -> float:
        """Calculate overall confidence score for the business case"""
        
        # Investment confidence (weighted by cost)
        total_inv_cost = sum(inv.year_1_cost + inv.year_2_cost + inv.year_3_cost for inv in investments)
        inv_confidence = sum(
            (inv.year_1_cost + inv.year_2_cost + inv.year_3_cost) * inv.confidence_level 
            for inv in investments
        ) / total_inv_cost if total_inv_cost > 0 else 0.8
        
        # Benefit confidence (weighted by value)
        total_ben_value = sum(ben.year_1_value + ben.year_2_value + ben.year_3_value for ben in benefits)
        ben_confidence = sum(
            (ben.year_1_value + ben.year_2_value + ben.year_3_value) * ben.confidence_level * ben.realization_probability
            for ben in benefits
        ) / total_ben_value if total_ben_value > 0 else 0.7
        
        # Risk adjustment
        high_risk_count = sum(1 for risk in risks if risk.impact.value >= 3 and risk.probability > 0.5)
        risk_adjustment = max(0.0, 1.0 - (high_risk_count * 0.1))
        
        # Overall confidence
        confidence = (inv_confidence * 0.3 + ben_confidence * 0.5 + risk_adjustment * 0.2)
        
        return min(1.0, max(0.0, confidence))
    
    # Helper methods for data structures and calculations...
    
    def _initialize_investment_templates(self) -> Dict[str, Dict[str, float]]:
        """Initialize investment allocation templates by industry"""
        return {
            "default": {
                "infrastructure": 0.30,
                "technology": 0.25,
                "talent": 0.20,
                "training": 0.15,
                "consulting": 0.10
            },
            "financial_services": {
                "technology": 0.35,
                "infrastructure": 0.25,
                "talent": 0.20,
                "consulting": 0.15,
                "training": 0.05
            },
            "manufacturing": {
                "infrastructure": 0.40,
                "technology": 0.30,
                "talent": 0.15,
                "training": 0.10,
                "consulting": 0.05
            }
        }
    
    def _initialize_benefit_models(self) -> Dict[str, Dict[str, float]]:
        """Initialize benefit multiplier models"""
        return {
            "revenue_models": {
                "customer_experience": {"conversion_lift": 0.15, "retention_improvement": 0.12},
                "personalization": {"cross_sell_lift": 0.25, "pricing_optimization": 0.08},
                "product_innovation": {"time_to_market": 0.30, "feature_premium": 0.10},
                "market_expansion": {"new_segments": 0.20, "geographic_expansion": 0.15}
            },
            "cost_models": {
                "process_automation": {"admin_tasks": 0.60, "customer_service": 0.45},
                "operational_efficiency": {"supply_chain": 0.18, "energy_optimization": 0.22},
                "quality_improvement": {"defect_reduction": 0.35, "rework_elimination": 0.40},
                "resource_optimization": {"capacity_utilization": 0.25, "inventory_reduction": 0.20}
            },
            "productivity_models": {
                "decision_acceleration": {"management_decisions": 0.40, "operational_decisions": 0.55},
                "knowledge_work": {"analytical_tasks": 0.35, "research_tasks": 0.50},
                "collaboration": {"meeting_efficiency": 0.25, "information_sharing": 0.30},
                "innovation": {"idea_generation": 0.45, "prototype_testing": 0.35}
            }
        }
    
    def _initialize_risk_library(self) -> Dict[str, List[Dict]]:
        """Initialize comprehensive risk library"""
        return {
            "common": [
                {
                    "risk": "Project timeline delays",
                    "impact": 2,
                    "probability": 0.4,
                    "mitigation": "Agile implementation with regular checkpoints",
                    "cost": 25000
                },
                {
                    "risk": "Budget overruns",
                    "impact": 3,
                    "probability": 0.3,
                    "mitigation": "Detailed cost tracking and contingency planning",
                    "cost": 15000
                }
            ],
            "financial_services": [
                {
                    "risk": "Regulatory compliance issues",
                    "impact": 4,
                    "probability": 0.5,
                    "mitigation": "Early regulatory engagement and compliance review",
                    "cost": 75000
                }
            ]
        }
    
    def _load_industry_benchmarks(self) -> Dict[str, Dict[str, float]]:
        """Load industry-specific ROI and benefit benchmarks"""
        return {
            "default": {
                "revenue_multiplier": 0.15,
                "cost_reduction_multiplier": 0.20,
                "productivity_multiplier": 0.25,
                "customer_multiplier": 0.10
            },
            "financial_services": {
                "revenue_multiplier": 0.12,
                "cost_reduction_multiplier": 0.25,
                "productivity_multiplier": 0.30,
                "customer_multiplier": 0.15
            },
            "manufacturing": {
                "revenue_multiplier": 0.18,
                "cost_reduction_multiplier": 0.30,
                "productivity_multiplier": 0.35,
                "customer_multiplier": 0.08
            }
        }
    
    def _calculate_irr(self, cashflows: List[float], initial_investment: float) -> float:
        """Calculate Internal Rate of Return (simplified)"""
        # Simplified IRR calculation
        if initial_investment <= 0:
            return 0.0
        
        total_return = sum(cashflows)
        years = len(cashflows)
        
        if total_return <= 0:
            return -1.0
        
        # Approximation: (Total Return / Initial Investment) ^ (1/years) - 1
        irr = (total_return / initial_investment) ** (1/years) - 1
        return min(1.0, max(-1.0, irr))
    
    # Additional helper methods...
    def _get_investment_description(self, inv_type: InvestmentType) -> str:
        descriptions = {
            InvestmentType.INFRASTRUCTURE: "AI-ready infrastructure and cloud platforms",
            InvestmentType.TALENT: "AI talent acquisition and retention",
            InvestmentType.TECHNOLOGY: "AI software licenses and tools",
            InvestmentType.TRAINING: "Employee training and upskilling programs",
            InvestmentType.CONSULTING: "External consulting and implementation support"
        }
        return descriptions.get(inv_type, "AI transformation investment")
    
    def _adjust_investment(self, investment: Investment, factor: float) -> Investment:
        """Adjust investment costs by a factor"""
        return Investment(
            category=investment.category,
            description=investment.description,
            year_1_cost=investment.year_1_cost * factor,
            year_2_cost=investment.year_2_cost * factor,
            year_3_cost=investment.year_3_cost * factor,
            ongoing_annual_cost=investment.ongoing_annual_cost * factor,
            confidence_level=investment.confidence_level
        )
    
    def _adjust_benefit(self, benefit: Benefit, factor: float) -> Benefit:
        """Adjust benefit values by a factor"""
        return Benefit(
            category=benefit.category,
            description=benefit.description,
            year_1_value=benefit.year_1_value * factor,
            year_2_value=benefit.year_2_value * factor,
            year_3_value=benefit.year_3_value * factor,
            ongoing_annual_value=benefit.ongoing_annual_value * factor,
            confidence_level=benefit.confidence_level,
            realization_probability=benefit.realization_probability
        )
    
    def _delay_benefit(self, benefit: Benefit, delay_months: int) -> Benefit:
        """Delay benefit realization by specified months"""
        if delay_months <= 6:
            # Shift Year 1 to Year 2
            return Benefit(
                category=benefit.category,
                description=benefit.description,
                year_1_value=benefit.year_1_value * 0.5,
                year_2_value=benefit.year_2_value + benefit.year_1_value * 0.5,
                year_3_value=benefit.year_3_value,
                ongoing_annual_value=benefit.ongoing_annual_value,
                confidence_level=benefit.confidence_level,
                realization_probability=benefit.realization_probability
            )
        else:
            # More significant delay
            return Benefit(
                category=benefit.category,
                description=benefit.description,
                year_1_value=0,
                year_2_value=benefit.year_1_value * 0.7,
                year_3_value=benefit.year_2_value + benefit.year_1_value * 0.3,
                ongoing_annual_value=benefit.ongoing_annual_value,
                confidence_level=benefit.confidence_level * 0.9,
                realization_probability=benefit.realization_probability * 0.9
            )
    
    def _generate_executive_summary(self, projection: FinancialProjection, objectives: List[str], timeline: Dict[str, int]) -> str:
        """Generate executive summary text"""
        total_timeline = sum(timeline.values())
        
        return f"""
This AI transformation initiative presents a compelling investment opportunity with projected ROI of {projection.roi_percentage:.1f}% 
and payback period of {projection.payback_period_months} months. The initiative directly supports {len(objectives)} strategic 
objectives and is expected to generate ${projection.total_benefits:,.0f} in total benefits against an investment of 
${projection.total_investment:,.0f} over the {total_timeline}-month implementation timeline.

Key value drivers include operational efficiency gains, revenue growth through enhanced capabilities, and competitive 
differentiation in the marketplace. The financial projections are based on industry benchmarks and incorporate realistic 
risk assessments to ensure achievable outcomes.
"""
    
    def _generate_strategic_alignment(self, objectives: List[str]) -> str:
        """Generate strategic alignment statement"""
        return f"""
This AI transformation initiative directly aligns with {len(objectives)} key strategic objectives: {', '.join(objectives[:3])}
{'and others' if len(objectives) > 3 else ''}. The initiative will enhance organizational capabilities, drive operational 
excellence, and position the company as an AI-enabled leader in the industry.
"""
    
    def _generate_approval_recommendation(self, projection: FinancialProjection, risks: List[RiskFactor]) -> str:
        """Generate approval recommendation"""
        if projection.roi_percentage > 30 and projection.payback_period_months <= 24:
            recommendation = "STRONGLY RECOMMEND APPROVAL"
        elif projection.roi_percentage > 15 and projection.payback_period_months <= 36:
            recommendation = "RECOMMEND APPROVAL"
        else:
            recommendation = "CONDITIONAL APPROVAL WITH RISK MITIGATION"
        
        high_risks = [r for r in risks if r.impact.value >= 3 and r.probability > 0.5]
        risk_note = f" Key risks identified: {len(high_risks)} high-impact risks require mitigation." if high_risks else ""
        
        return f"{recommendation}.{risk_note}"
    
    def _generate_market_opportunity_slide(self, business_case: BusinessCase) -> str:
        """Generate market opportunity analysis content"""
        industry = business_case.organization_name.split()[-1] if business_case.organization_name else "industry"
        roi = business_case.financial_projection.roi_percentage
        
        return f"""
        **AI Market Opportunity Analysis**
        
        • Global AI market growing at 35% CAGR, reaching $190B by 2025
        • {industry.title()} sector AI adoption accelerating with 60% of leaders investing
        • Early adopters achieving 2-3x higher performance improvements
        • Competitive window closing - first-mover advantage critical
        • Expected ROI of {roi:.1f}% positions us in top quartile of implementations
        
        **Strategic Positioning**
        • Transform from AI experimenter to AI-powered market leader
        • Capture {business_case.financial_projection.total_benefits/1000000:.1f}M in value creation over 3 years
        • Build sustainable competitive moats through AI capabilities
        """
    
    def _generate_competitive_advantage_slide(self, business_case: BusinessCase) -> str:
        """Generate competitive advantage analysis content"""
        benefits = [b.category.value.replace('_', ' ').title() for b in business_case.benefits[:3]]
        
        return f"""
        **Competitive Advantage Through AI**
        
        **Unique Value Creation:**
        • {', '.join(benefits)} driving differentiation
        • Data-driven decision making at enterprise scale
        • Automated insights and predictive capabilities
        • Enhanced customer experience and personalization
        
        **Market Positioning:**
        • Move from reactive to predictive business model
        • Scale expertise and insights across organization
        • Create network effects and platform advantages
        • Build barriers to entry through AI sophistication
        
        **Competitive Timeline:**
        • {business_case.financial_projection.payback_period_months}-month payback faster than industry average
        • Sustainable advantage through continuous learning and improvement
        """
    
    def _create_investment_chart_data(self, investments: List[Investment]) -> Dict:
        """Create investment breakdown chart data"""
        investment_data = {}
        for inv in investments:
            total_cost = inv.year_1_cost + inv.year_2_cost + inv.year_3_cost
            investment_data[inv.category.value.replace('_', ' ').title()] = total_cost
        
        return {
            "chart_type": "pie",
            "title": "Investment Allocation by Category",
            "data": investment_data,
            "total": sum(investment_data.values())
        }
    
    def _create_benefit_chart_data(self, benefits: List[Benefit]) -> Dict:
        """Create benefit projection chart data"""
        benefit_data = {
            "categories": [],
            "year_1": [],
            "year_2": [],
            "year_3": []
        }
        
        for benefit in benefits:
            benefit_data["categories"].append(benefit.category.value.replace('_', ' ').title())
            benefit_data["year_1"].append(benefit.year_1_value)
            benefit_data["year_2"].append(benefit.year_2_value)
            benefit_data["year_3"].append(benefit.year_3_value)
        
        return {
            "chart_type": "stacked_bar",
            "title": "Projected Benefits by Category and Year",
            "data": benefit_data
        }
    
    def _create_cashflow_chart_data(self, projection: FinancialProjection) -> Dict:
        """Create cashflow timeline chart data"""
        return {
            "chart_type": "line",
            "title": "Projected Cash Flow Over Time",
            "data": {
                "years": [f"Year {i+1}" for i in range(len(projection.yearly_cashflow))],
                "cashflow": projection.yearly_cashflow,
                "cumulative": [sum(projection.yearly_cashflow[:i+1]) for i in range(len(projection.yearly_cashflow))]
            }
        }
    
    def _create_roi_comparison_data(self, business_case: BusinessCase) -> Dict:
        """Create ROI comparison chart data"""
        industry_benchmarks = {
            "financial_services": 28.0,
            "manufacturing": 35.0,
            "retail": 25.0,
            "healthcare": 22.0,
            "default": 25.0
        }
        
        # Determine industry from organization or use default
        industry_avg = industry_benchmarks.get("default", 25.0)
        
        return {
            "chart_type": "comparison_bar",
            "title": "ROI Comparison vs Industry Average",
            "data": {
                "categories": ["Industry Average", "Projected ROI", "Conservative Case", "Optimistic Case"],
                "values": [
                    industry_avg,
                    business_case.financial_projection.roi_percentage,
                    business_case.financial_projection.roi_percentage * 0.7,
                    business_case.financial_projection.roi_percentage * 1.3
                ]
            }
        }
    
    def _generate_key_milestones(self, business_case: BusinessCase) -> List[str]:
        """Generate key implementation milestones"""
        timeline = business_case.implementation_timeline
        total_months = sum(timeline.values())
        
        milestones = [
            f"Month {timeline.get('planning_and_setup', 2)}: Foundation and governance established",
            f"Month {timeline.get('planning_and_setup', 2) + timeline.get('infrastructure_deployment', 4)}: Infrastructure deployment complete",
            f"Month {sum(list(timeline.values())[:3])}: First pilot projects successful",
            f"Month {sum(list(timeline.values())[:4])}: Training programs completed",
            f"Month {sum(list(timeline.values())[:5])}: Enterprise scaling achieved",
            f"Month {total_months}: Full deployment and optimization complete"
        ]
        
        return milestones
    
    def _generate_resource_requirements(self, business_case: BusinessCase) -> Dict:
        """Generate detailed resource requirements"""
        total_investment = business_case.financial_projection.total_investment
        
        return {
            "budget": {
                "total_investment": total_investment,
                "year_1": total_investment * 0.6,
                "year_2": total_investment * 0.3,
                "year_3": total_investment * 0.1
            },
            "personnel": {
                "core_team": 8,
                "extended_team": 15,
                "executive_sponsors": 3,
                "change_agents": 12
            },
            "timeline": {
                "total_months": sum(business_case.implementation_timeline.values()),
                "critical_path": list(business_case.implementation_timeline.keys())[:3]
            },
            "infrastructure": {
                "cloud_platforms": "AWS/Azure/GCP",
                "ai_tools": "MLOps, Data platforms, Analytics tools",
                "integration": "APIs, Data pipelines, Security frameworks"
            }
        }
    
    def _generate_measurement_framework(self, business_case: BusinessCase) -> str:
        """Generate measurement and governance framework"""
        return f"""
        **Performance Measurement Framework**
        
        **Financial Tracking:**
        • Monthly ROI progress vs. {business_case.financial_projection.roi_percentage:.1f}% target
        • Quarterly NPV realization vs. ${business_case.financial_projection.net_present_value/1000000:.1f}M projection
        • Benefit realization tracking by category and timeline
        
        **Operational Metrics:**
        • User adoption rates and feature utilization
        • Process efficiency improvements and time savings
        • Quality metrics and error reduction measurements
        • Customer satisfaction and experience improvements
        
        **Governance Structure:**
        • Weekly project team progress reviews
        • Monthly steering committee updates
        • Quarterly executive business reviews
        • Annual strategic assessment and roadmap updates
        
        **Risk Monitoring:**
        • Monthly risk register reviews and mitigation tracking
        • Quarterly scenario analysis and contingency planning
        • Continuous stakeholder engagement and communication
        """


def main():
    """Example usage of the Business Case Generator"""
    generator = BusinessCaseGenerator()
    
    # Example organization parameters
    business_case = generator.generate_business_case(
        organization_name="TechCorp Industries",
        initiative_name="Enterprise AI Transformation",
        industry="manufacturing",
        organization_size="large",
        investment_budget=2000000,
        strategic_objectives=[
            "Increase operational efficiency by 25%",
            "Reduce production costs by 15%",
            "Improve customer satisfaction",
            "Accelerate product innovation"
        ],
        current_challenges=[
            "Legacy system integration",
            "Limited data science talent",
            "Inconsistent data quality"
        ]
    )
    
    print(f"Business Case Generated for {business_case.organization_name}")
    print(f"Expected ROI: {business_case.financial_projection.roi_percentage:.1f}%")
    print(f"Payback Period: {business_case.financial_projection.payback_period_months} months")
    print(f"Confidence Score: {business_case.confidence_score:.1f}")
    print(f"Recommendation: {business_case.approval_recommendation}")
    
    # Perform sensitivity analysis
    sensitivity = generator.perform_sensitivity_analysis(business_case)
    print(f"\nSensitivity Analysis:")
    print(f"Optimistic NPV: ${sensitivity['optimistic_case']['npv']:,.0f}")
    print(f"Pessimistic NPV: ${sensitivity['pessimistic_case']['npv']:,.0f}")
    
    # Generate presentation
    presentation = generator.generate_executive_presentation(business_case)
    print(f"\nExecutive presentation generated with {len(presentation)} sections")


if __name__ == "__main__":
    main()