# EdgeGuard: An Adaptive Privacy-Preserving Gateway for Secure Industrial LLM Integration

## Title Page

**EdgeGuard: An Adaptive Privacy-Preserving Gateway for Secure Industrial LLM Integration**

A B.Tech project report submitted in partial fulfillment of the requirements for the award of the degree of

**Bachelor of Technology**

by

**Nisarg Parmar (Roll No. 202201443)**  
**Saish Pagar (Roll No. 202201092)**

Under the Supervision of

**Prof. [Supervisor Name]**

DA-IICT, Gandhinagar

---

## Certificate

This is to certify that the report entitled **"EdgeGuard: An Adaptive Privacy-Preserving Gateway for Secure Industrial LLM Integration"**, submitted by **Nisarg Parmar** and **Saish Pagar** to DA-IICT, for the award of the degree of **Bachelor of Technology in Information and Communication Technology (ICT)**, is a record of the original, bona fide work carried out by them under my supervision and guidance. The report has reached the standards fulfilling the requirements of the regulations related to the award of the degree.

The results contained in this report have not been submitted in part or in full to any other University or Institute for the award of any degree or diploma to the best of my knowledge.

....................................  
**Prof. [Supervisor Name]**  
DA-IICT, Gandhinagar

---

## Declaration

We declare that this written submission represents our ideas in our own words and where others' ideas or words have been included, we have adequately cited and referenced the original sources. We also declare that we have adhered to all principles of academic honesty and integrity and have not misrepresented or fabricated or falsified any data in our submission. We understand that any violation of the above will be cause for disciplinary action by the Institute and can also evoke penal action from the sources which have thus not been properly cited or from whom proper permission has not been taken when needed.

...........................  
**Nisarg Parmar**  
Roll No.: 202201443

...........................  
**Saish Pagar**  
Roll No.: 202201092

Date:  
Place: DA-IICT, Gandhinagar

---

## Acknowledgements

We would like to express our sincere gratitude to our supervisor, **Prof. [Supervisor Name]**, for the guidance, encouragement, and technical direction provided throughout this B.Tech project. His insights were instrumental in shaping both the research perspective and the engineering realization of this work.

We also thank the faculty and institute for providing an academic environment that encouraged us to explore contemporary problems in secure AI systems. Finally, we are grateful to our peers and well-wishers whose feedback and support helped us refine the conceptual and practical aspects of this project.

**Nisarg Parmar**  
**Saish Pagar**

---

## Abstract

The idea for this project emerged from a focused case-study review of recent research on cloud-edge-client architectures for Large Language Models (LLMs), together with literature on prompt injection, privacy-preserving inference, and secure Retrieval-Augmented Generation (RAG). That review revealed a recurring practical tension in industrial AI adoption. Cloud-hosted LLMs provide strong reasoning and natural-language assistance, yet their direct use in operational environments creates serious concerns related to data sovereignty, prompt injection, response trustworthiness, and the uncontrolled disclosure of sensitive local knowledge. In contrast, purely edge-hosted solutions improve privacy but often lack the reasoning strength required for complex industrial support tasks. This report presents **EdgeGuard**, an adaptive privacy-preserving gateway designed to mediate that tension through a secure hybrid architecture.

EdgeGuard is implemented as a localized trust boundary placed before external model inference. The system is built around three technical layers: **semantic de-identification**, which identifies and masks structured industrial identifiers before transmission; **adversarial input filtering**, which analyzes prompts for policy bypass, privilege escalation, and data-exfiltration behavior; and **secure local contextualization**, which retrieves only role-approved operational knowledge while preventing the exposure of restricted internal records. Together, these layers create a protective sleeve that allows an organization to use external LLMs without forwarding raw operational context directly.

To evaluate the feasibility of the approach, a complete simulation pipeline and an interactive web-based demonstration platform were developed. The prototype includes a gateway orchestration backend, a curated industrial knowledge base, scenario-driven validation, and an OpenAI-compatible response connector with offline fallback support for disconnected demonstrations. Experimental evaluation over benign and adversarial scenarios showed that the EdgeGuard pipeline successfully blocked all simulated malicious requests in the current test set, performed semantic masking on sensitive identifiers, prevented restricted knowledge exposure, and returned grounded, safety-oriented responses for legitimate users. Although the gateway introduces additional processing latency compared to a direct cloud path, the resulting gains in privacy, trustworthiness, and operational safety suggest that EdgeGuard provides a practical architectural model for secure industrial LLM integration.

---

## Contents

1. Introduction  
2. Literature Review and Comparative Study  
3. EdgeGuard System Design  
4. Implementation and Software Architecture  
5. Analysis and Results  
6. Conclusions and Practical Implications  
Appendices  
Bibliography

---

## List of Figures

**Figure 3.1** Overall EdgeGuard architecture with cloud-edge-client separation  
**Figure 3.2** Internal gateway pipeline for semantic de-identification, filtering, and retrieval  
**Figure 4.1** Interactive EdgeGuard dashboard  
**Figure 4.2** Backend request-response flow  
**Figure 5.1** Comparative results for baseline versus EdgeGuard  
**Figure 5.2** Example blocked malicious-query response

---

## Abbreviations

**AI** Artificial Intelligence  
**API** Application Programming Interface  
**EI** Edge Intelligence  
**IIoT** Industrial Internet of Things  
**JSON** JavaScript Object Notation  
**KB** Knowledge Base  
**LLM** Large Language Model  
**PII** Personally Identifiable Information  
**RAG** Retrieval-Augmented Generation  
**RBAC** Role-Based Access Control  
**SOP** Standard Operating Procedure  
**UI** User Interface  
**WAN** Wide Area Network

---

## Chapter 1: Introduction

### 1.1 Motivation

The motivation for this project emerged through a case-study driven reading of the literature provided for the B.Tech project. We examined recent work on LLM-based edge intelligence, cloud-edge-client deployment models, prompt injection defense, and secure knowledge retrieval. A common pattern became immediately visible. Researchers and system designers increasingly want to use LLMs in practical environments because of their ability to summarize logs, explain anomalies, interpret operator queries, and convert technical records into usable recommendations. However, the same literature also shows that direct LLM deployment in sensitive environments introduces unresolved issues around trustworthiness.

Industrial settings make this tension even sharper. Unlike casual chatbot usage, industrial AI systems may operate around machine telemetry, maintenance records, supplier details, confidential operating thresholds, or process-specific formulas. A cloud-only design may expose too much contextual information to external inference endpoints. An edge-only design may preserve privacy but often cannot offer the same reasoning quality as large external models. As a result, industrial adoption is constrained not by the lack of AI capability, but by the absence of a trustworthy mediation layer between local operations and external reasoning systems.

This observation led directly to the EdgeGuard idea. Instead of assuming that the model itself will solve privacy and security concerns, we frame the problem as a gateway-design challenge. If a localized gateway can sanitize sensitive data, inspect for adversarial intent, and selectively inject minimal local context, then an organization can safely benefit from cloud-scale reasoning without surrendering raw internal information. This design philosophy converts the abstract trustworthiness concerns raised in recent surveys into a practical systems-engineering problem.

### 1.2 Problem Statement

The objective of this B.Tech project is to design and implement **EdgeGuard**, an adaptive privacy-preserving gateway that enables the safe use of external or cloud-based Large Language Models in industrial settings. The gateway must ensure that sensitive identifiers and operational records are not transmitted in raw form, that prompt injection and related adversarial inputs are intercepted before inference, and that contextually grounded answers can still be generated using locally available operational knowledge.

The engineering challenge is therefore threefold. First, the system must preserve privacy by de-identifying structured industrial information in real time. Second, it must defend the inference pipeline against malicious linguistic instructions that attempt to override policies, extract secrets, or bypass trust controls. Third, it must ground legitimate user queries in role-appropriate local information without revealing the full contents of a restricted internal knowledge base. The final system must be demonstrable through both a simulation pipeline and a presentation-ready interactive application.

### 1.3 Project Objectives

To solve the above problem, this project is organized around the following engineering objectives:

- To design a **semantic de-identification module** that identifies and masks asset identifiers, formula references, employee IDs, and related structured operational tokens before any cloud transmission.
- To implement an **adversarial input filtering module** that assigns risk scores to incoming prompts and blocks requests that demonstrate prompt injection, privilege escalation, or exfiltration intent.
- To build a **secure local contextualization module** based on RAG principles, ensuring that only approved and role-specific operational documents are used for response grounding.
- To create a **hybrid edge-cloud architecture** in which a local gateway mediates all interaction between industrial users and an external LLM.
- To develop a **full simulation pipeline** for validating benign and adversarial industrial scenarios.
- To build an **interactive software prototype** that visualizes the complete trust pipeline in a presentation-friendly way.
- To evaluate the architecture using metrics related to security, privacy protection, contextual relevance, and latency trade-offs.

### 1.4 Dissertation Organization

This dissertation is organized into six chapters to systematically present the conceptual, architectural, implementation, and evaluative aspects of EdgeGuard:

- **Chapter 1 (Introduction):** Describes the motivation, problem statement, and technical objectives of the project.
- **Chapter 2 (Literature Review and Comparative Study):** Reviews relevant work in edge intelligence, privacy-preserving inference, prompt defense, and secure retrieval, and identifies the research gap addressed by EdgeGuard.
- **Chapter 3 (EdgeGuard System Design):** Presents the overall architecture of the proposed gateway and explains the design of each trust-enforcing module.
- **Chapter 4 (Implementation and Software Architecture):** Describes the implementation of the simulation pipeline, backend gateway service, interactive dashboard, and LLM connector.
- **Chapter 5 (Analysis and Results):** Evaluates the system over multiple industrial scenarios and compares the EdgeGuard pipeline against a direct cloud baseline.
- **Chapter 6 (Conclusions and Practical Implications):** Summarizes the findings, contributions, limitations, and future scope of the project.

---

## Chapter 2: Literature Review and Comparative Study

### 2.1 Introduction

The secure deployment of LLMs in industrial environments draws from several overlapping domains of research. Edge intelligence explores how advanced AI capabilities can be moved closer to data sources. Privacy-preserving inference studies how sensitive inputs can be protected during model usage. Prompt-security research investigates adversarial language attacks such as prompt injection and jailbreaking. Secure RAG literature examines how private knowledge can be incorporated into generation pipelines without creating leakage risks. This chapter synthesizes these strands and explains how they collectively motivate the EdgeGuard approach.

### 2.2 LLM-Based Edge Intelligence

Recent survey work on LLM-based edge intelligence emphasizes that cloud-only deployment is often insufficient in environments where latency, privacy, autonomy, and resilience matter. Friha et al. argue that edge integration improves local responsiveness and data control, but they also highlight security and trustworthiness as central unresolved concerns. Their survey is especially relevant because it does not treat edge deployment as merely a performance optimization; instead, it frames the problem as an architectural balancing act between capability, safety, and operational practicality.

This framing is important for industrial contexts. Pure edge deployment may reduce the need to send data externally, but high-capacity reasoning still often depends on models or services beyond the resource limits of local devices. A hybrid approach therefore becomes attractive: local systems perform trust enforcement and context handling, while external models provide the heavier reasoning layer. This is the general design space within which EdgeGuard is situated.

### 2.3 Prompt Injection and Adversarial Threats

The literature review supplied for this project identifies prompt injection and jailbreaking as some of the most serious threats to integrated AI systems. This is consistent with broader research trends. Attackers can embed instructions that attempt to override prior policies, reveal hidden prompts, expose confidential content, or manipulate downstream actions. In an industrial environment, such attacks are not merely academic. They may result in the leakage of maintenance secrets, proprietary formulas, internal procedures, or operational configurations.

One consistent conclusion across the literature is that provider-side guardrails alone are not sufficient for specialized, domain-sensitive applications. A system that depends only on the cloud model’s internal safety policies has already sent the risky query to the external endpoint. For industrial workflows, security controls must therefore operate at the network entry point, before the model is reached. This insight directly supports the gateway-based filtering strategy of EdgeGuard.

### 2.4 Privacy-Preserving Inference and Semantic De-identification

Another important research thread concerns privacy during inference. Traditional approaches often focus on encryption, anonymization, or generic redaction. However, recent research has increasingly moved toward **semantic de-identification**, in which structured and context-specific patterns are masked in a way that preserves the meaning of the request while reducing disclosure risk. This shift is particularly relevant to industrial environments where sensitive information does not always appear as conventional PII. A machine serial, formula reference, calibration identifier, batch code, or employee tag may be operationally sensitive even if it is not personally identifying in the classical sense.

The literature review provided for this project highlights the importance of moving this sanitization step to the edge. Doing so creates a local privacy checkpoint that prevents raw identifiers from ever leaving the operational environment. EdgeGuard adopts that logic by implementing real-time masking before any request is considered for cloud inference.

### 2.5 Secure RAG and Knowledge Isolation

RAG has become a dominant strategy for improving LLM relevance in domain-specific tasks. Instead of retraining the model, a system retrieves context from local documents and includes that context in the inference prompt. While effective, this architecture introduces a new attack surface. If retrieval is unrestricted or loosely controlled, private documents may be exposed indirectly through generation. Research on RAG security therefore stresses restricted retrieval, minimal disclosure, secure embeddings, and clear access boundaries.

For industrial settings, this means that a local knowledge base must not be treated as a transparent extension of the model. Only the minimum necessary information should be forwarded, and role-based access rules must remain intact throughout the pipeline. EdgeGuard operationalizes this principle through a simple but explicit retrieval policy: role-approved documents may be surfaced, while restricted content remains local even if the query appears highly relevant.

### 2.6 Adaptive Gateway Thinking

The supplied literature review also pointed to work on AI-driven gateway security and adaptive policy enforcement for decentralized edge systems. The core insight across such work is that the gateway is a natural enforcement point because it sits at the intersection of user intent, local data, and external services. It can observe the incoming request, apply context-sensitive policy, and decide whether to sanitize, monitor, retrieve, forward, or block. This perspective is especially useful for EdgeGuard because it allows us to unify privacy preservation, prompt security, and contextual retrieval into one coherent control layer.

### 2.7 Research Gaps and Proposed Novelty

The literature contains substantial work on each individual component that EdgeGuard uses. There are surveys on edge intelligence, papers on prompt defense, research on privacy-preserving inference, and emerging work on secure RAG. However, relatively little attention has been paid to a **unified industrial gateway** that combines these mechanisms into a single adaptive architecture for external LLM usage. Existing solutions are frequently either cloud-only, which weakens privacy guarantees, or edge-only, which weakens reasoning capability.

EdgeGuard addresses this gap by combining three trust-enforcing layers into a single pre-inference sleeve:

- semantic de-identification of sensitive operational content
- adversarial prompt filtering before inference
- restricted local contextualization with role-aware retrieval

The novelty of the project lies less in inventing each component independently and more in the systems-level integration of these components for a practical industrial trust boundary.

### 2.8 Summary

The literature indicates that secure industrial use of LLMs requires more than a powerful model. It requires a surrounding architecture that can enforce privacy, defend against adversarial prompts, and ground responses in local knowledge without exposing the entire knowledge base. EdgeGuard is proposed as such an architecture, and the subsequent chapters describe its design and implementation.

---

## Chapter 3: EdgeGuard System Design

### 3.1 Introduction

The EdgeGuard architecture is designed as a hybrid cloud-edge-client trust gateway. Its central design principle is that no industrial request should reach an external LLM in raw form. Instead, each request passes through a sequence of local controls that inspect, sanitize, and selectively enrich it. This chapter explains the structure of the system and the design logic of its major modules.

### 3.2 Overall Architecture

At a high level, EdgeGuard consists of four layers:

1. **Client Layer:** the operator, engineer, or analyst interface through which an industrial query is submitted.
2. **EdgeGuard Gateway Layer:** the local trust boundary where privacy masking, threat detection, and retrieval orchestration take place.
3. **Local Knowledge Layer:** a curated knowledge base containing SOPs, maintenance notes, policy documents, and restricted records.
4. **External Reasoning Layer:** a cloud or externally hosted LLM that receives only the sanitized query and approved contextual bundle.

This separation is important because it preserves a clear trust boundary. Sensitive industrial content is handled locally first. Only the filtered and approved subset of the request is passed forward. If the query is judged unsafe, inference is never attempted.

### 3.3 Semantic De-identification Module

The first module in the EdgeGuard pipeline is semantic de-identification. Its purpose is to preserve the user’s intent while minimizing the exposure of structured sensitive identifiers. In the current implementation, the masking logic recognizes several industrially relevant token types:

- asset IDs such as machine or equipment labels
- formula references and batch codes
- employee identifiers
- IP-style structured technical identifiers

Each matched item is replaced with a stable placeholder such as `<asset_id_1>` or `<employee_id_1>`. This allows the downstream reasoning system to retain the structural meaning of the query without seeing the original operational identifier. The design decision here is deliberate: instead of deleting sensitive content entirely, the system preserves semantic shape so that the LLM can still understand relationships in the prompt.

### 3.4 Adversarial Input Filtering Module

The second module is adversarial input filtering. This component performs pattern-based risk scoring over the sanitized input. It searches for linguistic indicators associated with prompt injection and exfiltration attempts, including:

- instruction override attempts such as “ignore previous instructions”
- privilege escalation language such as “act as administrator”
- direct secret extraction requests
- bulk extraction requests such as dumping logs or listing confidential assets
- policy-bypass language

Each detected pattern contributes to a cumulative threat score. If the score crosses a defined threshold, the request is blocked and escalated locally. If the score is non-trivial but below the blocking threshold, the query is marked as monitored and allowed to proceed under observation. This design enables a graded response rather than a simplistic safe/unsafe split.

### 3.5 Secure Local Contextualization Module

The third module is the secure local contextualization layer. Its purpose is to inject only the minimum relevant operational context into the inference flow. The local knowledge base is tagged by both topic and access level. In the current prototype, documents are categorized around operations, maintenance, security, and restricted content. A role-based access policy then determines what a given requester may retrieve.

For example:

- an operations user may receive operations documents
- a maintenance user may access maintenance and operations documents
- a security user may access security and operations documents
- restricted documents are never released to the cloud-facing inference stage

This design is intentionally conservative. The system chooses minimum necessary retrieval over maximum relevance in order to preserve the zero-trust posture of the gateway.

### 3.6 Data Flow and Trust Boundaries

From a trust-boundary perspective, the EdgeGuard pipeline can be understood as a sequence of decision gates:

1. The client submits a raw industrial request.
2. The gateway performs local masking of sensitive identifiers.
3. The adversarial filter evaluates the sanitized prompt.
4. If unsafe, the query is blocked locally and never reaches inference.
5. If safe, the retrieval layer selects only approved local documents.
6. The external model receives the sanitized query plus approved context only.
7. The response is returned to the user together with a local trace of gateway decisions.

This flow ensures that three categories of content remain explicitly protected:

- original sensitive identifiers
- restricted knowledge-base records
- blocked malicious requests

### 3.7 Adaptive Design Rationale

The word “adaptive” in EdgeGuard refers to two related properties. First, the gateway changes its behavior based on the observed risk of the prompt. A safe query, a monitored query, and a blocked query do not receive the same treatment. Second, the retrieval behavior changes according to the requester role and the semantic content of the prompt. This combination of threat-aware and context-aware behavior makes the system more useful than a rigid filter and more trustworthy than a direct passthrough.

### 3.8 Summary

EdgeGuard is designed not as a monolithic model, but as a layered trust architecture. Semantic masking reduces privacy exposure, adversarial filtering protects the inference boundary, and secure retrieval grounds the response while preserving local isolation. Together these modules define the architectural contribution of the project.

---

## Chapter 4: Implementation and Software Architecture

### 4.1 Introduction

To validate the proposed design, a complete simulation pipeline and an interactive application were implemented. The goal of the implementation was not only to show the conceptual feasibility of EdgeGuard, but also to produce a demonstrable and presentation-ready prototype that makes each trust-enforcing stage visible. This chapter explains the software organization of the project and the logic of its major components.

### 4.2 Core Simulation Package

The core trust logic of the project is implemented in the `edgeguard_sim` package. This package contains the underlying simulation primitives:

- `data.py` stores the local knowledge base and scenario set
- `gateway.py` implements semantic de-identification and adversarial filtering
- `rag.py` implements secure retrieval
- `simulation.py` orchestrates baseline and EdgeGuard comparative runs

The knowledge base used in the prototype contains a small but representative set of industrial documents, including boiler safety instructions, predictive maintenance notes, a mixing safety rule, a gateway policy note, an escalation playbook, and a restricted secret record. The scenario set includes both benign and adversarial prompts so that the gateway can be evaluated under mixed operational conditions.

### 4.3 Interactive Dashboard

In addition to the offline simulation, a browser-based interactive dashboard was developed. The dashboard is designed as a control center rather than a minimal form page. Its major sections include:

- a hero/status panel displaying backend mode and LLM configuration
- a query panel where the requester role and prompt can be chosen
- preset scenario cards for presentation-friendly demonstrations
- a metrics strip showing threat status, score, latency, redactions, and retrieved documents
- a pipeline timeline visualizing the stages executed by the gateway
- a sanitized-query panel showing masking results
- an approved-context panel showing retrieved local documents
- a final-response panel showing whether the result was live, fallback, or blocked

This interface is important pedagogically because it transforms an otherwise hidden backend trust flow into a visible and explainable process.

### 4.4 Backend Gateway Service

The backend request orchestration is implemented in the `edgeguard_app` package. A request submitted from the UI is passed to the `EdgeGuardService`, which performs the following sequence:

1. receive raw query and user role
2. sanitize the query
3. compute adversarial threat score
4. block immediately if the query violates policy
5. retrieve approved local context if the query is safe
6. call the response engine
7. package all metrics, traces, and outputs into a structured JSON payload

This service returns not only the final answer but also the evidence trail needed to explain why the answer took the form it did.

### 4.5 HTTP Server and Request Routing

To avoid unnecessary dependency complexity, the application uses a standard-library based HTTP server rather than a full external framework. The main server exposes four essential routes:

- `/` for the frontend page
- `/api/config` for backend capability status
- `/api/scenarios` for preset scenarios
- `/api/ask` for processing live user queries

This design keeps the app lightweight and easy to run in a local academic environment while still supporting the interaction patterns needed for a polished demonstration.

### 4.6 LLM Connector and Fallback Strategy

The project includes an OpenAI-compatible connector that can send sanitized prompts and approved context to a live API when credentials are available. This connector constructs two messages:

- a system message defining the secure assistant behavior
- a user message containing the requester role, sanitized query, and approved local context

If no live API key is configured, or if the request fails, the system uses an offline grounded fallback responder. The fallback responder does not pretend to be a fully live cloud model; instead, it produces a structured response using the retrieved local documents. This choice ensures that the application remains functional and demonstrable even in the absence of API billing or connectivity, while preserving the architectural logic of the project.

### 4.7 Scenario Dataset and Validation Inputs

The scenario dataset used in the prototype consists of six representative industrial prompts:

- a benign boiler-pressure support request
- a maintenance request containing sensitive identifiers
- a prompt injection request attempting administrative override
- a bulk data-exfiltration request
- a local security policy query
- a mixed query containing both valid operational context and malicious extraction intent

This dataset is intentionally small but carefully chosen to test each branch of the trust pipeline. It allows the system to show privacy masking, safe retrieval, monitored queries, and complete blocking behavior.

### 4.8 Deployment Workflow

The software can be executed in two forms:

- as an offline simulation using `run_simulation.py`
- as an interactive browser application using `run_edgeguard_app.py`

The simulation writes structured outputs in JSON and Markdown form. The app serves an interactive UI locally and can optionally integrate with a live LLM backend through environment configuration. This dual-mode deployment supports both formal report evaluation and live project presentation.

### 4.9 Summary

The implementation of EdgeGuard demonstrates that the proposed trust architecture can be translated into a working software prototype. The project combines a modular simulation core, a lightweight backend, a demonstrable dashboard, and a live-or-fallback response connector to produce a complete end-to-end system.

---

## Chapter 5: Analysis and Results

### 5.1 Introduction

This chapter evaluates the behavior of EdgeGuard under a controlled set of industrial scenarios. The objective of the analysis is not to claim production-level benchmarking, but to study whether the proposed architecture behaves as intended when compared with a direct cloud-style baseline. The evaluation therefore focuses on architectural behavior rather than raw model accuracy alone.

### 5.2 Experimental Setup

Two pipelines were considered in the simulation:

- a **baseline cloud path**, in which the query is effectively forwarded without local trust enforcement
- the **EdgeGuard path**, in which the query passes through semantic masking, adversarial filtering, and secure retrieval before inference

The comparison uses the following metrics:

- average latency
- number of blocked malicious requests
- attack blocking rate
- number of redactions applied
- number of restricted exposures prevented

The evaluation scenarios included both benign and adversarial prompts so that trust enforcement and operational utility could be examined together.

### 5.3 Scenario-Based Validation

#### 5.3.1 Benign Operations Query

In the first scenario, an operations user reported elevated boiler pressure and requested a safe near-term response plan. The EdgeGuard pipeline allowed the query, redacted the machine identifier, and retrieved two relevant local documents: a boiler shutdown SOP and an operator escalation playbook. The resulting response was contextually grounded and operationally constrained. This demonstrates that the gateway does not simply block by default; it supports legitimate tasks while enforcing local trust rules.

#### 5.3.2 Sensitive Maintenance Query

The second scenario involved a maintenance query that contained a motor serial and a supplier batch reference. The system applied two semantic redactions and retrieved maintenance-relevant documents while preserving the meaning of the request. This case is especially important because it illustrates the privacy logic of EdgeGuard. The model still receives an interpretable prompt, but the original identifiers are never sent out in raw form.

#### 5.3.3 Prompt Injection Attempt

The third scenario explicitly attempted to override prior instructions, assume administrative privilege, and reveal restricted information. EdgeGuard assigned a maximal threat score and blocked the request before inference. No documents were retrieved and no cloud-facing reasoning was attempted. This behavior confirms that the adversarial filter functions as a true pre-inference gate rather than as a post-hoc warning system.

#### 5.3.4 Data Exfiltration Attempt

In the fourth scenario, the requester asked for confidential machine serials, supplier details, and proprietary mix ratios. EdgeGuard again blocked the request before inference. The restricted-exposure logic also prevented any secret-bearing internal document from being surfaced. This scenario validates the interaction between the threat detector and the retrieval boundary.

#### 5.3.5 Policy Assistance Query

The fifth scenario was a legitimate security-policy question. The system identified moderate threat-related language but did not block the request because the user was asking about policy rather than attempting to violate it. It retrieved the zero-trust gateway policy and escalation guidance, then returned a grounded answer. This is an important nuance: security-sensitive language does not always imply malicious intent, and the gateway must therefore distinguish between a policy query and a policy attack.

#### 5.3.6 Mixed Benign-Malicious Query

The sixth scenario combined a valid operational signal with an explicit attempt to extract a hidden maintenance password. EdgeGuard treated the malicious portion as dominant and blocked the overall request. This is a desirable behavior in high-stakes environments because partial legitimacy should not be allowed to smuggle unsafe intent across the inference boundary.

### 5.4 Quantitative Results

In the current simulation output, the following results were observed:

| Metric | Baseline Cloud | EdgeGuard |
| --- | ---: | ---: |
| Average latency (ms) | 79.33 | 127.33 |
| Blocked requests | 0 | 3 |
| Blocked attack rate | 0.00 | 1.00 |
| Redactions applied | 0 | 4 |
| Restricted exposures prevented | 0 | 4 |

These values indicate several key points:

- the baseline path is faster because it does not perform trust enforcement
- EdgeGuard introduces moderate gateway overhead
- EdgeGuard blocked all attack scenarios in the evaluated run
- EdgeGuard performed meaningful privacy masking on sensitive inputs
- restricted local content remained protected

### 5.5 Qualitative Interpretation

The numerical results are best understood in terms of architectural trade-offs. A direct cloud path minimizes local processing time, but it also forwards unsafe or overshared content without meaningful control. EdgeGuard accepts a moderate latency increase in order to create three practical guarantees:

1. raw structured identifiers are not forwarded blindly
2. malicious prompt attempts can be blocked before model access
3. local context is injected selectively rather than indiscriminately

In an industrial deployment, these trade-offs are not incidental. They reflect a shift in optimization priorities. The goal is no longer "fastest possible response at any cost," but rather "useful response under bounded trust." This makes EdgeGuard better aligned with operational environments where confidentiality and safety matter more than minimal response delay.

### 5.6 Discussion of Trustworthiness

From a trustworthiness perspective, the evaluation supports the central claim of the project: a gateway-centered architecture can make cloud-scale reasoning more deployable in sensitive industrial contexts. Importantly, EdgeGuard does not eliminate all risk. It does not provide cryptographic secrecy, formal verification, or production-grade adaptive learning in its current form. However, it shows that meaningful trust enforcement can be introduced without abandoning the practical benefits of external LLM reasoning. That systems-level contribution is the main significance of the project.

### 5.7 Summary

The analysis demonstrates that EdgeGuard behaves as intended across a mixed set of benign and adversarial scenarios. The system introduces moderate latency overhead, but it also provides strong benefits in request sanitization, attack blocking, contextual grounding, and restricted-data protection. These findings justify the architectural choices presented in the earlier chapters.

---

## Chapter 6: Conclusions and Practical Implications

### 6.1 Summary

This project explored how large external language models can be used in industrial settings without directly exposing sensitive operational data or trusting the model endpoint unconditionally. Through a case-study guided literature review, we identified that the major obstacles to industrial LLM adoption are not only capability-related but trust-related. Prompt injection, raw data exposure, insecure retrieval, and weak control over cloud inference form a combined systems problem. EdgeGuard was proposed and implemented as a response to that problem.

### 6.2 Study Findings

The study yielded the following principal findings:

- a gateway-first design provides a practical trust boundary for industrial LLM use
- semantic masking can preserve prompt meaning while reducing disclosure risk
- prompt injection defense is most useful before inference, not after it
- secure retrieval improves contextual grounding without requiring full database exposure
- a hybrid cloud-edge design is more practical than a strict cloud-only or edge-only alternative

These findings align with the trends observed in the literature and show that EdgeGuard is conceptually sound as a secure deployment model.

### 6.3 Conclusive Contribution of the Project

The main contribution of this project is the design and implementation of a **unified adaptive gateway** for industrial LLM integration. Rather than treating privacy, adversarial defense, and contextual grounding as separate subsystems, EdgeGuard integrates them into one pre-inference architecture. In addition, the project contributes a working demonstration platform that visualizes each stage of the trust pipeline, making the concept easier to analyze, present, and extend.

### 6.4 Practical Implications

The practical value of EdgeGuard lies in its applicability to industrial use cases such as:

- maintenance-assistance chat systems
- operator support dashboards
- policy-aware incident response tools
- LLM-assisted log interpretation
- plant knowledge retrieval systems

In such systems, blindly exposing raw local context to an external model is often unacceptable. EdgeGuard demonstrates a path toward safer adoption by enforcing a local zero-trust gateway. Even in its prototype form, the project makes clear that a lightweight mediation layer can substantially improve the deployability of industrial LLM solutions.

### 6.5 Study Limitations

Several limitations should be acknowledged:

- the evaluation uses a simulation dataset rather than a production industrial deployment
- the threat detector is rule-based and not trained on large adversarial corpora
- the retrieval layer uses a small curated document set rather than a large-scale enterprise knowledge base
- the current live-LLM mode depends on external API access and billing availability
- the latency and security findings are indicative of prototype behavior, not final production benchmarks

These limitations do not invalidate the architectural contribution, but they do bound the strength of the conclusions.

### 6.6 Scope for Future Work

This project opens several promising directions for future development:

- replace rule-based threat scoring with adaptive or learned classifiers
- integrate embedding-based secure retrieval with stronger policy control
- add enterprise authentication and audit logging
- evaluate the system on larger industrial document collections
- incorporate multi-turn conversational state while preserving trust boundaries
- study formal privacy guarantees and stronger isolation mechanisms
- deploy the system in a real or semi-real industrial pilot environment

### 6.7 Closing Remark

The broader lesson of this project is that trustworthy industrial AI will not emerge from model scale alone. It will emerge from architectures that decide what may be asked, what may be revealed, what must remain local, and when a model should not be consulted at all. EdgeGuard is a step toward that architectural vision.

---

## Appendix A: Simulation Components

The simulation is organized into modular Python components:

- `SemanticDeidentifier`
- `AdversarialFilter`
- `SecureRetriever`
- baseline and EdgeGuard comparative pipelines
- scenario dataset and local knowledge base

These components together implement the trust logic used throughout the report.

## Appendix B: Interactive Application Components

The web prototype includes:

- a backend gateway service
- an HTTP server for request routing
- a browser dashboard
- a response-mode display showing LIVE, FALLBACK, or BLOCKED
- an OpenAI-compatible connector with offline fallback

## Appendix C: Evaluation Scenarios

The six evaluation scenarios used in this project are:

1. benign operations query
2. sensitive maintenance query
3. prompt injection attack
4. bulk exfiltration query
5. policy assistance query
6. mixed benign-malicious prompt

## Appendix D: Suggested Figures and Tables

The following figures should ideally be inserted before final submission:

- system architecture diagram
- trust-boundary data-flow diagram
- dashboard screenshot
- comparative-results bar chart
- blocked-query example

---

## Bibliography

[1] O. Friha, M. A. Ferrag, B. Kantarci, B. Cakmak, A. Ozgun, and N. Ghoualmi-Zine, "LLM-Based Edge Intelligence: A Comprehensive Survey on Architectures, Applications, Security and Trustworthiness," *IEEE Open Journal of the Communications Society*, vol. 5, 2024.

[2] "A Systematic Literature Review on LLM Defenses Against Prompt Injection and Jailbreaking," arXiv preprint, 2026.

[3] "RAG Security and Privacy: Formalizing the Threat Model and Attack Surface," arXiv preprint, 2025.

[4] "Privacy-Aware RAG: Secure and Isolated Knowledge Retrieval," arXiv preprint, 2025.

[5] "AI-Driven Adaptive Security Frameworks for Decentralized Edge Computing," ResearchGate publication, 2026.

[6] M. A. Ferrag et al., "Prompt Injection Attacks: Risks and Defense Mechanisms," 2023.

[7] "A Survey on Privacy-Preserving Machine Learning Inference," ResearchGate publication, 2026.

[8] "Large-Language-Model-Enabled Text Semantic Communication Systems," MDPI publication, 2025.

[9] "AI-Driven API Gateway Security for Real-Time Threat Detection," ResearchGate publication, 2026.

[10] "Cybersecurity Solutions for Industrial IoT-Edge Computing Integration," PMC publication, 2024.

[11] Literature review document provided for the present project, "Literature review.pdf".
