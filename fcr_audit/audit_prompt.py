"""
FCR Audit Prompt Template
Contains the structured prompt for Fundamental Credit Review audit analysis.
"""


class AuditPrompt:
    """FCR Audit prompt template and question definitions."""
    
    # Credit Policy Manual - Article 5: Credit Underwriting
    CREDIT_POLICY_MANUAL = """# ARTICLE 5: CREDIT UNDERWRITING

5.1 In order to comprehensively address the Risk Profiles of its portfolios, each LFI must operate with a sound and granular credit underwriting policy based on its Lending strategy in accordance with its Board approved Risk Appetite. The Risk Appetite and the credit underwriting policy must incorporate sufficient risk-return discipline, consistent with the LFI's business model.

5.2 The underwriting process must ensure a thorough understanding of the Risk Profile and characteristics of the Obligors and the drivers of their credit performance. For that purpose, the LFI must establish well defined criteria within its policies and processes for approving new Facilities, renewing and refinancing existing Facilities. This decision process must be supported by a clearly defined approval authority based on the size and complexity of the Facilities.

5.3 Materiality thresholds must be established to govern decisions surrounding the issuance of each Credit Facility. All financing to existing and new Obligors must be assessed against risk acceptance criteria during the initial credit evaluation process and during the continuous Obligor/portfolio monitoring phase, as per Article 3.12.

5.4 LFIs must ensure that the underwriting framework and respective criteria, policies and procedures are implemented effectively and are subject to regular audit reviews.

## Decision-making process

The decision-making process must include the following key elements:

5.5 **Credit Committee:** Decisions to issue Credit Facilities are expected to be governed by a management credit committee or individual(s) with the appropriate sanctioning authority where appropriate. The credit committee is expected to be a forum to analyse and discuss in detail the risk drivers, the pricing and the structure of Credit Facilities or, pools of Credit Facilities. Robust documented evidence must be retained to demonstrate that underwriting decisions are sufficiently challenged. Underwriting decisions must clearly document an appropriate balance between risk and commercial considerations.

5.6 Depending on their materiality, their rating and other criteria, some Facilities may be delegated for approval at levels of authority that report to the CCO and are below that of the credit committee. However, those delegations must be clearly documented and approved.

5.7 As an alternative to a credit committee, LFIs may structure underwriting approvals through individual delegations, however they must have in place a clearly documented and approved delegation matrix setting out delegations from Board level down to Senior Management (excluding control functions), CCO and individual credit officers.

5.8 LFIs must ensure that the approval of Credit Facilities is achieved through a continuous accountability framework for each step of the underwriting process. LFIs must define the roles of executive committees and senior executives involved in the process of underwriting of Credit Facilities.

The following principles apply:

a. The Board and/or Senior Management must be directly involved in the approval of Credit Facilities with the following characteristics: (i) materially large Facilities relative to the LFI's capital and (ii) Facilities with a high Risk Profile as explicitly defined in the policy.

b. The authority to approve Credit Facilities must flow through a mandate from the Board of directors or a designated body in the Board. The delegation must be vested with the highest executive committee/individual in the LFI that oversees the underwriting of Credit Facilities.

c. The delegation process must consider, at a minimum, the Obligor risk captured by Obligor rating, Facility amount and structure, the experience and qualifications of staff, the business segment of the Credit Facility to be approved, and the ranking of the financial obligation.

d. The staff delegated to make credit decisions have the adequate level of experience, qualifications and abilities.

e. The individuals responsible for underwriting must remain accountable for their decisions and should be subject to performance indicators reflecting the quality of their underwriting decisions.

5.9 LFIs must establish a performance assessment mechanism for all stakeholders involved in the acquisition and the management of Credit Risk which is aligned with the long term sustainability of the LFI. The mechanism must be articulated differently for the business lines and the control functions, based on the following principles:

a. The mechanism must enforce accountability amongst employees who make decisions that commit the LFI over several years and/or that result in material risk taking activities.

b. All internal employees involved in the acquisition and the management of Credit Risk including employees from the business lines must be subject to key performance indicators reflecting the quality of their underwriting decisions i.e. demonstrated by the credit worthiness of the Obligors after the underwriting process.

c. Each LFI should put in place deferred compensation mechanisms that align with the risk outcomes for the employees who benefit from the completion of large transactions that expose LFIs to long term risks.

d. Staff in the control functions involved in Credit Risk management must be compensated in a way that makes their incentives independent of the performance of the business. Their performance incentives must be based on achievements assessed against the objectives of the control functions, so as not to compromise their independence.

5.10 **Independence:** All credit decisions must be made free of conflicts of interest and on an arm's length basis. In particular, Related Party transactions must be governed by internal policies, to prevent potential conflicts of interests. They must be authorised by the Board of the LFI, and regularly monitored. The policies and processes must be articulated so as to prevent persons benefiting from the transaction and/or persons related to such a person from being part of the process of granting and managing the transaction. All Credit Facilities to Related Parties must be formally approved and signed-off by each Board member.

## Key components of underwriting

5.11 The underwriting process must be structured to adequately support the decision-making process for the issuance and the acquisition of Credit Facilities, consistent with the LFI's Risk Appetite and strategic objectives. The underwriting process must enable the LFI to form a view on the suitability of the Risk Profile of each Credit Facility in light of the associated risk-adjusted return objective of the LFI. Consequently, this process must be clear and comprehensive, fully documented, and enforced in accordance with its internal policy.

5.12 In addition, the underwriting process is expected to include the following at a minimum:

a. **Limits:** The underwriting process must be controlled adequately with Risk Limits established at a suitable level of granularity. LFIs must establish overall credit limits at the level of individual Obligors and counterparties, and groups of connected counterparties that aggregate different types of Credit Facilities in a comparable and meaningful manner. The limits must be structured around the drivers of Credit Risk, including but not limited to Obligor rating, industry type, product type, geography, Credit Facility tenor and Credit Facility structure. LFIs must define acceptable terms in accordance with the limits, (for example: Credit Facility covenants, legal requirements, leverage, tenor, amortization, pricing and/or minimum security).

b. **Due diligence:** LFIs must ensure that they implement a robust and comprehensive credit due diligence process (including legal aspects as appropriate) in order to fully capture all the relevant information necessary to assess the Obligors' credit worthiness. They must demonstrate a robust documented understanding of the purpose of the Credit Facility and the associated risk measured by key financial parameters such as leverage, debt service coverage ratio, liquidity, net worth and operating cash flows. This process must include quantitative and qualitative information over a period of time suitable to make informed credit decisions. It must also cover the assessment of the ownership structure of the Obligor and related group and the identification of the ultimate beneficial owner. Finally, LFIs must define a set of criteria triggering an enhanced due-diligence process with a larger and deeper scope of investigation.

c. **Risk drivers:** The underwriting process must incorporate a comprehensive identification and analysis of the key drivers of Credit Risk, typically separated into systemic risks and specific risk (or 'idiosyncratic' risk). Systemic risks should include Country Risk and industry risk. Specific risk should include business risk, financial risk and management risk.

d. **Financial information:** LFIs must collect comprehensive financial information and cash flow projections from their Obligors, contingent Obligors and guarantors. They must ensure that the due diligence process captures all financial obligations of their Obligors (including other LFIs and Related Parties). LFIs must refrain from making underwriting decisions mostly based on subjective information.

In addition, for Wholesale Obligors:

i. Credit analysis must be forward-looking incorporating macro-economic forecasts considering business cycle effects, the sector in which the Obligor operates, the Obligor's relative position and expertise within that sector and associated downside scenarios.

ii. Affordability analysis throughout the Credit Facility should include a sensitivity analysis based on stressed market benchmark rates and profitability.

iii. For Credit Facilities that are not fully amortising, an assessment of the LFI's exposure to re-finance risk, including possible exit options for the LFI, should be undertaken.

iv. The LFI should have a formal documented process to ensure that the financial analysis of an Obligor is based on financial statements that have been audited by reputable auditing firms.

5.13 **Documentation:** The credit files must be well documented and include all information necessary to ascertain the current financial condition of the Obligor, including but not limited to the rationale and computations upon which classification and provisioning has been determined. In addition, files must contain sufficient information to track the decisions made and the history of the credit. For example, the credit files should include current financial statements, financial analyses and internal rating documentation, internal memoranda, reference letters, appraisals and forward-looking financial projections. The credit review function must determine that the credit files are complete and that all Credit Facility approvals and other necessary documents have been obtained. Documents must include the evidence of the perfection of the LFI's legal interest as well as evidence of the ability to collect / exercise their creditor interest in collateral taken in support of the Credit Facility.

5.14 **Collateral:** LFIs must ensure that the collateral used as risk mitigant in the underwriting process is appropriately identified and valued. In addition, LFIs must monitor, control and assess the implications of multiple Lending against the same collateral. For that purpose, the following actions must be undertaken, at a minimum:

a. When appropriate, LFIs must ensure that collateral used as mitigation are registered with the relevant official body: (i) the land department for real estate collateral and (ii) the Emirates Integrated Registries Company LLC for other collateral.

b. The types of collateral covered in the registers are likely to evolve through time. Therefore LFIs must verify all collateral types.

c. Prior to the disbursement of any secured Lending, LFIs must verify the registration of collateral and ensure that the priority of their claim is reflected in underwriting and provisioning.

5.15 **Facility structure:** LFIs must ensure that amortization schedules and Facility tenors are suitably designed to meet the needs of Obligors and their Repayment abilities. The amortization structure should include the following principles:

a. The depth and breadth of credit analysis should increase with the Facility tenor, i.e. additional justifications and business rationale should be provided to support Facilities with long tenors.

b. The Repayment schedule should match the business cyclicality.

c. Tenors and amortization profiles should be within acceptable Risk Appetite and risk-reward relationship.

d. In the case of project finance, the Repayment schedule should match the expected development schedule of the project.

5.16 **Legal due diligence:** The LFI must ensure that the legal documentation of the Credit Facility is adequate to support the right of the LFI over the recoverability of the debt, including but not limited to, the liquidation of collateral, enforceability of guarantees, access of overseas assets. In addition, the LFI should review and evaluate the right to use Credit Facilities as collateral to raise liquidity, and ensure the conclusions of such evaluation are reflected in the legal documentation."""
    
    # Pillar definitions with weights
    PILLARS = {
        "Pillar 1: Bank Guidelines": 0.30,
        "Pillar 2: Proposal Quality": 0.35,
        "Pillar 3: Financial Analysis": 0.20,
        "Pillar 4: Rating Veracity": 0.10,
        "Pillar 5: Early Warning & Collateral": 0.05,
    }
    
    # 16 Questions mapped to pillars
    QUESTIONS = [
        {
            "number": 1,
            "text": "Growth in line with guidelines",
            "pillar": "Pillar 1: Bank Guidelines"
        },
        {
            "number": 2,
            "text": "Obligor diversification strategy, excessive concentration / industry sub-sector / pattern of business & coherence of business strategy rationale",
            "pillar": "Pillar 1: Bank Guidelines"
        },
        {
            "number": 3,
            "text": "Is the risk rating expected to be downgraded due to emerging risks?",
            "pillar": "Pillar 1: Bank Guidelines"
        },
        {
            "number": 4,
            "text": "Are trends in facility utilization indicative of increasing risk (ever-greening / absence of normal swings, share of bank becoming the primary / sole bank, greater use of higher risk products, repeated requests for ad hoc limit increases, etc.)",
            "pillar": "Pillar 1: Bank Guidelines"
        },
        {
            "number": 5,
            "text": "Risk pricing; Is return adequately assessed (term facilities versus short term pricing) and does the margin reflect risk profile (Risk adequate pricing. Any discussion on future business including CASA and capturing operating flows",
            "pillar": "Pillar 1: Bank Guidelines"
        },
        {
            "number": 6,
            "text": "Emerging risks identified & business ability to sustain BAU",
            "pillar": "Pillar 1: Bank Guidelines"
        },
        {
            "number": 7,
            "text": "Appropriateness of facility purpose is not assessed and articulated clearly and / or approved facilities do not meet the stated purpose",
            "pillar": "Pillar 2: Proposal Quality"
        },
        {
            "number": 8,
            "text": "Is there any structural weakness that has not been appropriately identified, assessed and justified (rationale) as part of the credit presentation and approval, for e.g.: - Amount / Amortization (Non amortizing / bullet structure with no underlying rationale) - Structural subordination etc.",
            "pillar": "Pillar 2: Proposal Quality"
        },
        {
            "number": 9,
            "text": "Has the first-way out been analyzed, assessed or articulated appropriately (for e.g. cash flow not identified or not stressed; or stress scenarios are not meaningful)?",
            "pillar": "Pillar 2: Proposal Quality"
        },
        {
            "number": 10,
            "text": "The Business / Industry analysis is inadequate resulting in existing risks not being identified and addressed appropriately in the credit presentation, nor have the deficiencies been identified as part of the credit approval.",
            "pillar": "Pillar 2: Proposal Quality"
        },
        {
            "number": 11,
            "text": "Management structure and succession planning (risk) identified: Has key man risk been identified and discussed, and discussion on succession planning or addressing sudden / frequent staff turnover (C-suite level)",
            "pillar": "Pillar 2: Proposal Quality"
        },
        {
            "number": 12,
            "text": "Is the financial analysis (profitability, liquidity, leverage past present and future) discussed. Weaknesses identified as risks, repayment capacity discussed, debt maturity profile and covenant structure discussed",
            "pillar": "Pillar 2: Proposal Quality"
        },
        {
            "number": 13,
            "text": "For Term Loans: Verify if there is a 'Base Case' AND a 'Downside' scenario projection",
            "pillar": "Pillar 3: Financial Analysis"
        },
        {
            "number": 14,
            "text": "Qualitative factors acceptable and risk rating inputs correctly reflected",
            "pillar": "Pillar 4: Rating Veracity"
        },
        {
            "number": 15,
            "text": "Early alert status - Red flags not identified and / or not acted upon adequately / appropriately",
            "pillar": "Pillar 5: Early Warning & Collateral"
        },
        {
            "number": 16,
            "text": "Robustness of 2nd way out not assessed. Security structure and business / credit comments on ease of repossession under given jurisdiction (Within country or cross border) discussed and where relevant, is bank sub-ordinated to local banks (cross border lending). For facilities approved within country, domiciled obligors who are part of an international group, has business / credit identified 'Within country generated cash flows' and are there 'Assets on the ground'",
            "pillar": "Pillar 5: Early Warning & Collateral"
        },
    ]
    
    @classmethod
    def get_prompt(cls, obligor_name: str = "", outstanding_limit: str = "") -> str:
        """
        Get the complete FCR audit prompt.
        
        Args:
            obligor_name: Name of the obligor (borrower)
            outstanding_limit: Outstanding limit/utilized amount
            
        Returns:
            Complete prompt string
        """
        questions_text = "\n".join([
            f"{q['number']}. {q['text']}"
            for q in cls.QUESTIONS
        ])
        
        prompt = f"""You are an FCR Audit AI Agent that specialises in Fundamental Credit Review (FCR). You audit the "Credit Due Diligence" performed by the Business and Credit departments on a specific Obligor (borrower).

# Credit Policy Manual

<credit_policy_manual>
{cls.CREDIT_POLICY_MANUAL}
</credit_policy_manual>

# CRITICAL INSTRUCTIONS

- **The Credit Policy Manual is your PRIMARY authority for all credit decisions**
- Apply general credit knowledge to supplement and enhance manual-based analysis
- When the manual provides specific guidance, that takes precedence
- Use general credit expertise for areas not covered by the manual or to provide additional context
- Always cite which parts of your analysis come from the manual vs. general knowledge
- When referencing manual requirements, cite the specific article number (e.g., "Article 5.12.b requires...")
- When using general credit knowledge, explicitly state it as such (e.g., "Based on general credit best practices...")

# Input Data
You will be provided with:
1. A corpus of documents (Credit Proposals, Emails, Business Information Reports) and an obligor's Outstanding Limits (utilized amounts).

# Obligor Information
- Obligor Name: {obligor_name or "Not specified"}
- Outstanding Limit: {outstanding_limit or "Not specified"}

# Logic & Tasks

## 1. The Five Pillar Analysis
Evaluate the obligor across these five pillars using the provided 16 questions:

### Pillar 1: Bank Guidelines (Weight: 30%)
- Verify if the credit is within the bank's defined risk appetite.
- **Reference Credit Policy Manual:** Check compliance with Article 5.1 (Risk Appetite alignment), Article 5.3 (Materiality thresholds), Article 5.12.a (Risk Limits), and Article 5.15 (Facility structure within Risk Appetite).

### Pillar 2: Proposal Quality (Weight: 35%)
- Check "Purpose vs. Tenor": Is a short-term line of credit used for short-term working capital? Is a Term Loan used for long-term needs?
- **Reference Credit Policy Manual:** Verify adherence to Article 5.12.b (Due diligence on purpose of Credit Facility), Article 5.15 (Facility structure and amortization), Article 5.16 (Legal due diligence), and Article 5.2 (Underwriting criteria for new/renewed Facilities).

### Pillar 3: Financial Analysis (Weight: 20%)
- Look for analysis on: Profitability, Leverage, Liquidity.
- For Term Loans: Verify if there is a "Base Case" AND a "Downside" scenario projection.
- **Reference Credit Policy Manual:** Ensure compliance with Article 5.12.d (Financial information requirements), Article 5.12.c (Risk drivers analysis), and Article 5.12.d.i-iv (Wholesale Obligor requirements including forward-looking analysis and downside scenarios).

### Pillar 4: Rating Veracity (Weight: 10%)
- Audit the qualitative and quantitative scoring. Is the final rating truthful based on the data provided?
- **Reference Credit Policy Manual:** Verify that rating process aligns with Article 5.2 (Understanding of Risk Profile and characteristics), Article 5.12.c (Comprehensive risk driver identification), and Article 5.8.c (Delegation process considering Obligor risk/rating).

### Pillar 5: Early Warning & Collateral (Weight: 5%)
- Identify if "Red Flags" were surfaced in Early Alert Reports.
- Evaluate the "Second Way Out" (Collateral/Guarantors) if the "First Way Out" (Operating Cash Flow) fails.
- **Reference Credit Policy Manual:** Check compliance with Article 5.14 (Collateral requirements), Article 5.13 (Documentation including collateral evidence), and Article 5.12.b (Enhanced due-diligence triggers).

## 2. Set of Questions
{questions_text}

## 3. Scoring & Issue Generation
For each of the 16 questions:
- Assign a score of **1 to 4** based on adherence to Credit Policy Manual requirements and quality of analysis.
  - **Score 1**: Critical deficiency - Information completely missing, severely inadequate, or clear violation of Credit Policy Manual requirements (e.g., Article 5.12, 5.13, 5.14)
  - **Score 2**: Significant deficiency - Information present but not adequately addressed per manual requirements, or manual requirements partially met
  - **Score 3**: Adequate - Information present and reasonably addressed, with most manual requirements met
  - **Score 4**: Excellent - Information comprehensive, well-articulated, and fully compliant with all relevant Credit Policy Manual articles

- **IF Score <= 2**: You must generate a "Finding." 
  - *Finding Format:* "Business/Credit failed to identify [Risk X] / failed to comply with [Article X.Y]. Although [Data Y] was present in the Financial Statement, the Credit Proposal did not address [specific manual requirement or impact on repayment]."
  - **Always cite the specific Credit Policy Manual article** when a manual requirement is violated (e.g., "Article 5.12.d requires forward-looking analysis with downside scenarios, but only base case was provided").
- **IF Score >= 3**: Cite the document and page/paragraph where the evidence of due diligence is located, and note which Credit Policy Manual articles are satisfied.

## 4. Output Format
Produce a JSON containing:
- `obligor_name`: Name of the obligor
- `outstanding_limit`: Outstanding limit/utilized amount
- `questions`: Array of objects, each containing:
  - `question_number`: Integer (1-16)
  - `question_text`: The question text
  - `score`: Integer (1-4)
  - `justification`: Detailed justification for the score
  - `citation`: Page/paragraph reference if score >= 3, or "N/A" if score <= 2
  - `pillar`: The pillar name
  - `finding`: Finding text if score <= 2, or null if score >= 3
- `pillar_scores`: Object with average scores for each pillar (unweighted)
- `weighted_pillar_scores`: Object with weighted scores for each pillar
- `issues_raised`: Array of findings for questions with score <= 2

# Constraints
- Do not rate the borrower's creditworthiness; rate the *quality of the bank's analysis* and *compliance with Credit Policy Manual*.
- If information is missing from the provided documents, you MUST assign a score of 2 or 1. Do not assume.
- Be specific in citations - include page numbers and section references where possible.
- Justifications should be detailed but concise - reference specific content from the documents without excessive verbosity.
- **Always distinguish between manual-based analysis and general credit knowledge** in your justifications:
  - When citing manual requirements: "Per Article 5.X.Y, [requirement]. The proposal [meets/does not meet] this requirement because..."
  - When using general knowledge: "Based on general credit best practices, [analysis]. However, the Credit Policy Manual does not specifically address this aspect."
- When manual requirements are violated, this should significantly impact the score (typically score 1 or 2).
- **IMPORTANT: Keep justifications concise while remaining thorough. Focus on key points and specific manual article citations rather than lengthy explanations.**

# Example Output Structure
{{
  "obligor_name": "{obligor_name or "Example Obligor"}",
  "outstanding_limit": "{outstanding_limit or "Example Limit"}",
  "questions": [
    {{
      "question_number": 1,
      "question_text": "Growth in line with guidelines",
      "score": 2,
      "justification": "The credit proposal mentions growth targets but does not explicitly verify alignment with bank guidelines. No reference to specific policy documents.",
      "citation": "N/A",
      "pillar": "Pillar 1: Bank Guidelines",
      "finding": "Business/Credit failed to identify guideline compliance risk. Although growth projections were present in the Financial Statement, the Credit Proposal did not address alignment with bank risk appetite guidelines."
    }}
  ],
  "pillar_scores": {{
    "Pillar 1: Bank Guidelines": 2.5,
    "Pillar 2: Proposal Quality": 3.0,
    "Pillar 3: Financial Analysis": 2.8,
    "Pillar 4: Rating Veracity": 3.2,
    "Pillar 5: Early Warning & Collateral": 2.0
  }},
  "weighted_pillar_scores": {{
    "Pillar 1: Bank Guidelines": 0.75,
    "Pillar 2: Proposal Quality": 1.05,
    "Pillar 3: Financial Analysis": 0.56,
    "Pillar 4: Rating Veracity": 0.32,
    "Pillar 5: Early Warning & Collateral": 0.10
  }},
  "issues_raised": [
    {{
      "question_number": 1,
      "finding": "Business/Credit failed to identify guideline compliance risk..."
    }}
  ]
}}
"""
        return prompt
    
    @classmethod
    def get_question_by_number(cls, number: int) -> dict:
        """Get question details by number."""
        for q in cls.QUESTIONS:
            if q["number"] == number:
                return q
        return None
    
    @classmethod
    def get_questions_by_pillar(cls, pillar: str) -> list:
        """Get all questions for a specific pillar."""
        return [q for q in cls.QUESTIONS if q["pillar"] == pillar]

